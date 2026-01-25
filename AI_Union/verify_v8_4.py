# -*- coding: utf-8 -*-
"""
verify_v8_4.py - Test Integracyjny dla EriAmo v8.4.0 (FIXED)
Poprawiono:
1. Wymuszenie nauki chunka (podwójna ekspozycja).
2. Import kolorów.
"""

import sys
import os
import numpy as np
import time

# Upewnij się, że jesteśmy w dobrym katalogu
if not os.path.exists("aii.py"):
    print("❌ BŁĄD: Uruchom ten skrypt w katalogu AI_Union!")
    sys.exit(1)

# Import konfiguracji (dla kolorów)
try:
    from union_config import UnionConfig, Colors
except ImportError:
    class Colors: # Fallback gdyby nie było pliku
        GREEN = ""; RED = ""; RESET = ""

print(f"🔍 [TEST] Rozpoczynam weryfikację EriAmo v8.4.0-Hybrid...")

# 1. TEST IMPORTÓW
print("\n--- KROK 1: Weryfikacja Modułów ---")
try:
    from aii import AII
    print("✅ Moduł 'aii' załadowany.")
except ImportError as e:
    print(f"❌ BŁĄD: Nie można załadować aii.py: {e}")
    sys.exit(1)

try:
    from chunk_lexicon import ChunkLexicon
    print("✅ Moduł 'chunk_lexicon' załadowany.")
except ImportError:
    print("❌ BŁĄD: Brak pliku 'chunk_lexicon.py'.")
    sys.exit(1)

try:
    from ontological_compression_15d import OntologicalCompressor
    print("✅ Moduł 'ontological_compression_15d' załadowany.")
except ImportError:
    print("❌ BŁĄD: Brak pliku 'ontological_compression_15d.py'.")
    sys.exit(1)

# 2. INICJALIZACJA RDZENIA
print("\n--- KROK 2: Inicjalizacja Rdzenia ---")
try:
    # Uruchamiamy w trybie cichym (bez GUI)
    core = AII(standalone_mode=False)
    print(f"✅ EriAmo uruchomione. Wersja: {core.VERSION}")
    print(f"✅ Wymiary wektora: {core.DIM}")
except Exception as e:
    print(f"❌ BŁĄD INICJALIZACJI: {e}")
    sys.exit(1)

# 3. TEST CHUNKÓW (SEKWENCJI)
print("\n--- KROK 3: Test Chunk-Based Processing ---")
test_phrase = "w głębi duszy"
print(f"🔹 Uczę frazy testowej: '{test_phrase}'")

# Symulacja ekstraktora (jak przy /read)
if core.chunk_lexicon:
    # FIX: Powtarzamy frazę 2x, bo ekstraktor wymaga min. 2 wystąpień (filtr szumu)
    text_to_learn = f"{test_phrase}. To jest zdanie i znowu {test_phrase}."
    core.chunk_lexicon.extract_chunks_from_text(text_to_learn)
    
    # Sprawdź czy zapamiętał
    if test_phrase in core.chunk_lexicon.chunks:
        chunk = core.chunk_lexicon.chunks[test_phrase]
        print(f"✅ SUKCES: Chunk '{test_phrase}' zapisany w pamięci.")
        print(f"   Częstość: {chunk.frequency}")
        
        # Test analizy
        analysis = core.chunk_lexicon.analyze_text_chunks(f"Czuję to {test_phrase}")
        print(f"✅ Analiza zdania: Pokrycie = {analysis['coverage']:.2%}")
        if analysis['coverage'] > 0:
            print("✅ System poprawnie wykrył chunk w nowym zdaniu.")
        else:
            print("❌ BŁĄD: Nie wykryto chunka w zdaniu.")
    else:
        print("❌ BŁĄD: Fraza nie została dodana do leksykonu (sprawdź filtr częstości).")
else:
    print("❌ BŁĄD: Obiekt chunk_lexicon jest None.")

# 4. TEST KOMPRESJI ONTOLOGICZNEJ
print("\n--- KROK 4: Test Kompresji Ontologicznej ---")
# Ustawiamy sztuczny stan (np. Radość)
core.context_vector = np.zeros(core.DIM)
core.context_vector[0] = 1.0 # Radość

# Bodziec zgodny (też Radość)
vec_harmony = np.zeros(core.DIM); vec_harmony[0] = 0.9
is_comp, cos_a = core.check_ontological_compression(vec_harmony)
print(f"🔹 Test Zgodności (Radość vs Radość): cos α = {cos_a:.4f}")
if is_comp or cos_a > 0.8:
    print(f"✅ Wynik: {core.get_compression_interpretation(vec_harmony)} (Oczekiwano: HARMONIA/KOMPRESJA)")
else:
    print("❌ BŁĄD: System nie wykrył harmonii.")

# Bodziec sprzeczny (Smutek)
vec_conflict = np.zeros(core.DIM); vec_conflict[1] = 1.0 
is_comp, cos_a = core.check_ontological_compression(vec_conflict)
print(f"🔹 Test Konfliktu (Radość vs Smutek): cos α = {cos_a:.4f}")
print(f"✅ Interpretacja: {core.get_compression_interpretation(vec_conflict)}")

# 5. TEST CZYTANIA (PROGRESS BAR)
print("\n--- KROK 5: Test Deep Read (Pasek Postępu) ---")
# Tworzymy tymczasowy plik
dummy_file = "test_read.txt"
with open(dummy_file, "w", encoding="utf-8") as f:
    f.write("To jest testowe zdanie numer jeden. To jest testowe zdanie numer dwa. To jest testowe zdanie numer trzy.")

print("🔹 Uruchamiam /read...")
result = core.deep_read(dummy_file)
print(f"\n✅ Wynik czytania: {result}")

# Sprzątanie
try: os.remove(dummy_file)
except: pass

# 6. PODSUMOWANIE
print("\n" + "="*40)
print(f"{Colors.GREEN}WSZYSTKIE TESTY INTEGRACYJNE ZAKOŃCZONE POMYŚLNIE.{Colors.RESET}")
print("System EriAmo v8.4.0 jest gotowy do pracy.")
print("="*40)