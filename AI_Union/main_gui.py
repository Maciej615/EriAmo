# -*- coding: utf-8 -*-
"""
main_gui.py v4.4.0-HybridInterface
ZMIANY:
- ✅ Graficzny pasek postępu (ttk.Progressbar) zamiast tekstu.
- ✅ Filtracja logów: Haiku, Fraktale i debug zostają TYLKO w terminalu.
- ✅ Chat w GUI zawiera tylko wypowiedzi Ty/EriAmo i ważne statusy.
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
import threading
import queue
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from union_core import EriAmoUnion
    from multimodal_agency import MultimodalAgency
    from union_config import Colors
except ImportError:
    class Colors:
        CYAN = "\x1b[96m"; GREEN = "\x1b[92m"; YELLOW = "\x1b[93m"
        RESET = "\x1b[0m"

class SelectiveRedirector:
    """Przekierowuje wybrane komunikaty do GUI, a wszystko do konsoli."""
    def __init__(self, gui_queue):
        self.queue = gui_queue
        self.terminal = sys.__stdout__ # Oryginalna konsola

    def write(self, string):
        # 1. Zawsze wyślij do oryginalnego terminala (Haiku, Fraktale, etc.)
        self.terminal.write(string)
        
        # 2. Filtruj to, co trafia do okna chatu GUI
        # Nie wpuszczamy Haiku (===), Fraktali i pustych linii
        if any(x in string for x in ["===", "FRACTAL", "DEBUG", "[EXPLORER]"]):
            return

        # Obsługa paska postępu (szukamy frazy 'Postęp: [')
        if "Postęp:" in string:
            match = re.search(r'(\d+)%', string)
            if match:
                self.queue.put(("PROGRESS", int(match.group(1))))
            return

        # Reszta (EriAmo, Kurz, Chunks) trafia do chatu
        if string.strip():
            self.queue.put(("TEXT", string))

    def flush(self):
        self.terminal.flush()

class EriAmoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EriAmo Union v8.6")
        self.root.geometry("950x800")
        self.root.configure(bg="#0f0f0f")
        self.msg_queue = queue.Queue()
        self.is_closing = False
        
        self.color_map = {'96': '#00f0ff', '92': '#00ff00', '93': '#ffff00', '95': '#ff00ff', '0': '#ddd'}
        
        self.init_backend()
        self.create_widgets()
        
        # Przełączamy strumień na nasz selektywny filtr
        sys.stdout = SelectiveRedirector(self.msg_queue)
        self.root.after(100, self.update_loop)

    def init_backend(self):
        try:
            self.union = EriAmoUnion(verbose=True)
            self.agency = MultimodalAgency(self.union, verbose=True)
            self.agency.start(); self.union.start()
        except Exception as e: print(f"Błąd backendu: {e}")

    def create_widgets(self):
        # Panel stanu i pasek postępu (GÓRA)
        self.top_frame = tk.Frame(self.root, bg="#0f0f0f")
        self.top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(self.top_frame, text="EriAmo: Gotowy", bg="#0f0f0f", fg="#555", font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(self.top_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        # Pasek postępu jest domyślnie ukryty (pack_forget)
        
        # Okno Chatu
        self.console_log = scrolledtext.ScrolledText(self.root, bg="#050505", fg="#ddd", font=("Consolas", 12), borderwidth=0)
        self.console_log.pack(fill=tk.BOTH, expand=True, padx=20)
        
        for code, hex_color in self.color_map.items():
            self.console_log.tag_config(code, foreground=hex_color)
        self.console_log.tag_config("USER", foreground="#00ffaa", font=("Consolas", 12, "bold"))

        # Wejście (DÓŁ)
        self.entry = tk.Entry(self.root, bg="#1a1a1a", fg="#fff", font=("Consolas", 13), borderwidth=0, insertbackground="white")
        self.entry.pack(fill=tk.X, padx=20, pady=20, ipady=10)
        self.entry.bind("<Return>", self.send_command)
        self.entry.focus_set()

    def update_loop(self):
        while not self.msg_queue.empty():
            msg_type, data = self.msg_queue.get_nowait()
            if msg_type == "TEXT":
                self.append_text(data)
            elif msg_type == "PROGRESS":
                self.show_progress(data)
        
        if not self.is_closing:
            try:
                intro = self.union.aii.introspect()
                clean_intro = re.sub(r'\x1b\[[0-9;]*m', '', intro)
                self.status_label.config(text=f"Stan: {clean_intro}")
            except: pass
        self.root.after(100, self.update_loop)

    def show_progress(self, value):
        if value < 100:
            if not self.progress.winfo_manager(): # Jeśli ukryty, pokaż go
                self.progress.pack(side=tk.RIGHT, padx=10)
            self.progress['value'] = value
        else:
            self.progress['value'] = 100
            self.root.after(2000, lambda: self.progress.pack_forget()) # Ukryj po 2s

    def append_text(self, text, tag=None):
        ansi_regexp = re.compile(r'\x1b\[([0-9;]*)m')
        parts = ansi_regexp.split(text)
        current_tag = tag
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part: self.console_log.insert(tk.END, part, current_tag)
            else:
                code = part
                if code in self.color_map: current_tag = code
                elif code == "0": current_tag = tag
        self.console_log.see(tk.END)

    def send_command(self, event=None):
        cmd = self.entry.get().strip()
        if not cmd: return
        self.entry.delete(0, tk.END)
        self.append_text(f"\nTy > {cmd}\n", "USER")
        if cmd.lower() in ['exit', 'quit', '/exit', '/quit']:
            self.on_closing()
        else:
            threading.Thread(target=self._process_command_thread, args=(cmd,), daemon=True).start()

    def _process_command_thread(self, cmd):
        response = self.union.process_input(cmd)
        if response: print(f" [EriAmo] {response}")

    def on_closing(self):
        self.is_closing = True
        self.append_text(f"\n{Colors.YELLOW}[SYSTEM] Zamykanie i zapis danych...{Colors.RESET}\n")
        self.root.update()
        self.agency.stop(); self.union.stop()
        self.root.after(1500, lambda: (self.root.destroy(), sys.exit(0)))

if __name__ == "__main__":
    root = tk.Tk()
    app = EriAmoGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()