# -*- coding: utf-8 -*-
# soul_io.py v2.1 - Hybrid Soul Handler (JSONL + Legacy Migration)
# Changelog:
#   - ADD: Automatyczne wykrywanie i migracja formatu v1.x (JSON) -> v2.x (JSONL)

import json
import time
import numpy as np
import os
from config import Colors

class SoulIO:
    FORMAT_VERSION = "2.1-Hybrid"
    
    @staticmethod
    def vec_to_sparse(vec, axes_list):
        sparse = {}
        if vec is None or len(vec) == 0: return sparse
        for i, val in enumerate(vec):
            if abs(val) > 0.001:
                axis_name = axes_list[i] if i < len(axes_list) else f"dim_{i}"
                sparse[axis_name] = round(float(val), 4)
        return sparse

    @staticmethod
    def sparse_to_vec(sparse_dict, axes_list):
        dim = len(axes_list)
        vec = np.zeros(dim)
        for i, axis in enumerate(axes_list):
            vec[i] = sparse_dict.get(axis, 0.0)
        return vec

    @staticmethod
    def _migrate_dimensions(old_dims, new_dims, sparse_dict):
        migrated = {}
        for axis, val in sparse_dict.items():
            if axis in new_dims: migrated[axis] = val
        return migrated

    @staticmethod
    def save_soul(filepath, aii_instance):
        """Zapisuje stan AI do formatu .soul (JSONL - linia po linii)."""
        print(f"{Colors.CYAN}[SoulIO] Pulsowanie duszy (JSONL) do {filepath}...{Colors.RESET}")
        start_time = time.time()
        
        meta = {
            "name": "EriAmo",
            "format_version": SoulIO.FORMAT_VERSION,
            "created_at": int(time.time()),
            "total_mass": round(aii_instance.byt_stan.promien_historii(), 4),
            "definition_count": len(aii_instance.D_Map),
            "axiom_count": sum(1 for d in aii_instance.D_Map.values() if d.get('immutable'))
        }

        state = {
            "energy": round(aii_instance.energy, 2),
            "emotion": aii_instance.emocja,
            "F_will": round(aii_instance.F_will, 4),
            "context_vector": SoulIO.vec_to_sparse(aii_instance.context_vector, aii_instance.AXES_ORDER),
            "context_decay": aii_instance.context_decay,
            "status": aii_instance.status
        }

        byt = {
            "stan": SoulIO.vec_to_sparse(aii_instance.byt_stan.stan, aii_instance.AXES_ORDER),
            "promien": round(aii_instance.byt_stan.promien_historii(), 4)
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json.dumps({"_type": "@META", **meta}, ensure_ascii=False) + "\n")
                f.write(json.dumps({"_type": "@DIMENSIONS", "data": aii_instance.AXES_ORDER}, ensure_ascii=False) + "\n")
                f.write(json.dumps({"_type": "@STATE", **state}, ensure_ascii=False) + "\n")
                f.write(json.dumps({"_type": "@BYT", **byt}, ensure_ascii=False) + "\n")

                for uid, d in aii_instance.D_Map.items():
                    entry = {
                        "_type": "@CORE" if d.get('immutable') else "@MEMORY",
                        "id": uid,
                        "vector": SoulIO.vec_to_sparse(d['wektor_C_Def'], aii_instance.AXES_ORDER),
                        "content": d['tresc'],
                        "weight": round(float(d['waga_Ww']), 2),
                        "tags": d.get('tagi', []),
                        "category": d.get('kategoria'),
                        "created_at": d.get('created_at', 0)
                    }
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

                h_log = aii_instance.H_log[-100:] if hasattr(aii_instance, 'H_log') else []
                for h_entry in h_log:
                    f.write(json.dumps({"_type": "@HISTORY", **h_entry}, ensure_ascii=False) + "\n")

            print(f"{Colors.GREEN}[SoulIO] Zapisano strumieniowo ({len(aii_instance.D_Map)} def).{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd zapisu JSONL: {e}{Colors.RESET}")
            return False

    @staticmethod
    def load_soul(filepath, aii_instance):
        """Inteligentne ładowanie: próbuje JSONL, w razie błędu spada na Legacy JSON."""
        if not os.path.exists(filepath):
            print(f"{Colors.YELLOW}[SoulIO] Brak pliku {filepath}. Tworzę nową duszę.{Colors.RESET}")
            return False

        # Próba 1: Czy to JSONL (v2+)?
        if SoulIO._try_load_jsonl(filepath, aii_instance):
            return True
        
        # Próba 2: Czy to Legacy JSON (v1)?
        print(f"{Colors.YELLOW}[SoulIO] Wykryto starszy format pliku. Rozpoczynam migrację Legacy -> JSONL...{Colors.RESET}")
        if SoulIO._load_legacy_v1(filepath, aii_instance):
            print(f"{Colors.CYAN}[SoulIO] Migracja udana w pamięci. Zapisz (/save) aby utrwalić format.{Colors.RESET}")
            return True
            
        return False

    @staticmethod
    def _try_load_jsonl(filepath, aii_instance):
        """Logika ładowania strumieniowego v2."""
        temp_d_map = {}
        temp_h_log = []
        saved_dims = []
        current_dims = aii_instance.AXES_ORDER
        dims_changed = False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Sprawdź pierwsze 5 linii. Jeśli wszystkie błędne -> to nie JSONL
                sample_lines = [f.readline() for _ in range(5)]
                valid_lines = 0
                for l in sample_lines:
                    if not l.strip(): continue
                    try: 
                        d = json.loads(l)
                        if isinstance(d, dict) and "_type" in d: valid_lines += 1
                    except: pass
                
                # Jeśli próbka wygląda źle, przerwij i oddaj sterowanie do Legacy
                if valid_lines == 0 and any(l.strip() for l in sample_lines):
                    return False
                
                # Reset pointera i właściwe ładowanie
                f.seek(0)
                print(f"{Colors.CYAN}[SoulIO] Wczytywanie strumienia JSONL...{Colors.RESET}")

                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        data = json.loads(line)
                    except: continue

                    type_tag = data.pop("_type", None)

                    if type_tag == "@DIMENSIONS":
                        saved_dims = data.get("data", [])
                        if saved_dims != current_dims: dims_changed = True

                    elif type_tag == "@STATE":
                        aii_instance.energy = data.get("energy", 100)
                        aii_instance.emocja = data.get("emotion", "neutralna")
                        aii_instance.F_will = data.get("F_will", 0.5)
                        aii_instance.status = data.get("status", "myślę")
                        aii_instance.context_decay = data.get("context_decay", 0.8)
                        ctx_sparse = data.get("context_vector", {})
                        if dims_changed: ctx_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, ctx_sparse)
                        aii_instance.context_vector = SoulIO.sparse_to_vec(ctx_sparse, current_dims)

                    elif type_tag == "@BYT":
                        byt_sparse = data.get("stan", {})
                        if dims_changed: byt_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, byt_sparse)
                        aii_instance.byt_stan.stan = SoulIO.sparse_to_vec(byt_sparse, current_dims)

                    elif type_tag in ["@CORE", "@MEMORY"]:
                        uid = data.get("id")
                        if not uid: continue
                        vec_sparse = data.get("vector", {})
                        if dims_changed: vec_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, vec_sparse)
                        temp_d_map[uid] = {
                            'wektor_C_Def': SoulIO.sparse_to_vec(vec_sparse, current_dims),
                            'tresc': data.get("content", ""),
                            'waga_Ww': data.get("weight", 10.0),
                            'tagi': data.get("tags", []),
                            'kategoria': data.get("category"),
                            'created_at': data.get("created_at", 0),
                            'immutable': (type_tag == "@CORE")
                        }
                    elif type_tag == "@HISTORY":
                        temp_h_log.append(data)

            # Sukces - podmień struktury
            aii_instance.D_Map = temp_d_map
            aii_instance.H_log = temp_h_log
            print(f"{Colors.GREEN}[SoulIO] Wczytano JSONL: {len(temp_d_map)} definicji.{Colors.RESET}")
            return True

        except Exception as e:
            # Błąd krytyczny odczytu JSONL
            return False

    @staticmethod
    def _load_legacy_v1(filepath, aii_instance):
        """Ładowanie starego formatu (cały plik na raz)."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            saved_dims = data.get("@DIMENSIONS", [])
            current_dims = aii_instance.AXES_ORDER
            dims_changed = saved_dims != current_dims

            state = data.get("@STATE", {})
            aii_instance.energy = state.get("energy", 100)
            aii_instance.emocja = state.get("emotion", "neutralna")
            aii_instance.context_decay = state.get("context_decay", 0.8)

            ctx_sparse = state.get("context_vector", {})
            if dims_changed: ctx_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, ctx_sparse)
            aii_instance.context_vector = SoulIO.sparse_to_vec(ctx_sparse, current_dims)

            byt_data = data.get("@BYT", {})
            byt_sparse = byt_data.get("stan", {})
            if dims_changed: byt_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, byt_sparse)
            aii_instance.byt_stan.stan = SoulIO.sparse_to_vec(byt_sparse, current_dims)

            aii_instance.D_Map = {}
            core_ids = set(c["id"] for c in data.get("@CORE", []))
            all_entries = data.get("@CORE", []) + data.get("@MEMORY", [])

            for entry in all_entries:
                uid = entry["id"]
                vec_sparse = entry.get("vector", {})
                if dims_changed: vec_sparse = SoulIO._migrate_dimensions(saved_dims, current_dims, vec_sparse)
                aii_instance.D_Map[uid] = {
                    'wektor_C_Def': SoulIO.sparse_to_vec(vec_sparse, current_dims),
                    'tresc': entry.get("content", ""),
                    'waga_Ww': entry.get("weight", 10.0),
                    'tagi': entry.get("tags", []),
                    'kategoria': entry.get("category"),
                    'created_at': entry.get("created_at", 0),
                    'immutable': uid in core_ids
                }

            aii_instance.H_log = data.get("@HISTORY", [])
            return True

        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd migracji Legacy: {e}{Colors.RESET}")
            return False

    @staticmethod
    def get_soul_summary(filepath):
        if not os.path.exists(filepath): return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Najpierw sprawdź czy to JSONL (pierwsza linia)
                first_line = f.readline().strip()
                if first_line.startswith('{'):
                    try:
                        data = json.loads(first_line)
                        if data.get("_type") == "@META": return data
                        # Jeśli pierwsza linia to {, ale nie ma _type, to może być stary JSON
                        if data.get("@META"): return data.get("@META") # Stary format
                    except: pass
                
                # Jeśli parsowanie linii nie wyszło, spróbuj stary format brute-force (tylko meta)
                f.seek(0)
                try:
                    full = json.load(f)
                    return full.get("@META")
                except: return None
        except Exception: return None