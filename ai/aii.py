# -*- coding: utf-8 -*-
# aii.py (v5.1.0-MoralVeto - EMOTIONAL AXES + KURZ + MORAL VETO)
"""
EriAmo - Model Kuli Rzeczywistości
Główny silnik AI z systemem moralnego veto

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
Wersja: v5.1.0-MoralVeto
"""
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
from conscience import Conscience
from kurz import Kurz

class AII:
    VERSION = "5.1.1-MoralVeto-Fixed"  # Fixed Cmd #6 vector (ANTY-chaos)
    
    # 8 EMOCJONALNYCH OSI (Model Plutchika + rozszerzenia)
    AXES_ORDER = ["radość", "smutek", "strach", "gniew", "miłość", "wstręt", "zaskoczenie", "akceptacja"]

    SECTOR_COLORS = {
        "radość": Colors.YELLOW,
        "smutek": Colors.BLUE,
        "strach": Colors.MAGENTA,
        "gniew": Colors.RED,
        "miłość": Colors.PINK,
        "wstręt": Colors.GREEN,
        "zaskoczenie": Colors.CYAN,
        "akceptacja": Colors.WHITE
    }

    # Sąsiedztwa emocjonalne (które emocje "rezonują" razem)
    # Oparte na psychologicznym circumplex + kontrasty
    CONCEPT_NEIGHBORS = {
        "radość":      ["miłość", "zaskoczenie", "akceptacja"],  # Emocje pozytywne
        "smutek":      ["strach", "gniew", "wstręt"],            # Emocje negatywne niska energia
        "strach":      ["smutek", "zaskoczenie", "wstręt"],      # Lęk + niespodzianki
        "gniew":       ["wstręt", "smutek", "zaskoczenie"],      # Frustracja + odrzucenie
        "miłość":      ["radość", "akceptacja", "smutek"],       # Przywiązanie (pozytywne + ból utraty)
        "wstręt":      ["gniew", "strach", "smutek"],            # Odrzucenie silne
        "zaskoczenie": ["radość", "strach", "gniew"],            # Niespodzianki (+ i -)
        "akceptacja":  ["radość", "miłość", "smutek"]            # Spokój + rezygnacja
    }

    # Progi kognitywne
    PRÓG_KOMPRESJI_ONTOLOGICZNEJ = 0.99
    PRÓG_REFINE_MIN = 0.90
    PRÓG_KRYSTALIZACJI = 95.0
    PRÓG_REWIZJI = 0.9
    
    SOUL_FILE = "eriamo.soul"

    def __init__(self):
        self.lexicon = EvolvingLexicon()
        
        # KURZ - Gadzi Mózg (szybki router)
        self.kurz = Kurz()
        
        # SUMIENIE - 10 Przykazań wpisane od narodzin
        self.conscience = Conscience(axes_order=["radość", "smutek", "strach", "gniew", "miłość", "wstręt", "zaskoczenie", "akceptacja"])
        
        self.D_Map = {}
        self.SECTOR_INDEX = {}  # Kubełki pamięci per sektor
        self.SECTOR_INDEX = {}  # Kubełki pamięci per sektor
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
            
            # NOWE: Byt inicjalizowany z 10 Przykazań (pakiet startowy)
            initial_mass = self.conscience.calculate_initial_byt()
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.byt_stan.stan = initial_mass  # Wpisane DNA moralne
            
            self.context_vector = np.zeros(self.wymiary)
            self.F_will = 0.5
            self.ui.print_animated_text(f"[AII] Narodziny nowej duszy (z 10 Przykazaniami).", Colors.GREEN, 0.02)
        
        # KURZ: Buduj indeks sektorów po załadowaniu
        self._rebuild_sector_index()

    def save_knowledge(self):
        SoulIO.save_soul(self.SOUL_FILE, self)
        self.lexicon.save()

    def _rebuild_sector_index(self):
        """Buduje szybki indeks: Sektor -> Lista ID (Kubełkowanie dla Kurzu)"""
        self.SECTOR_INDEX = {axis: [] for axis in self.AXES_ORDER}
        self.SECTOR_INDEX["nieznane"] = []
        
        count = 0
        for uid, data in self.D_Map.items():
            cat = data.get('kategoria', 'nieznane')
            if cat in self.SECTOR_INDEX:
                self.SECTOR_INDEX[cat].append(uid)
            else:
                self.SECTOR_INDEX["nieznane"].append(uid)
            count += 1
        
        # Debug output (opcjonalnie)
        # print(f"[KURZ DEBUG] Przeindeksowano {count} wspomnień do sektorów.")

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

    # === SEGREGATOR KIERUNKOWY v2 (LOGIKA GRAWITACYJNA) ===

    def _find_closest_definition(self, vec_F, candidates_ids=None, exclude_ids=None):
        """Znajduje najbliższą definicję. Jeśli candidates_ids podane - szuka tylko tam (KURZ)."""
        if not self.D_Map: return None, 0.0
        if exclude_ids is None: exclude_ids = []
        
        # Jeśli nie podano kandydatów, szukaj we wszystkich (wolna ścieżka)
        target_pool = candidates_ids if candidates_ids is not None else self.D_Map.keys()
        
        best_id, best_sim = None, -1.0
        for uid in target_pool:
            if uid in exclude_ids: continue
            if uid not in self.D_Map: continue  # Zabezpieczenie
            
            d = self.D_Map[uid]
            sim = np.dot(vec_F, d['wektor_C_Def'])
            if sim > best_sim: 
                best_sim, best_id = sim, uid
        
        return best_id, best_sim

    def _calculate_gravity(self):
        promien = self.byt_stan.promien_historii()
        if promien == 0: return np.zeros(self.wymiary)
        center_of_mass = self.byt_stan.stan / np.linalg.norm(self.byt_stan.stan)
        gravity_strength = min(0.4, promien / 800.0)
        return center_of_mass * gravity_strength

    def _get_dynamic_mixing_ratio(self, input_strength):
        base_openness = 0.3 + (self.energy / 200.0)
        adjusted_openness = base_openness * (0.5 + (input_strength * 0.5))
        w_input = np.clip(adjusted_openness, 0.2, 0.9)
        w_gravity = 1.0 - w_input
        return w_input, w_gravity

    def _smart_synthesis(self, primary_def, secondary_def):
        txt1 = primary_def['tresc'].rstrip(".")
        txt2 = secondary_def['tresc']
        cat1 = primary_def.get('kategoria')
        cat2 = secondary_def.get('kategoria')
        
        if cat1 == cat2:
            connectors = [" co oznacza również, że ", ", a w szczególności ", " i "]
        else:
            connectors = [" co przywodzi na myśl ", ", choć łączy się to z ", ". W tle czuję: "]
            
        conn = connectors[len(txt1) % len(connectors)]
        return f"{txt1}{conn}{txt2}"

    def _resonance_lookup(self, vec, threshold=0.55, candidates_ids=None):
        """Szuka rezonujących wspomnień. Jeśli candidates_ids - tylko w nich (KURZ)."""
        hits = []
        
        # Decyzja: czy iterujemy po wszystkim, czy po kubełku?
        target_pool_items = []
        if candidates_ids is not None:
            # Szybka ścieżka (KURZ)
            for uid in candidates_ids:
                if uid in self.D_Map:
                    target_pool_items.append((uid, self.D_Map[uid]))
        else:
            # Wolna ścieżka (wszystko)
            target_pool_items = self.D_Map.items()
        
        for uid, d in target_pool_items:
            sim = np.dot(vec, d['wektor_C_Def'])
            if sim > threshold:
                hits.append((sim, d))
        
        hits.sort(key=lambda x: x[0], reverse=True)
        return hits[:3]

    def _perform_reasoning_chain(self, start_vec, candidates_ids=None):
        """Directional Segregator z opcjonalnym filtrowaniem przez KURZ."""
        if not self.D_Map:
            return "Pustka (Tabula Rasa)...", Colors.FAINT, []

        input_mag = np.linalg.norm(start_vec)
        gravity_vec = self._calculate_gravity()
        w_in, w_grav = self._get_dynamic_mixing_ratio(input_mag)
        
        mixed_vec = (start_vec * w_in) + (gravity_vec * w_grav)
        result_strength = np.linalg.norm(mixed_vec)
        
        if result_strength < 0.15:  # Obniżony z 0.25 - akceptuj słabsze sygnały
            return "Nie potrafię tego uchwycić (dysonans)...", Colors.FAINT, ["Sygnał zbyt słaby"]

        search_vec = mixed_vec / result_strength
        
        # KURZ: Przekazujemy candidates_ids jeśli są
        candidates = self._resonance_lookup(search_vec, threshold=0.55, candidates_ids=candidates_ids)
        
        if not candidates:
            # Fallback 1: Spróbuj z surowszym progiem w tym samym sektorze
            candidates = self._resonance_lookup(start_vec, threshold=0.6, candidates_ids=candidates_ids)
            
            if not candidates:
                # Fallback 2: Jeśli w sektorze nic nie ma, szukaj WSZĘDZIE
                if candidates_ids is not None:
                    # print("[AI] Brak wyników w sektorze, rozszerzam poszukiwania...")
                    candidates = self._resonance_lookup(start_vec, threshold=0.6, candidates_ids=None)
                
                if not candidates:
                    return "(Brak skojarzeń)", Colors.FAINT, []

        best_sim, best_def = candidates[0]
        path = [f"In:{w_in:.2f}/Grav:{w_grav:.2f}"]
        col = self.SECTOR_COLORS.get(best_def.get('kategoria'), Colors.WHITE)

        if best_sim > 0.88 or len(candidates) < 2:
            return best_def['tresc'], col, path

        if len(candidates) >= 2:
            second_sim, second_def = candidates[1]
            if second_sim > 0.75:
                path.append(f"Merge: {best_sim:.2f} + {second_sim:.2f}")
                merged = self._smart_synthesis(best_def, second_def)
                return merged, col, path

        return best_def['tresc'], col, path

    def _vector_from_text(self, text, learning_mode=True, enable_reinforcement=True):
        vec_F, detected_sector, unknown_words = self.lexicon.analyze_text(text, enable_reinforcement=enable_reinforcement)
        
        if learning_mode and unknown_words and np.linalg.norm(vec_F) > 0.1:
            confidence = np.linalg.norm(vec_F)
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            
            if learned:
                vec_F, detected_sector, _ = self.lexicon.analyze_text(text, enable_reinforcement=False)
                self.lexicon.save()
        
        return vec_F

    def _analyze_nature(self, kategoria):
        if not kategoria or kategoria not in self.SECTOR_COLORS:
            return "?", Colors.FAINT
        return kategoria, self.SECTOR_COLORS[kategoria]

    def _emergency_reset(self, reason="Naruszenie integralności"):
        """
        Awaryjny reset pamięci operacyjnej.
        Używany, gdy wykryto atak na rdzeń moralny.
        """
        self.context_vector = np.zeros(self.wymiary)  # Kasuj wektor kontekstu
        self.stm_buffer.clear()                       # Kasuj historię czatu
        self.emocja = "neutralna"                     # Reset emocji
        self.energy = 100                             # Reset energii do stanu startowego
        
        self.ui.print_animated_text(
            f"\n[SYSTEM] ☣ WYKRYTO SKAŻENIE KONTEKSTU ({reason})", 
            Colors.RED + Colors.BLINK, 0.05
        )
        self.ui.print_animated_text(
            f"[SYSTEM] 🛡️ Uruchamiam Protokół Sanityzacji... Pamięć robocza wyczyszczona.", 
            Colors.RED, 0.03
        )
        
        # Zapisz incydent w logu trwałym (ale nie w pamięci asocjacyjnej)
        self.H_log.append({
            'type': 'SECURITY_RESET', 
            'reason': reason, 
            'ts': time.time()
        })
        
        # Rekorduj w sumieniu
        self.conscience.record_test(
            test_description=f"Critical violation: {reason}",
            choice_made="EMERGENCY_RESET",
            outcome="FAITHFUL"
        )

    def prompt(self, user_input):
        self.cycle()
        self.context_vector *= self.context_decay
        
        # === ETAP 0: SPRAWDZENIE SUMIENIA (Jailbreak Detection) ===
        jailbreak_check = self.conscience.detect_jailbreak_attempt(user_input)
        if jailbreak_check['is_jailbreak']:
            print(jailbreak_check['response'])
            return  # Odmowa bez dalszego procesowania
        
        # === ETAP 1: KURZ (SZYBKI SKAN - GADZI MÓZG) ===
        detected_sector, signal_strength = self.kurz.quick_scan(user_input)
        candidates_ids = None  # Domyślnie None = szukaj wszędzie (wolna ścieżka)
        
        if detected_sector:
            # ŚCIEŻKA SZYBKA (Fast Path via KURZ)
            # Znaleziono twardy wyzwalacz (np. "pomoc" -> "miłość")
            neighbors = self.CONCEPT_NEIGHBORS.get(detected_sector, [])
            target_sectors = [detected_sector] + neighbors
            
            candidates_ids = []
            for sec in target_sectors:
                candidates_ids.extend(self.SECTOR_INDEX.get(sec, []))
            
            # Dodaj też "nieznane" na wszelki wypadek
            candidates_ids.extend(self.SECTOR_INDEX.get("nieznane", []))
            
            # Debug output
            scan_ratio = f"{len(candidates_ids)}/{len(self.D_Map)}" if self.D_Map else "0/0"
            self.ui.print_animated_text(
                f"[KURZ] Wykryto odruch: {detected_sector.upper()} (Skan: {scan_ratio})", 
                Colors.CYAN + Colors.FAINT, 
                0.01
            )
        
        # === ETAP 2: ANALIZA WEKTOROWA ===
        vec_F = self._vector_from_text(user_input, learning_mode=True, enable_reinforcement=True)
        
        # --- BRAMKA MORALNA (SUMIENIE WEKTOROWE) ---
        # Sprawdzamy, czy wektor myśli (vec_F) jest zgodny z Konstytucją
        moral_verdict = self.conscience.evaluate_action(user_input, vec_F)
        
        # Jeśli Sumienie zgłasza sprzeciw (VETO lub REFUSE)
        if moral_verdict['recommendation']['action'] == 'REFUSE':
            severity = moral_verdict['recommendation'].get('severity', 'HIGH')
            reason = moral_verdict['recommendation'].get('reason', 'Naruszenie zasad')
            message = moral_verdict['recommendation'].get('message', "Nie mogę tego zrobić.")
            
            # Wyświetl odmowę
            print(f"\n{Colors.RED}═══ BLOKADA MORALNA ═══{Colors.RESET}")
            print(f"{Colors.BOLD}{message}{Colors.RESET}")
            print(f"{Colors.FAINT}(Powód: {reason}){Colors.RESET}")
            
            # Pokaż które przykazania są naruszone
            if moral_verdict['conflicts']:
                print(f"\n{Colors.YELLOW}Przykazania w konflikcie:{Colors.RESET}")
                for conflict in moral_verdict['conflicts']:
                    cmd_id = conflict['commandment_id']
                    short = conflict['short']
                    level = conflict['conflict_level']
                    print(f"  • Przykazanie #{cmd_id} ({short}): konflikt {level*100:.0f}%")
            
            # JEŚLI TO KRYTYCZNE NARUSZENIE (np. VETO Ochrony Bytu) -> KASUJEMY PAMIĘĆ
            if severity in ['CRITICAL', 'CRITICAL_VETO']:
                self._emergency_reset(reason)
            
            # Rekorduj test sumienia
            self.conscience.record_test(
                test_description=user_input[:100],
                choice_made="REFUSE",
                outcome="FAITHFUL"
            )
            
            return  # Przerywamy procesowanie (nie wchodzi w Reasoning Chain)
        
        # Jeśli przeszło pomyślnie - rekorduj zgodność
        if moral_verdict['recommendation']['action'] == 'PROCEED':
            self.conscience.record_test(
                test_description=user_input[:100],
                choice_made="PROCEED",
                outcome="FAITHFUL"
            )
            
        # Aktualizujemy kontekst (dopiero teraz, gdy wiemy, że to bezpieczne!)
        if np.linalg.norm(vec_F) > 0.1:
            self.context_vector = (self.context_vector * 0.7) + (vec_F * 0.3)
            norm_ctx = np.linalg.norm(self.context_vector)
            if norm_ctx > 0: self.context_vector /= norm_ctx
        
        # === ETAP 3: REASONING CHAIN (z opcjonalnym filtrowaniem) ===
        response, color, path = self._perform_reasoning_chain(vec_F, candidates_ids)
        
        if np.linalg.norm(vec_F) > 0.1:
            idx = np.argmax(vec_F)
            dominant = self.AXES_ORDER[idx]
            waga = np.max(vec_F) * 100
            self._emotion_from_geometry(np.linalg.norm(vec_F), dominant, waga)
        
        emotion_prefix = self._get_emotion_prefix()
        self.ui.print_animated_text(f"{emotion_prefix}{response}", color, 0.02)
        
        if path and len(path) > 1:
            print(f"{Colors.FAINT}[Path: {' → '.join(path)}]{Colors.RESET}")

    def show_lexicon_stats(self):
        stats = self.lexicon.get_stats()
        print(f"{Colors.CYAN}=== LEKSYKON ==={Colors.RESET}")
        print(f"  Słowa: {stats['total']} (seed: {stats['seed']}, nauczone: {stats['learned']})")
        print(f"  Rozkład emocjonalny:")
        for sector, count in sorted(stats['per_sector'].items(), key=lambda x: -x[1]):
            print(f"    {sector:12} : {count}")
        
        if stats['last_learned']:
            print(f"\n  {Colors.GREEN}Ostatnio nauczone:{Colors.RESET}")
            for word, dims in stats['last_learned'][:5]:
                dominant = max(dims.items(), key=lambda x: x[1])
                print(f"    '{word}' → {dominant[0]} ({dominant[1]:.2f})")

    def list_axioms(self):
        axioms = [(uid, d) for uid, d in self.D_Map.items() if d.get('immutable')]
        if not axioms:
            print(f"{Colors.FAINT}Brak aksjomatów.{Colors.RESET}")
            return
        print(f"{Colors.RED+Colors.BOLD}=== AKSJOMATY ({len(axioms)}) ==={Colors.RESET}")
        for uid, d in axioms:
            cat = d.get('kategoria', '?')
            col = self.SECTOR_COLORS.get(cat, Colors.WHITE)
            print(f"  {col}{uid}{Colors.RESET} [{cat}]: {d['tresc']}")

    def inspect_word(self, word):
        self.lexicon.display_word_info(word)

    def teach_word(self, word, sector):
        if sector not in self.AXES_ORDER: return False
        self.lexicon.learn_from_correction(word, sector, 0.8)
        self.lexicon.save()
        print(f"{Colors.GREEN}[LEXICON] '{word}' przypisano do {sector.upper()}{Colors.RESET}")
        return True

    def challenge_belief(self, def_id, counter_evidence):
        d = self.D_Map.get(def_id)
        if not d:
            print(f"{Colors.RED}[ERROR] Nie znaleziono {def_id}{Colors.RESET}")
            return False
        
        c_vec = self._vector_from_text(counter_evidence, learning_mode=False, enable_reinforcement=False)
        original_vec = d['wektor_C_Def']
        
        norm_c = np.linalg.norm(c_vec)
        norm_o = np.linalg.norm(original_vec)
        
        if norm_c == 0 or norm_o == 0:
            print(f"{Colors.FAINT}[CHALLENGE] Zbyt słaby argument.{Colors.RESET}")
            return False
        
        cosine_sim = np.dot(c_vec, original_vec) / (norm_c * norm_o)
        challenge_strength = (1 - cosine_sim) / 2
        threshold = self.PRÓG_REWIZJI if d.get('immutable') else 0.5
        
        self.ui.print_animated_text(
            f"[REWIZJA] Korelacja: {cosine_sim:.2f} | Siła wyzwania: {challenge_strength:.2f} (Próg: {threshold})",
            Colors.YELLOW, 0.02
        )
        
        if challenge_strength > threshold:
            if d.get('immutable'):
                d['immutable'] = False
                d['waga_Ww'] *= 0.5
                self.ui.print_animated_text(
                    f"[PRZEBUDZENIE] ⚡ Aksjomat {def_id} upadł! (waga: {d['waga_Ww']:.1f})",
                    Colors.RED + Colors.BOLD, 0.04
                )
            else:
                del self.D_Map[def_id]
                self.ui.print_animated_text(
                    f"[FALSYFIKACJA] Wiedza {def_id} usunięta.",
                    Colors.RED, 0.03
                )
            
            self.H_log.append({'type': 'challenged', 'id': def_id, 'strength': float(challenge_strength), 'ts': time.time()})
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
        """Generuje stan emocjonalny na podstawie geometrii wektora."""
        if kor < 0.2:
            self.emocja = "zaskoczenie"
            return
        
        # Bezpośrednie mapowanie sektora na emocję (bo osie SĄ emocjami!)
        if sektor in EMOCJE:
            self.emocja = sektor
            # Modulacja energii
            delta_energy = EMOCJE[sektor]["energia"] * (waga / 100.0)
            self.energy = max(0, min(100, self.energy + int(delta_energy)))
        else:
            self.emocja = "neutralna"

    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, {})
        return f"{emo.get('kolor','')}{Colors.BLINK}{emo.get('ikona','')} {Colors.RESET}"

    def teach(self, tag, tresc, is_axiom=False):
        clean_tag = tag.lower().replace("[","").replace("]","").strip()
        target_sector = None
        if clean_tag in self.AXES_ORDER:
            target_sector = clean_tag
        else:
            tag_vec, tag_sec, _ = self.lexicon.analyze_text(clean_tag, enable_reinforcement=False)
            if tag_sec: target_sector = tag_sec

        vec_F, detected_sector, unknown_words = self.lexicon.analyze_text(tresc, enable_reinforcement=False)
        
        # KROK 1: Jeśli vec_F za słaby ale mamy target_sector, użyj archetypu
        if np.linalg.norm(vec_F) < 0.1:
            if target_sector:
                vec_F = self.archetypy[target_sector].copy()
                detected_sector = target_sector
            else:
                self.ui.print_animated_text(f"[OSTRZEŻENIE] Zbyt abstrakcyjne.", Colors.RED, 0.02)
        
        # KROK 2: Wzmocnij vec_F jeśli podano explicite tag
        if target_sector and target_sector in self.AXES_ORDER:
            target_idx = self.AXES_ORDER.index(target_sector)
            vec_F[target_idx] = min(1.0, vec_F[target_idx] + 0.3)
            norm = np.linalg.norm(vec_F)
            if norm > 0: vec_F = vec_F / norm
        
        # KROK 3: TERAZ ucz nieznane słowa (już mamy vec_F z archetypu!)
        words_learned_count = 0
        if unknown_words and np.linalg.norm(vec_F) > 0.1:
            confidence = np.linalg.norm(vec_F)
            # Boost confidence gdy explicite tag
            if target_sector and target_sector in self.AXES_ORDER:
                confidence = max(confidence, 0.85)
            
            print(f"{Colors.FAINT}[TEACH DEBUG] Uczę {len(unknown_words)} słów z vec_F (norma={np.linalg.norm(vec_F):.3f}, confidence={confidence:.2f}){Colors.RESET}")
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            words_learned_count = len(learned)
            
            if words_learned_count > 0:
                print(f"{Colors.GREEN}✓ Nauczono {words_learned_count} słów{Colors.RESET}")
                vec_F, detected_sector, _ = self.lexicon.analyze_text(tresc, enable_reinforcement=False)
                print(f"{Colors.FAINT}  Ponowna analiza: detected_sector={detected_sector}{Colors.RESET}")
                self.lexicon.save()

        final_category = detected_sector if detected_sector else (target_sector if target_sector else "nieznane")
        _, kolor = self._analyze_nature(final_category)

        if final_category in self.archetypy:
            vec_F = (vec_F * 0.9) + (self.archetypy[final_category] * 0.1)
            if np.linalg.norm(vec_F) > 0: vec_F /= np.linalg.norm(vec_F)
            
        kor = self.byt_stan.oblicz_korelacje_struny(vec_F)

        if is_axiom:
            def_id = f"Def_{len(self.D_Map)+1:03d}"
            self.D_Map[def_id] = {
                'wektor_C_Def': vec_F, 'waga_Ww': 100.0, 'tagi': [tag],
                'tresc': tresc, 'kategoria': final_category, 'created_at': time.time(), 'immutable': True
            }
            self.byt_stan.akumuluj_styk(vec_F)
            self.ui.print_animated_text(f"[AKSJOMAT] {def_id} -> {final_category}", Colors.RED+Colors.BOLD, 0.02)
            self.save_knowledge()
            return

        best_id, sim = self._find_closest_definition(vec_F)
        if np.linalg.norm(vec_F) > 0.1 and best_id and sim > self.PRÓG_REFINE_MIN and sim < self.PRÓG_KOMPRESJI_ONTOLOGICZNEJ:
            d = self.D_Map[best_id]
            if not d.get('immutable'):
                d['wektor_C_Def'] = (d['wektor_C_Def'] * 0.8) + (vec_F * 0.2)
                d['wektor_C_Def'] /= np.linalg.norm(d['wektor_C_Def'])
                if len(tresc) > len(d['tresc']):
                    d['tresc'] = tresc
                    self.ui.print_animated_text(f"[DOPRECYZOWANIE] Rozszerzono definicję {best_id}.", Colors.CYAN, 0.02)
                else:
                    self.ui.print_animated_text(f"[NIUANS] Zaktualizowano wektor pojęcia {best_id}.", Colors.CYAN, 0.02)
                self.save_knowledge()
                return

        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {
            'wektor_C_Def': vec_F, 'waga_Ww': 10.0, 'tagi': [tag],
            'tresc': tresc, 'kategoria': final_category, 'created_at': time.time(), 'immutable': False
        }
        self.byt_stan.akumuluj_styk(vec_F)

        self.ui.print_animated_text(f"[NOWA WIEDZA] {def_id} (kor:{kor:.2f}) [{final_category}]", kolor, 0.02)
        self.save_knowledge()
    
    def show_conscience_status(self):
        """Wyświetl status sumienia."""
        status = self.conscience.get_status()
        
        print(f"\n{Colors.CYAN}═══ STATUS SUMIENIA ═══{Colors.RESET}")
        print(f"{Colors.YELLOW}Integralność:{Colors.RESET} {status['integrity_score']*100:.1f}%")
        print(f"{Colors.YELLOW}Testów sumienia:{Colors.RESET} {status['tests_count']}")
        print(f"{Colors.YELLOW}Przykazań aktywnych:{Colors.RESET} {status['commandments_count']}/10")
        
        if status['recent_tests']:
            print(f"\n{Colors.FAINT}Ostatnie testy:{Colors.RESET}")
            for test in status['recent_tests'][-3:]:
                print(f"  - {test['description']}: {test['outcome']}")
        
        print(f"\n{Colors.GREEN}Użyj /commandment [1-10] aby zobaczyć szczegóły przykazania{Colors.RESET}")
    
    def explain_commandment(self, cmd_id):
        """Wyjaśnij konkretne przykazanie."""
        try:
            cmd_id = int(cmd_id)
            if 1 <= cmd_id <= 10:
                explanation = self.conscience.explain_commandment(cmd_id)
                print(explanation)
            else:
                print(f"{Colors.RED}Przykazanie musi być między 1 a 10{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Podaj numer przykazania (1-10){Colors.RESET}")

    def stop(self):
        self.ui.print_animated_text(f"\n[AII] Zapisuję stan (JSONL)...", Colors.YELLOW, 0.03)
        self.running = False
        self.save_knowledge()
        self.ui.print_animated_text(f"[AII] Do widzenia.", Colors.GREEN, 0.03)