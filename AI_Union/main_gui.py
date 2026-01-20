# main_gui_union.py
# -*- coding: utf-8 -*-
"""
EriAmo Union GUI v1.0
- Pełna integracja z EriAmoUnion (Language + Music + Agency)
- Zakładka Czat do rozmowy z systemem
- Współdzielony stan emocjonalny (Agencja wpływa na muzykę i odwrotnie)
"""
import re 
import customtkinter as ctk
# ... reszta importów
import customtkinter as ctk
import threading
import queue
import os
import sys
import io
import contextlib

# WAŻNE: Ustawienie backendu matplotlib PRZED importem
import matplotlib
matplotlib.use('Agg')

# Importy Union
from union_core import EriAmoUnion
from amocore import AXES_LIST, EPHEMERAL_AXES
from music_analyzer import MusicAnalyzer
from data_loader import ExternalKnowledgeLoader
from genre_definitions import list_genres

# Dark mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class EriAmoBrain(threading.Thread):
    """
    Mózg operacyjny (Backend).
    Obsługuje zarówno muzykę, jak i interakcje językowe Union.
    """
    
    def __init__(self, union_instance, cmd_queue, resp_queue):
        super().__init__(daemon=True)
        self.union = union_instance
        self.cmd_queue = cmd_queue
        self.resp_queue = resp_queue
        self.running = True
        
        # Pobieramy podsystemy z Union
        self.core = self.union.music_core
        self.logger = self.union.music_logger
        self.composer = self.union.music_composer
        
        # Lazy initialization
        self.analyzer = MusicAnalyzer(self.core, self.logger) if self.core else None
        self.loader = None
        self.visualizer = None

    def _get_loader(self):
        if self.loader is None:
            self.loader = ExternalKnowledgeLoader()
        return self.loader

    def _get_visualizer(self):
        if self.visualizer is None:
            from visualizer import SoulVisualizerV59
            self.visualizer = SoulVisualizerV59()
        return self.visualizer

    def run(self):
        self.resp_queue.put({"status": "LOG", "msg": "[SYSTEM] Wątek Union Brain: Aktywny"})
        
        while self.running:
            try:
                task = self.cmd_queue.get(timeout=0.5)
                cmd_type = task['type']
                
                if cmd_type == 'STOP':
                    self.running = False
                    break
                
                elif cmd_type == 'CHAT':
                    self._handle_chat(task)

                elif cmd_type == 'ANALYZE':
                    self._handle_analyze(task)
                
                elif cmd_type == 'COMPOSE':
                    self._handle_compose(task)
                
                elif cmd_type == 'REPORT':
                    self._handle_report()
                
                elif cmd_type == 'DECAY':
                    # Union może mieć własne mechanizmy, ale tu wymuszamy decay muzyczny
                    cycles = task.get('cycles', 1)
                    if self.core:
                        self.core.apply_emotion_decay(cycles)
                        self.resp_queue.put({"status": "LOG", "msg": f"Wygaszanie (Core): {cycles} cykli"})
                
                # Zawsze aktualizuj stan po operacji
                self.send_soul_update()
                
            except queue.Empty:
                continue
            except Exception as e:
                import traceback
                self.resp_queue.put({
                    "status": "ERROR", 
                    "msg": f"Błąd krytyczny: {e}\n{traceback.format_exc()}"
                })

    def _handle_chat(self, task):
        """Obsługa czatu z Union (przechwytywanie stdout)."""
        text = task['text']
        self.resp_queue.put({"status": "CHAT_USER", "msg": text})
        
        # Przechwytujemy to, co Union wypisuje do konsoli (printy)
        f = io.StringIO()
        try:
            with contextlib.redirect_stdout(f):
                self.union.process_input(text)
            
            output = f.getvalue()
            self.resp_queue.put({"status": "CHAT_BOT", "msg": output})
            
        except Exception as e:
            self.resp_queue.put({"status": "ERROR", "msg": f"Błąd Union: {e}"})

    def _handle_analyze(self, task):
        if not self.core:
            self.resp_queue.put({"status": "ERROR", "msg": "Brak rdzenia muzycznego w Union!"})
            return

        title = task['title']
        features = list(task['features'])
        
        if task.get('artist'):
            try:
                loader = self._get_loader()
                web_features = loader.get_context_from_web(task['artist'], title)
                features.extend(web_features)
            except Exception as e:
                self.resp_queue.put({"status": "LOG", "msg": f"Web Loader: {e}"})
        
        mode = "!teach" if task['mode'] == 'full' else "!simulate"
        self.analyzer.analyze_and_shift(features, title, mode=mode)
        self.resp_queue.put({"status": "LOG", "msg": f"Analiza zakończona: {title}"})

    def _handle_compose(self, task):
        if not self.composer:
            self.resp_queue.put({"status": "ERROR", "msg": "Brak kompozytora w Union!"})
            return

        genre = task['genre']
        instrument = task.get('instrument', None)
        try:
            paths = self.composer.compose_new_work(genre, instrument_override=instrument)
            self.resp_queue.put({
                "status": "SUCCESS", 
                "msg": f"Skomponowano {genre}!", 
                "data": paths
            })
        except Exception as e:
            self.resp_queue.put({"status": "ERROR", "msg": str(e)})

    def _handle_report(self):
        try:
            vis = self._get_visualizer()
            paths = vis.create_complete_report()
            self.resp_queue.put({"status": "REPORT_READY", "paths": paths})
        except Exception as e:
            self.resp_queue.put({"status": "ERROR", "msg": f"Raport: {e}"})

    def send_soul_update(self):
        """Wysyła stan rdzenia muzycznego."""
        if not self.core: return
        try:
            vec = self.core.get_vector_copy()
            vector_dict = {AXES_LIST[i]: vec[i] for i in range(len(AXES_LIST))}
            # decay_status = self.core.get_decay_status() # Jeśli metoda istnieje
            self.resp_queue.put({
                "status": "UPDATE_VECTORS", 
                "data": vector_dict
            })
        except Exception:
            pass


