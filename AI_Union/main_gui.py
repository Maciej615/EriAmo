# -*- coding: utf-8 -*-
"""
main_gui.py v4.2.0-SafeExit
Zapewnia poprawny zapis danych przy zamknięciu okna.
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
import sys
import threading
import queue
import os
import time

# Dodajemy ścieżkę
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from union_core import EriAmoUnion
    from multimodal_agency import MultimodalAgency
    from union_config import Colors
except ImportError:
    class Colors:
        CYAN = ""; RESET = ""; GREEN = ""; YELLOW = ""; MAGENTA = ""

class ConsoleRedirector:
    def __init__(self, text_widget_queue):
        self.queue = text_widget_queue
    def write(self, string):
        self.queue.put(string)
    def flush(self): pass

class EriAmoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EriAmo Union v8.6 [SAFE EXIT]")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f0f0f")
        self.msg_queue = queue.Queue()
        self.is_closing = False
        
        self.init_backend()
        self.create_widgets()
        
        sys.stdout = ConsoleRedirector(self.msg_queue)
        self.root.after(100, self.update_loop)
        
        print(f"{Colors.CYAN}🌌 System gotowy.{Colors.RESET}")

    def init_backend(self):
        try:
            self.union = EriAmoUnion(verbose=True)
            self.agency = MultimodalAgency(self.union, verbose=True)
            self.agency.start()
            self.union.start()
        except Exception as e:
            print(f"Błąd backendu: {e}")

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        main_split = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_split.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_split)
        main_split.add(left_frame, weight=3)

        self.console_log = scrolledtext.ScrolledText(left_frame, bg="#050505", fg="#ddd", font=("Consolas", 11))
        self.console_log.pack(fill=tk.BOTH, expand=True)
        self.console_log.tag_config("USER", foreground="#ffff00")

        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X)
        
        self.entry = tk.Entry(input_frame, bg="#222", fg="#fff", font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.entry.bind("<Return>", self.send_command)
        
        tk.Button(input_frame, text="WYŚLIJ", command=self.send_command, bg="#333", fg="white").pack(side=tk.RIGHT)

        right_frame = ttk.Frame(main_split)
        main_split.add(right_frame, weight=1)
        self.stats_text = tk.Text(right_frame, bg="#111", fg="#0f0", height=20, width=30)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

    def send_command(self, event=None):
        cmd = self.entry.get().strip()
        if not cmd: return
        self.entry.delete(0, tk.END)
        
        self.append_text(f"\nTy > {cmd}\n", "USER")

        # Obsługa komendy wyjścia w czacie
        if cmd.lower() in ['exit', 'quit', '/exit', '/quit']:
            self.on_closing()
            return
        
        threading.Thread(target=self._process_command_thread, args=(cmd,), daemon=True).start()

    def _process_command_thread(self, cmd):
        if self.is_closing: return
        if hasattr(self.agency, 'stimulate'): self.agency.stimulate(cmd)
        response = self.union.process_input(cmd)
        if response: print(f" [EriAmo] {response}")

    def update_loop(self):
        while not self.msg_queue.empty():
            msg = self.msg_queue.get_nowait()
            self.append_text(msg)
        
        if not self.is_closing:
            try:
                intro = self.union.aii.introspect()
                self.stats_text.delete('1.0', tk.END)
                self.stats_text.insert('1.0', f"{intro}\n\n")
            except: pass
        
        self.root.after(100, self.update_loop)

    def append_text(self, text, tag=None):
        self.console_log.insert(tk.END, text, tag)
        self.console_log.see(tk.END)

    def on_closing(self):
        """Bezpieczne zamykanie."""
        if self.is_closing: return # Zapobiega podwójnemu kliknięciu
        self.is_closing = True
        
        # Wymuszamy komunikat w oknie
        self.console_log.insert(tk.END, "\n\n[SYSTEM] ZAMYKANIE... NIE WYŁĄCZAJ OKNA.\n")
        self.console_log.see(tk.END)
        self.root.update() # Odśwież widok, żeby użytkownik zobaczył napis
        
        # Zatrzymanie i zapis (to wywoła printy z union_core)
        self.agency.stop()
        self.union.stop()
        
        # Krótka pauza, żebyś zdążył przeczytać logi zapisu
        self.root.after(2000, self.real_destroy)

    def real_destroy(self):
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = EriAmoGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()