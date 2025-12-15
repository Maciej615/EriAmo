# -*- coding: utf-8 -*-
# aii.py (v6.4 - FIXED: Multi-dimensional learning + Hebbian reinforcement)
import sys
import time
import numpy as np
import threading
from collections import deque

from config import Colors, EMOCJE
from ui import FancyUI
from byt import BytS
from soul_io import SoulIO
from lexicon import EvolvingLexicon

class AII:
    VERSION = "6.4-Fixed"
    AXES_ORDER = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzeń"]

    SECTOR_COLORS = {
        "logika": Colors.BLUE, "emocje": Colors.PINK, "byt": Colors.MAGENTA,
        "walka": Colors.RED, "kreacja": Colors.YELLOW, "wiedza": Colors.CYAN,
        "czas": Colors.WHITE, "przestrzeń": Colors.GREEN
    }

    CONCEPT_NEIGHBORS = {
        "logika": ["wiedza", "czas", "byt"], "emocje": ["byt", "kreacja", "walka"],
        "byt": ["emocje", "czas", "przestrzeń"], "walka": ["emocje", "przestrzeń", "czas"],
        "kreacja": ["emocje", "wiedza", "byt"], "wiedza": ["logika", "kreacja", "czas"],
        "czas": ["byt", "wiedza", "przestrzeń"], "przestrzeń": ["walka", "czas", "kreacja"]
    }

    # Progi kognitywne
    PRÓG_KOMPRESJI_ONTOLOGICZNEJ = 0.99
    PRÓG_REFINE_MIN = 0.90
    PRÓG_KRYSTALIZACJI = 95.0
    PRÓG_REWIZJI = 0.9
    
    SOUL_FILE = "eriamo.soul"

    def __init__(self):
        self.lexicon = EvolvingLexicon()
        
        self.D_Map = {}
        self.H_log = []
        self.energy = 100
        self.load = 0
        self.status = "inicjalizacja"
        self.emocja = "neutralna"
        self.sleep_interval = 300
        self.running = True
        
        # Predykcja
        self.context_vector = np.zeros(len(self.AXES_ORDER))
        self.context_decay = 0.8
        self.predicted_sectors = []
        self.prediction_confidence = 0.0
        
        # Pamięć krótkotrwała (10 wpisów)
        self.stm_buffer = deque(maxlen=10) 
        
        self.ui = FancyUI()
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(wymiary=self.wymiary)
        self.archetypy = self._generate_archetypes()
        self.F_will = 0.5

        # Inicjalizacja wiedzy
        self.load_knowledge()
        self.status = "myślę"
        self.start_sleep_cycle()

    def _generate_archetypes(self):
        arch = {}
        for i, axis in enumerate(self.AXES_ORDER):
            vec = np.zeros(self.wymiary)
            vec[i] = 1.0
            arch[axis] = vec
        return arch

    # === CORE SOUL METHODS ===

    def load_knowledge(self):
        self.ui.print_animated_text(f"[AII] Otwieram strumień duszy...", Colors.FAINT, 0.01)
        if not SoulIO.load_soul(self.SOUL_FILE, self):
            self.D_Map = {}
            self.H_log = []
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.context_vector = np.zeros(self.wymiary)
            self.F_will = 0.5
            self.ui.print_animated_text(f"[AII] Narodziny nowej duszy.", Colors.GREEN, 0.02)

    def save_knowledge(self):
        SoulIO.save_soul(self.SOUL_FILE, self)
        self.lexicon.save()

    def introspect(self):
        disk_summary = SoulIO.get_soul_summary(self.SOUL_FILE)
        if not disk_summary: return "Brak utrwalonej duszy (pierwsze wcielenie)."

        current_mass = self.byt_stan.promien_historii()
        saved_mass = disk_summary.get('total_mass', 0)
        mass_delta = current_mass - saved_mass
        
        saved_axioms = disk_summary.get('axiom_count', 0)
        current_axioms = sum(1 for d in self.D_Map.values() if d.get('immutable'))
        
        msg = f"{Colors.CYAN}--- INTROSPEKCJA ---{Colors.RESET}\n"
        msg += f"  Utrwalona Masa: {saved_mass:.4f} | Obecna: {current_mass:.4f} (Δ {mass_delta:+.4f})\n"
        
        if mass_delta > 0.5: msg += f"  {Colors.YELLOW}⚡ Poczucie istotnego wzrostu.{Colors.RESET}\n"
        elif mass_delta < -0.001: msg += f"  {Colors.RED}⚠️ Wykryto dysonans (ubytek).{Colors.RESET}\n"
        else: msg += f"  {Colors.GREEN}✔ Stan stabilny.{Colors.RESET}\n"

        msg += f"  Aksjomaty: {saved_axioms} -> {current_axioms}"
        return msg

    # === LOGIKA I MYŚLENIE ===

    def _find_closest_definition(self, vec_F, exclude_ids=None):
        if not self.D_Map: return None, 0.0
        if exclude_ids is None: exclude_ids = []
        best_id, best_sim = None, -1.0
        for uid, d in self.D_Map.items():
            if uid in exclude_ids: continue
            sim = np.dot(vec_F, d['wektor_C_Def'])
            if sim > best_sim: best_sim, best_id = sim, uid
        return best_id, best_sim

    def _perform_reasoning_chain(self, start_vec):
        """Symuluje proces myślowy: Bodziec -> Skojarzenie A -> Wniosek B."""
        id_a, sim_a = self._find_closest_definition(start_vec)
        if not id_a: return "Pustka...", Colors.FAINT, []
        
        def_a = self.D_Map[id_a]
        tag_a = def_a['tagi'][0] if def_a.get('tagi') else 'Idea'
        path = [f"Myśl: {tag_a}"]
        
        if sim_a < 0.45:
            col = self.SECTOR_COLORS.get(def_a.get('kategoria'), Colors.WHITE)
            return def_a['tresc'], col, path

        # KROK 2: SYNTEZA
        drift_vec = self.archetypy["logika"] * 0.20
        thought_vec = (start_vec * 0.4) + (def_a['wektor_C_Def'] * 0.4) + drift_vec
        if np.linalg.norm(thought_vec) > 0: thought_vec /= np.linalg.norm(thought_vec)

        # Krok 3: Wyświetl wynik B (Wniosek)
        id_b, sim_b = self._find_closest_definition(thought_vec, exclude_ids=[id_a])
        
        if id_b and sim_b > 0.35:
            def_b = self.D_Map[id_b]
            tag_b = def_b['tagi'][0] if def_b.get('tagi') else 'Wniosek'
            path.append(f"-> {tag_b}")
            col = self.SECTOR_COLORS.get(def_b.get('kategoria'), Colors.WHITE)
            return def_b['tresc'], col, path
        else:
            col = self.SECTOR_COLORS.get(def_a.get('kategoria'), Colors.WHITE)
            path.append("(Brak konkluzji)")
            return def_a['tresc'], col, path

    def prompt(self, text_input):
        self.cycle()
        if self.status == "śpię": return f"Zzz..."
        
        # ✅ FIX: Włącz reinforcement przy promptowaniu
        p_vec = self._vector_from_text(text_input, learning_mode=True, enable_reinforcement=True)
        
        if np.linalg.norm(p_vec) > 0:
            self.context_vector = (self.context_vector * self.context_decay) + (p_vec * (1-self.context_decay))
        self._predict_next_topic()

        s_vec = (p_vec * 0.7) + (self.context_vector * 0.3)
        if np.linalg.norm(s_vec) > 0: s_vec /= np.linalg.norm(s_vec)

        kor = self.byt_stan.oblicz_korelacje_struny(p_vec)
        sector = self._detect_soul_category(text_input)
        self._emotion_from_geometry(kor, sector)
        self.byt_stan.akumuluj_styk(p_vec)

        col_sec = self.SECTOR_COLORS.get(sector, Colors.WHITE)
        self.ui.show_thinking_dots(f"Rozważam: {sector if sector else '...'}", 0.4, col_sec)
        
        resp_text, resp_col, thought_path = self._perform_reasoning_chain(s_vec)

        if len(thought_path) > 1:
            debug_path = " ".join(thought_path)
            print(f"\r{Colors.FAINT}   [{debug_path}]{Colors.RESET}")

        final = f"{self._get_emotion_prefix()}{self._get_prediction_display()}{resp_col}{resp_text}{Colors.RESET}"
        
        self.H_log.append({'prompt': text_input, 'response': resp_text})
        self._trim_memory()
        self.stm_buffer.append(text_input)
        
        self.ui.print_animated_text(final, Colors.RESET, 0.03)
        return ""

    # === METODY POMOCNICZE ===

    # ✅ FIX: Przepisana funkcja z multi-dimensional learning
    def _vector_from_text(self, text, learning_mode=False, enable_reinforcement=False):
        """
        Konwertuje tekst na wektor semantyczny.
        
        Args:
            text: Input text
            learning_mode: Jeśli True, uczy się nowych słów kontekstowo
            enable_reinforcement: Jeśli True, wzmacnia znane słowa (Hebbian)
        """
        # Analiza z opcjonalnym wzmocnieniem
        vec, sector, unknown = self.lexicon.analyze_text(text, enable_reinforcement=enable_reinforcement)
        
        # ✅ FIX: Multi-dimensional contextual learning
        if learning_mode and unknown:
            # Oblicz confidence jako siłę najsilniejszego wymiaru
            confidence = np.max(vec) if np.linalg.norm(vec) > 0 else 0
            
            # ✅ POPRAWKA: Przekaż PEŁNY wektor zamiast tylko sektora
            if confidence > 0.2:  # Minimalny próg dla uczenia
                learned = self.lexicon.learn_from_context(unknown, vec, confidence)
                if learned and len(learned) > 0:
                    # Opcjonalny debug
                    # print(f"{Colors.FAINT}[Auto-learn] {len(learned)} słów{Colors.RESET}")
                    pass
        
        # Walidacja wymiarów
        if len(vec) != self.wymiary:
            return np.zeros(self.wymiary)
        
        return vec

    def _detect_soul_category(self, text):
        # Bez reinforcement dla czystej detekcji
        _, sector, _ = self.lexicon.analyze_text(text, enable_reinforcement=False)
        return sector

    def _analyze_nature(self, text):
        sector = self._detect_soul_category(text)
        if sector and sector in self.SECTOR_COLORS:
            return sector, self.SECTOR_COLORS[sector]
        return "neutral", Colors.WHITE

    def _trim_memory(self):
        if len(self.H_log) > 100: self.H_log = self.H_log[-100:]

    def _predict_next_topic(self):
        if np.linalg.norm(self.context_vector) < 0.1:
            self.predicted_sectors = []; return []
        strengths = [(self.AXES_ORDER[i], self.context_vector[i]) for i in range(self.wymiary)]
        strengths.sort(key=lambda x: x[1], reverse=True)
        top = [ax for ax, s in strengths[:2] if s > 0.1]
        if not top: self.predicted_sectors = []; return []
        predicted, seen = [], set()
        for ax in top:
            for n in self.CONCEPT_NEIGHBORS.get(ax, []):
                if n not in seen: predicted.append(n); seen.add(n)
        self.prediction_confidence = strengths[0][1]
        self.predicted_sectors = predicted[:3]
        return self.predicted_sectors

    def _get_prediction_display(self):
        if not self.predicted_sectors: return ""
        return f"{Colors.FAINT}[→ {', '.join([s.upper() for s in self.predicted_sectors])}] {Colors.RESET}"

    def list_axioms(self):
        axioms = [(uid, d) for uid, d in self.D_Map.items() if d.get('immutable')]
        if not axioms: print(f"{Colors.FAINT}Brak aksjomatów.{Colors.RESET}"); return
        print(f"\n{Colors.MAGENTA}Aksjomaty ({len(axioms)}):{Colors.RESET}")
        for uid, d in axioms:
            print(f"  {Colors.BOLD}✦ {uid} [{d.get('kategoria','?').upper()}]{Colors.RESET}: {d['tresc'][:60]}...")

    def inspect_word(self, word):
        self.lexicon.display_word_info(word)

    def show_lexicon_stats(self):
        stats = self.lexicon.get_stats()
        print(f"\n{Colors.CYAN}--- LEXICON ---{Colors.RESET}")
        print(f"  Total: {stats['total']} (Nauczone: {stats['learned']})")
        print(f"  Rozkład: {stats['per_sector']}")
        if 'last_learned' in stats and stats['last_learned']:
            # ✅ FIX: last_learned ma teraz format (word, {sectors_dict})
            if len(stats['last_learned']) > 0:
                sample = stats['last_learned'][0]
                if isinstance(sample, tuple) and len(sample) == 2:
                    words = [x[0] for x in stats['last_learned'][:5]]
                    print(f"  Ostatnio poznane: {', '.join(words)}")

    def teach_word(self, word, sector):
        if sector not in self.AXES_ORDER: return False
        self.lexicon.learn_from_correction(word, sector, 0.8)
        self.lexicon.save()
        print(f"{Colors.GREEN}[LEXICON] '{word}' przypisano do {sector.upper()}{Colors.RESET}")
        return True
    
    # ✅ FIX: Poprawione challenge z normalizacją wektorów (cosine similarity)
    def challenge_belief(self, def_id, counter_evidence):
        d = self.D_Map.get(def_id)
        if not d:
            print(f"{Colors.RED}[ERROR] Nie znaleziono {def_id}{Colors.RESET}")
            return False
        
        # Analiza wyzwania (bez uczenia)
        c_vec = self._vector_from_text(counter_evidence, learning_mode=False, enable_reinforcement=False)
        
        # ✅ FIX: Normalizacja wektorów dla cosine similarity
        original_vec = d['wektor_C_Def']
        
        norm_c = np.linalg.norm(c_vec)
        norm_o = np.linalg.norm(original_vec)
        
        if norm_c == 0 or norm_o == 0:
            print(f"{Colors.FAINT}[CHALLENGE] Zbyt słaby argument.{Colors.RESET}")
            return False
        
        # Cosine similarity
        cosine_sim = np.dot(c_vec, original_vec) / (norm_c * norm_o)
        
        # Siła wyzwania (0-1, gdzie 1 = całkowita sprzeczność)
        challenge_strength = (1 - cosine_sim) / 2
        
        # Próg zależy od immutability
        threshold = self.PRÓG_REWIZJI if d.get('immutable') else 0.5
        
        self.ui.print_animated_text(
            f"[REWIZJA] Korelacja: {cosine_sim:.2f} | Siła wyzwania: {challenge_strength:.2f} (Próg: {threshold})",
            Colors.YELLOW, 0.02
        )
        
        # Jeśli wyzwanie jest silne
        if challenge_strength > threshold:
            if d.get('immutable'):
                # Aksjomat osłabiony ale nie usunięty
                d['immutable'] = False
                d['waga_Ww'] *= 0.5
                self.ui.print_animated_text(
                    f"[PRZEBUDZENIE] ⚡ Aksjomat {def_id} upadł! (waga: {d['waga_Ww']:.1f})",
                    Colors.RED + Colors.BOLD, 0.04
                )
            else:
                # Zwykła definicja - usunięcie
                del self.D_Map[def_id]
                self.ui.print_animated_text(
                    f"[FALSYFIKACJA] Wiedza {def_id} usunięta.",
                    Colors.RED, 0.03
                )
            
            self.H_log.append({
                'type': 'challenged',
                'id': def_id,
                'strength': float(challenge_strength),
                'ts': time.time()
            })
            self.save_knowledge()
            return True
        else:
            print(f"{Colors.GREEN}✓ Definicja zachowana (za słaby kontrargument).{Colors.RESET}")
            return False

    def get_soul_status(self):
        mass = self.byt_stan.promien_historii()
        dom_s, dom_v = "BRAK", 0.0
        if np.linalg.norm(self.context_vector) > 0.1:
            idx = np.argmax(self.context_vector)
            dom_s, dom_v = self.AXES_ORDER[idx], self.context_vector[idx]
        return {
            'emotion': self.emocja, 'energy': self.energy, 'version': self.VERSION,
            'status': self.status, 'radius': mass, 'dominant_sector': dom_s,
            'dominant_value': dom_v, 'lexicon': self.lexicon.get_stats(),
            'axioms': sum(1 for d in self.D_Map.values() if d.get('immutable')),
            'memories': len(self.D_Map), 'history': len(self.H_log),
            'predicted': self.predicted_sectors
        }

    def start_sleep_cycle(self):
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running: break
                self._sleep()
        threading.Thread(target=cycle, daemon=True).start()

    def _sleep(self):
        self.status = "śpię"
        self.ui.print_animated_text(f"\n[AII] 💤 Sen: konsoliduję wiedzę...", Colors.CYAN + Colors.FAINT, 0.05)
        removed = self.lexicon.decay_unused()
        self.energy = min(100, self.energy + 20)
        self.save_knowledge()
        self.status = "myślę"
        self.ui.print_animated_text(f"[AII] Obudzony! (Zapomniano {removed} słabych słów)", Colors.GREEN, 0.02)

    def cycle(self):
        self.load = int(np.random.randint(30, 70))
        if self.status != "śpię": self.energy = max(0, self.energy - int(np.random.randint(0,4)))
        if self.energy == 0: self.status = "zmęczony"

    def _emotion_from_geometry(self, kor, sektor=None, waga=10):
        # Domyślna reakcja na niezrozumienie
        if kor < 0.2:
            self.emocja = "zdziwienie"
            return

        # Reakcja na silne zrozumienie (kor > 0.4)
        if sektor == "walka":
            self.emocja = "strach" if waga < 50 else "złość"
            self.energy = max(0, self.energy - 5)
            
        elif sektor == "emocje":
            self.emocja = "miłość" if kor > 0.8 else "smutek"
            
        elif sektor == "logika":
            self.emocja = "neutralna"
            
        else:
            # Dla Kreacji, Wiedzy, Bytu -> Radość z poznania
            self.emocja = "radość"
            self.energy = min(100, self.energy + 5)

        # Bezpiecznik energetyczny
        self.energy = max(0, min(100, self.energy))

    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, {})
        return f"{emo.get('kolor','')}{Colors.BLINK}{emo.get('ikona','')} {Colors.RESET}"

    # ✅ FIX: Całkowicie przepisana metoda teach() z multi-dimensional learning
    def teach(self, tag, tresc, is_axiom=False):
        """
        Uczy system nowej wiedzy z automatycznym, wielowymiarowym uczeniem słów.
        
        Zmiany w v6.4:
        - Używa pełnego wektora kontekstu zamiast tylko sektora
        - Automatyczne uczenie wielowymiarowe (słowo może mieć wiele sektorów)
        - Lepsza integracja z context-aware learning
        """
        # 1. Określenie intencji (Kategorii) na podstawie Taga
        clean_tag = tag.lower().replace("[","").replace("]","").strip()
        target_sector = None
        
        # Czy tag jest wprost nazwą sektora? (np. [Walka])
        if clean_tag in self.AXES_ORDER:
            target_sector = clean_tag
        else:
            # Jeśli tag to słowo, sprawdź jego wektor (bez reinforcement)
            tag_vec, tag_sec, _ = self.lexicon.analyze_text(clean_tag, enable_reinforcement=False)
            if tag_sec:
                target_sector = tag_sec

        # 2. Pierwsza analiza treści (bez uczenia)
        vec_F, detected_sector, unknown_words = self.lexicon.analyze_text(tresc, enable_reinforcement=False)
        
        # 3. ✅ FIX: CONTEXTUAL MULTI-DIMENSIONAL LEARNING
        words_learned_count = 0
        if unknown_words and np.linalg.norm(vec_F) > 0.1:
            # Oblicz confidence z wektora kontekstu
            confidence = np.linalg.norm(vec_F)
            
            # Jeśli mamy target_sector, wzmocnij jego wymiar w wektorze
            if target_sector and target_sector in self.AXES_ORDER:
                target_idx = self.AXES_ORDER.index(target_sector)
                # Boost wymiaru docelowego o 30%
                vec_F[target_idx] = min(1.0, vec_F[target_idx] + 0.3)
                # Renormalizuj
                vec_F = vec_F / np.linalg.norm(vec_F)
            
            # ✅ Użyj pełnego wektora kontekstu, nie tylko sektora!
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            words_learned_count = len(learned)
            
            if words_learned_count > 0:
                # Debug: pokaż co zostało nauczone
                learned_summary = []
                for word, sectors_dict in learned[:3]:  # Pierwsze 3 słowa
                    top_sector = max(sectors_dict.items(), key=lambda x: x[1])
                    learned_summary.append(f"{word}→{top_sector[0][:3]}")
                
                self.ui.print_animated_text(
                    f"[NAUKA] {words_learned_count} nowych pojęć: {', '.join(learned_summary)}",
                    Colors.GREEN + Colors.FAINT, 0.01
                )
                
                # Ponowna analiza po nauce
                vec_F, detected_sector, _ = self.lexicon.analyze_text(tresc, enable_reinforcement=False)
                self.lexicon.save()

        # Fallback: Jeśli wektor nadal jest słaby, użyj archetypu
        if np.linalg.norm(vec_F) < 0.1:
            if target_sector:
                vec_F = self.archetypy[target_sector].copy()
                detected_sector = target_sector
                self.ui.print_animated_text(
                    f"[SYSTEM] Wektor wzmocniony archetypem '{target_sector}'.",
                    Colors.FAINT, 0.01
                )
            else:
                self.ui.print_animated_text(
                    f"[OSTRZEŻENIE] Zbyt abstrakcyjne. Użyj silniejszego tagu.",
                    Colors.RED, 0.02
                )

        # Ustal ostateczną kategorię
        final_category = detected_sector if detected_sector else (target_sector if target_sector else "nieznane")
        _, kolor = self._analyze_nature(final_category)

        # Wzmocnienie archetypowe
        if final_category in self.archetypy:
            vec_F = (vec_F * 0.9) + (self.archetypy[final_category] * 0.1)
            if np.linalg.norm(vec_F) > 0:
                vec_F /= np.linalg.norm(vec_F)
            
        kor = self.byt_stan.oblicz_korelacje_struny(vec_F)

        # Zapis AKSJOMATU
        if is_axiom:
            def_id = f"Def_{len(self.D_Map)+1:03d}"
            self.D_Map[def_id] = {
                'wektor_C_Def': vec_F, 'waga_Ww': 100.0, 'tagi': [tag],
                'tresc': tresc, 'kategoria': final_category, 'created_at': time.time(), 'immutable': True
            }
            self.byt_stan.akumuluj_styk(vec_F)
            self.ui.print_animated_text(
                f"[AKSJOMAT] {def_id} -> {final_category}",
                Colors.RED+Colors.BOLD, 0.02
            )
            self.save_knowledge()
            return

        # Refinement (Ulepszanie istniejącej wiedzy)
        best_id, sim = self._find_closest_definition(vec_F)
        if np.linalg.norm(vec_F) > 0.1 and best_id and sim > self.PRÓG_REFINE_MIN and sim < self.PRÓG_KOMPRESJI_ONTOLOGICZNEJ:
            d = self.D_Map[best_id]
            if not d.get('immutable'):
                d['wektor_C_Def'] = (d['wektor_C_Def'] * 0.8) + (vec_F * 0.2)
                d['wektor_C_Def'] /= np.linalg.norm(d['wektor_C_Def'])
                
                if len(tresc) > len(d['tresc']):
                    d['tresc'] = tresc
                    self.ui.print_animated_text(
                        f"[DOPRECYZOWANIE] Rozszerzono definicję {best_id}.",
                        Colors.CYAN, 0.02
                    )
                else:
                    self.ui.print_animated_text(
                        f"[NIUANS] Zaktualizowano wektor pojęcia {best_id}.",
                        Colors.CYAN, 0.02
                    )
                self.save_knowledge()
                return

        # Zapis NOWEJ WIEDZY
        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {
            'wektor_C_Def': vec_F, 'waga_Ww': 10.0, 'tagi': [tag],
            'tresc': tresc, 'kategoria': final_category, 'created_at': time.time(), 'immutable': False
        }
        self.byt_stan.akumuluj_styk(vec_F)

        self.ui.print_animated_text(
            f"[NOWA WIEDZA] {def_id} (kor:{kor:.2f}) [{final_category}]",
            kolor, 0.02
        )
        self.save_knowledge()

    def stop(self):
        self.ui.print_animated_text(f"\n[AII] Zapisuję stan (JSONL)...", Colors.YELLOW, 0.03)
        self.running = False
        self.save_knowledge()
        self.ui.print_animated_text(f"[AII] Do widzenia.", Colors.GREEN, 0.03)