class EriAmoApp(ctk.CTk):
    """Główne okno aplikacji (Union Edition)."""
    
    def __init__(self):
        super().__init__()
        
        self.title("EriAmo Union v1.7 - Integrated Interface")
        self.geometry("1200x800")
        
        self.cmd_queue = queue.Queue()
        self.resp_queue = queue.Queue()
        
        # --- INICJALIZACJA UNION ---
        print("Uruchamianie EriAmo Union...")
        self.union = EriAmoUnion(verbose=True, use_unified_memory=True)
        self.union.start() # Uruchamia wątki agencji
        
        # Start wątku GUI Brain
        self.brain = EriAmoBrain(self.union, self.cmd_queue, self.resp_queue)
        self.brain.start()
        
        self._init_ui()
        
        self._gui_loop_id = None
        self._start_gui_loop()
        
        # Początkowy update
        self.after(500, lambda: self.brain.send_soul_update())

    def _init_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self):
        self.frame_left = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_left.grid_propagate(False)
        
        lbl_logo = ctk.CTkLabel(self.frame_left, text="ERIAMO UNION", font=ctk.CTkFont(size=22, weight="bold"))
        lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        lbl_ver = ctk.CTkLabel(self.frame_left, text=f"Core v{self.union.VERSION}", text_color="gray")
        lbl_ver.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        self.vector_bars = {}
        self.vector_labels = {}
        
        # Generowanie pasków
        for i, axis in enumerate(AXES_LIST):
            prefix = "[E]" if axis in EPHEMERAL_AXES else "[T]"
            
            lbl = ctk.CTkLabel(self.frame_left, text=f"{prefix} {axis.upper()}: 0.0", anchor="w", font=ctk.CTkFont(size=11))
            lbl.grid(row=i*2+2, column=0, padx=20, pady=(5, 0), sticky="w")
            
            pbar = ctk.CTkProgressBar(self.frame_left, width=220, height=12)
            pbar.grid(row=i*2+3, column=0, padx=20, pady=(2, 5))
            pbar.set(0.5)
            
            # Kolorowanie
            if axis in EPHEMERAL_AXES: pbar.configure(progress_color="#95a5a6")
            elif axis == 'affections': pbar.configure(progress_color="#9b59b6")
            elif axis == 'etyka': pbar.configure(progress_color="#27ae60")
            elif axis in ['logika', 'wiedza']: pbar.configure(progress_color="#3498db")
            else: pbar.configure(progress_color="#e67e22")
            
            self.vector_bars[axis] = pbar
            self.vector_labels[axis] = lbl
        
        btn_decay = ctk.CTkButton(self.frame_left, text="Wygas emocje (Decay)", command=self._send_decay, fg_color="#34495e")
        btn_decay.grid(row=len(AXES_LIST)*2+4, column=0, padx=20, pady=(30, 10))

    def _build_right_panel(self):
        self.frame_right = ctk.CTkFrame(self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        
        self.tabview = ctk.CTkTabview(self.frame_right)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_chat = self.tabview.add("CZAT (UNION)")
        self.tab_analyze = self.tabview.add("NAUKA")
        self.tab_compose = self.tabview.add("KOMPOZYCJA")
        self.tab_logs = self.tabview.add("SYSTEM LOG")
        
        self._setup_chat_tab()
        self._setup_analyze_tab()
        self._setup_compose_tab()
        self._setup_logs_tab()

    def _setup_chat_tab(self):
        """Zakładka czatu z Union."""
        self.chat_display = ctk.CTkTextbox(self.tab_chat, font=ctk.CTkFont(size=12))
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_display.configure(state="disabled")
        
        input_frame = ctk.CTkFrame(self.tab_chat, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.chat_entry = ctk.CTkEntry(input_frame, placeholder_text="Napisz coś do Union...", height=40)
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", lambda event: self._send_chat())
        
        btn_send = ctk.CTkButton(input_frame, text="Wyślij", width=100, height=40, command=self._send_chat)
        btn_send.pack(side="right")

    def _setup_analyze_tab(self):
        frame = ctk.CTkFrame(self.tab_analyze, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Analiza Muzyczna (Wpływ na Union)", font=ctk.CTkFont(size=16)).pack(pady=10)
        
        self.entry_artist = ctk.CTkEntry(frame, placeholder_text="Artysta")
        self.entry_artist.pack(pady=5, fill="x")
        
        self.entry_title = ctk.CTkEntry(frame, placeholder_text="Tytuł utworu")
        self.entry_title.pack(pady=5, fill="x")
        
        self.entry_features = ctk.CTkEntry(frame, placeholder_text="Cechy (np. HEAVY ADAGIO)")
        self.entry_features.pack(pady=5, fill="x")
        
        btn_box = ctk.CTkFrame(frame, fg_color="transparent")
        btn_box.pack(pady=20)
        
        ctk.CTkButton(btn_box, text="[T] NAUCZ (Trwałe)", command=lambda: self._send_analyze('full'), 
                      fg_color="#9b59b6", width=200).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_box, text="[E] SYMULACJA", command=lambda: self._send_analyze('sim'), 
                      fg_color="transparent", border_width=2, width=150).pack(side="left", padx=10)

    def _setup_compose_tab(self):
        frame = ctk.CTkFrame(self.tab_compose, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Kompozytor Duszowy", font=ctk.CTkFont(size=16)).pack(pady=10)
        
        self.genre_var = ctk.StringVar(value="BLUES")
        self.combo_genre = ctk.CTkComboBox(frame, values=list_genres(), variable=self.genre_var)
        self.combo_genre.pack(pady=10)
        
        self.instrument_var = ctk.StringVar(value="Auto")
        instruments = ["Auto", "PIANO", "ORGAN", "GUITAR", "DISTORTION", "BASS", "STRINGS", "CHOIR", "SAX", "FLUTE", "PAD", "SITAR"]
        self.combo_instr = ctk.CTkComboBox(frame, values=instruments, variable=self.instrument_var)
        self.combo_instr.pack(pady=10)
        
        ctk.CTkButton(frame, text="KOMPONUJ", command=self._send_compose, 
                      height=50, font=ctk.CTkFont(weight="bold"), fg_color="#e67e22").pack(pady=30)
        
        ctk.CTkButton(frame, text="Generuj Raport PDF/HTML", command=self._send_report).pack(pady=10)

    def _setup_logs_tab(self):
        self.textbox_log = ctk.CTkTextbox(self.tab_logs, font=ctk.CTkFont(family="Consolas", size=11))
        self.textbox_log.pack(fill="both", expand=True, padx=10, pady=10)

    # === LOGIKA ===
    
    def _start_gui_loop(self):
        self._process_responses()
        self._gui_loop_id = self.after(100, self._start_gui_loop)

    def _process_responses(self):
        try:
            while True:
                msg = self.resp_queue.get_nowait()
                self._handle_message(msg)
        except queue.Empty:
            pass

    def _handle_message(self, msg):
        status = msg.get('status')
        
        if status == "UPDATE_VECTORS":
            self._update_vectors(msg['data'])
            
        elif status == "CHAT_USER":
            # Wyświetlamy wiadomość użytkownika
            self._append_chat(f"Ty: {msg['msg']}\n", "gray")
            
        elif status == "CHAT_BOT":
            raw_text = msg['msg']
            
            # 1. Usuwanie kodów ANSI (np. [97m, [0m)
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            clean_text = ansi_escape.sub('', raw_text)
            
            # 2. Usuwanie znacznika [USER] >> jeśli się powtarza w logach
            clean_text = clean_text.replace("[USER] >>", "").strip()
            
            # 3. Wyświetlenie czystego tekstu w oknie
            if clean_text:
                self._append_chat(f"Union:\n{clean_text}\n\n", "white")
            
            # 4. Logowanie surowej wersji (z kolorami) do zakładki "SYSTEM LOG"
            #    (tam kody też będą widoczne jako tekst, ale to log techniczny)
            self._log(f"[CHAT] Otrzymano odpowiedź ({len(clean_text)} znaków)")
            
        elif status in ["LOG", "SUCCESS", "ERROR"]:
            prefix = "[OK]" if status == "SUCCESS" else ("[ERR]" if status == "ERROR" else "[INFO]")
            self._log(f"{prefix} {msg['msg']}")
            
        elif status == "REPORT_READY":
            self._log(f"[RAPORT] Wygenerowano: {msg.get('paths')}")
            import webbrowser
            if msg.get('paths', {}).get('basic'):
                webbrowser.open('file://' + os.path.abspath(msg['paths']['basic']))

    def _update_vectors(self, data):
        for axis, val in data.items():
            if axis in self.vector_bars:
                norm = 0.5 + (val / 60.0)
                norm = max(0.0, min(1.0, norm))
                self.vector_bars[axis].set(norm)
                prefix = "[E]" if axis in EPHEMERAL_AXES else "[T]"
                self.vector_labels[axis].configure(text=f"{prefix} {axis.upper()}: {val:+.1f}")

    def _append_chat(self, text, color):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text) # Można dodać tagi kolorów w przyszłości
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _log(self, text):
        self.textbox_log.insert("end", f"{text}\n")
        self.textbox_log.see("end")

    # === WYSYŁANIE ===
    
    def _send_chat(self):
        text = self.chat_entry.get().strip()
        if not text: return
        self.chat_entry.delete(0, "end")
        self.cmd_queue.put({'type': 'CHAT', 'text': text})

    def _send_analyze(self, mode):
        self.cmd_queue.put({
            'type': 'ANALYZE',
            'title': self.entry_title.get(),
            'artist': self.entry_artist.get(),
            'features': self.entry_features.get().split(),
            'mode': mode
        })

    def _send_compose(self):
        instr = self.instrument_var.get()
        self.cmd_queue.put({
            'type': 'COMPOSE',
            'genre': self.genre_var.get(),
            'instrument': None if instr == "Auto" else instr
        })

    def _send_report(self):
        self.cmd_queue.put({'type': 'REPORT'})

    def _send_decay(self):
        self.cmd_queue.put({'type': 'DECAY'})

    def on_closing(self):
        if self.union:
            self.union.stop() # Bezpieczne zamknięcie Union
        self.cmd_queue.put({'type': 'STOP'})
        self.destroy()

if __name__ == "__main__":
    app = EriAmoApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.on_closing()