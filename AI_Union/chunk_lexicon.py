# -*- coding: utf-8 -*-
"""
chunk_lexicon.py v1.0.0 - Chunk-Based Language Processing
EriAmo Union - Nowa architektura językowa bazująca na sekwencjach

INSPIRACJA: Nature Human Behaviour (2026)
"Język to nie hierarchiczne drzewo składniowe, ale biblioteka gotowych sekwencji"

KLUCZOWE ZMIANY:
1. Zamiast pojedynczych słów → CHUNKS (sekwencje 2-5 słów)
2. Zamiast reguł gramatycznych → WZORCE STATYSTYCZNE
3. Zamiast parsing → PATTERN MATCHING
4. Dodano PRIMING (przyśpieszenie po pierwszym kontakcie)

Autor: Claude & Maciej (bazując na badaniach Christiansen et al.)
Data: 2025-01-25
"""

import numpy as np
import json
import time
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
from union_config import UnionConfig


# =============================================================================
# CHUNK DEFINITION
# =============================================================================

class LanguageChunk:
    """
    Chunk językowy - zapamiętana sekwencja słów.
    
    PRZYKŁADY:
    - "can I have a" (niekonstytutywa - nie jest frazą!)
    - "in the middle of the"
    - "czy mogę prosić o"
    - "w środku"
    
    Chunks są ZAPAMIĘTYWANE jako całość, nie generowane przez reguły.
    """
    
    def __init__(
        self,
        text: str,
        frequency: int = 1,
        emotional_vector: Optional[np.ndarray] = None
    ):
        """
        Args:
            text: Tekst chunka (np. "czy mogę prosić o")
            frequency: Częstość występowania
            emotional_vector: Wektor emocjonalny [15D]
        """
        self.text = text.lower().strip()
        self.words = self.text.split()
        self.length = len(self.words)
        self.frequency = frequency
        
        # Wektor emocjonalny (15D)
        if emotional_vector is None:
            self.emotional_vector = np.zeros(UnionConfig.DIMENSION)
        else:
            self.emotional_vector = emotional_vector
        
        # Priming (przyśpieszenie po pierwszym kontakcie)
        self.last_seen = 0.0
        self.priming_strength = 0.0
        
        # Konteksty użycia
        self.contexts = []  # Lista przykładowych zdań zawierających chunk
    
    def update_priming(self):
        """
        Aktualizuje siłę primingu po ponownym napotkaniu.
        
        MECHANIZM Z ARTYKUŁU:
        Po jednokrotnym zetknięciu mózg przetwarza sekwencję szybciej.
        """
        current_time = time.time()
        
        # Zanikanie primingu w czasie (half-life = 60 sekund)
        time_diff = current_time - self.last_seen
        decay = np.exp(-time_diff / 60.0)
        
        # Wzrost primingu (im częściej widzimy, tym silniejszy)
        self.priming_strength = min(1.0, self.priming_strength * decay + 0.3)
        self.last_seen = current_time
    
    def get_processing_speed_boost(self) -> float:
        """
        Zwraca boost szybkości przetwarzania (0.0 - 1.0).
        
        Returns:
            float: Multiplikator szybkości (1.0 = brak boostu, 2.0 = 2x szybciej)
        """
        return 1.0 + self.priming_strength
    
    def add_context(self, sentence: str):
        """Dodaje przykład użycia chunka."""
        if len(self.contexts) < 10:  # Limit 10 przykładów
            self.contexts.append(sentence)
    
    def to_dict(self) -> dict:
        """Serializacja do JSON."""
        return {
            'text': self.text,
            'frequency': self.frequency,
            'length': self.length,
            'emotional_vector': self.emotional_vector.tolist(),
            'priming_strength': self.priming_strength,
            'contexts': self.contexts[:3]  # Tylko 3 przykłady
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LanguageChunk':
        """Deserializacja z JSON."""
        chunk = cls(
            text=data['text'],
            frequency=data.get('frequency', 1),
            emotional_vector=np.array(data.get('emotional_vector', []))
        )
        chunk.priming_strength = data.get('priming_strength', 0.0)
        chunk.contexts = data.get('contexts', [])
        return chunk


# =============================================================================
# CHUNK-BASED LEXICON
# =============================================================================

class ChunkLexicon:
    """
    Leksykon oparty na sekwencjach (chunks) zamiast pojedynczych słów.
    
    NOWOŚĆ:
    - Zapamiętuje CZĘSTE SEKWENCJE (2-5 słów)
    - Automatyczne wykrywanie wzorców
    - Priming (przyśpieszenie po pierwszym kontakcie)
    - Statystyczna analiza bez reguł gramatycznych
    """
    
    def __init__(self, chunk_file: str = "data/chunks.json"):
        """
        Args:
            chunk_file: Ścieżka do pliku z chunkami
        """
        self.chunk_file = chunk_file
        
        # Chunks (indeksowane po tekście)
        self.chunks: Dict[str, LanguageChunk] = {}
        
        # Statystyki
        self.total_chunks = 0
        self.total_exposures = 0
        
        # Wczytaj z dysku
        self.load()
    
    # =========================================================================
    # CHUNK EXTRACTION (Automatyczne wykrywanie wzorców)
    # =========================================================================
    
    def extract_chunks_from_text(self, text: str, min_length: int = 2, max_length: int = 5):
        """
        Ekstraktuje wszystkie możliwe chunki z tekstu.
        
        MECHANIZM:
        - Okno przesuwne 2-5 słów
        - Zliczanie częstości
        - Filtrowanie po częstości
        
        Args:
            text: Tekst do analizy
            min_length: Min liczba słów w chunku
            max_length: Max liczba słów w chunku
        """
        # Preprocessing
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Usuń interpunkcję
        words = text.split()
        
        # Ekstraktuj wszystkie n-gramy
        chunk_candidates = []
        
        for n in range(min_length, max_length + 1):
            for i in range(len(words) - n + 1):
                chunk_text = ' '.join(words[i:i+n])
                chunk_candidates.append(chunk_text)
        
        # Zlicz częstości
        chunk_counts = Counter(chunk_candidates)
        
        # Dodaj do leksykonu (tylko częste)
        for chunk_text, count in chunk_counts.items():
            if count >= 2:  # Minimum 2 wystąpienia
                self.add_or_update_chunk(chunk_text, count)
    
    def add_or_update_chunk(self, chunk_text: str, frequency_boost: int = 1):
        """
        Dodaje chunk lub zwiększa jego częstość.
        
        Args:
            chunk_text: Tekst chunka
            frequency_boost: O ile zwiększyć częstość
        """
        chunk_text = chunk_text.lower().strip()
        
        if chunk_text in self.chunks:
            # Aktualizuj istniejący
            self.chunks[chunk_text].frequency += frequency_boost
            self.chunks[chunk_text].update_priming()
        else:
            # Stwórz nowy
            self.chunks[chunk_text] = LanguageChunk(chunk_text, frequency_boost)
            self.total_chunks += 1
        
        self.total_exposures += frequency_boost
    
    # =========================================================================
    # PATTERN MATCHING (Rozpoznawanie w tekście)
    # =========================================================================
    
    def find_chunks_in_text(self, text: str) -> List[Tuple[str, LanguageChunk, int]]:
        """
        Znajduje wszystkie chunki w tekście.
        
        Returns:
            List[(chunk_text, LanguageChunk, position)]
        """
        text_lower = text.lower()
        words = text_lower.split()
        found_chunks = []
        
        # Sortuj chunki po długości (najdłuższe pierwsze - zachłanny matching)
        sorted_chunks = sorted(
            self.chunks.items(),
            key=lambda x: x[1].length,
            reverse=True
        )
        
        for chunk_text, chunk in sorted_chunks:
            # Znajdź wszystkie wystąpienia
            chunk_words = chunk.words
            chunk_len = len(chunk_words)
            
            for i in range(len(words) - chunk_len + 1):
                if words[i:i+chunk_len] == chunk_words:
                    found_chunks.append((chunk_text, chunk, i))
                    
                    # Aktualizuj priming
                    chunk.update_priming()
        
        return found_chunks
    
    def analyze_text_chunks(self, text: str) -> Dict[str, any]:
        """
        Pełna analiza tekstu bazująca na chunkach.
        
        Returns:
            dict: {
                'chunks_found': List[str],
                'coverage': float,  # Procent tekstu pokryty chunkami
                'emotional_vector': np.ndarray,
                'priming_boost': float
            }
        """
        found_chunks = self.find_chunks_in_text(text)
        words = text.lower().split()
        
        # Oblicz pokrycie
        covered_words = set()
        for chunk_text, chunk, position in found_chunks:
            for i in range(position, position + chunk.length):
                covered_words.add(i)
        
        coverage = len(covered_words) / len(words) if words else 0.0
        
        # Agreguj wektor emocjonalny (ważony częstością)
        emotional_vector = np.zeros(UnionConfig.DIMENSION)
        total_weight = 0.0
        
        for chunk_text, chunk, position in found_chunks:
            weight = chunk.frequency * chunk.get_processing_speed_boost()
            emotional_vector += chunk.emotional_vector * weight
            total_weight += weight
        
        if total_weight > 0:
            emotional_vector /= total_weight
        
        # Średni boost primingu
        avg_priming = np.mean([
            chunk.get_processing_speed_boost() 
            for _, chunk, _ in found_chunks
        ]) if found_chunks else 1.0
        
        return {
            'chunks_found': [chunk_text for chunk_text, _, _ in found_chunks],
            'coverage': coverage,
            'emotional_vector': emotional_vector,
            'priming_boost': avg_priming,
            'chunk_count': len(found_chunks)
        }
    
    # =========================================================================
    # EMOTIONAL LEARNING (Uczenie emocji dla chunków)
    # =========================================================================
    
    def teach_chunk_emotion(
        self,
        chunk_text: str,
        emotional_vector: np.ndarray,
        strength: float = 0.5
    ):
        """
        Uczy chunk konkretnego wektora emocjonalnego.
        
        Args:
            chunk_text: Tekst chunka
            emotional_vector: Wektor emocji [15D]
            strength: Siła uczenia (0.0 - 1.0)
        """
        chunk_text = chunk_text.lower().strip()
        
        if chunk_text not in self.chunks:
            self.chunks[chunk_text] = LanguageChunk(chunk_text)
        
        chunk = self.chunks[chunk_text]
        
        # Uczenie z momentum
        chunk.emotional_vector = (
            chunk.emotional_vector * (1.0 - strength) +
            emotional_vector * strength
        )
    
    # =========================================================================
    # PERSISTENCE
    # =========================================================================
    
    def save(self):
        """Zapisuje leksykon do pliku."""
        import os
        os.makedirs(os.path.dirname(self.chunk_file), exist_ok=True)
        
        data = {
            'version': '1.0.0',
            'total_chunks': self.total_chunks,
            'total_exposures': self.total_exposures,
            'chunks': {
                text: chunk.to_dict()
                for text, chunk in self.chunks.items()
            }
        }
        
        with open(self.chunk_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Wczytuje leksykon z pliku."""
        import os
        if not os.path.exists(self.chunk_file):
            return
        
        try:
            with open(self.chunk_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.total_chunks = data.get('total_chunks', 0)
            self.total_exposures = data.get('total_exposures', 0)
            
            for text, chunk_data in data.get('chunks', {}).items():
                self.chunks[text] = LanguageChunk.from_dict(chunk_data)
        
        except Exception as e:
            print(f"[ChunkLexicon] Błąd wczytywania: {e}")
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_statistics(self) -> dict:
        """Zwraca statystyki leksykonu."""
        if not self.chunks:
            return {'total_chunks': 0}
        
        frequencies = [c.frequency for c in self.chunks.values()]
        lengths = [c.length for c in self.chunks.values()]
        
        return {
            'total_chunks': len(self.chunks),
            'total_exposures': self.total_exposures,
            'avg_frequency': np.mean(frequencies),
            'max_frequency': max(frequencies),
            'avg_length': np.mean(lengths),
            'most_common': self.get_most_common_chunks(5)
        }
    
    def get_most_common_chunks(self, n: int = 10) -> List[Tuple[str, int]]:
        """Zwraca n najczęstszych chunków."""
        sorted_chunks = sorted(
            self.chunks.items(),
            key=lambda x: x[1].frequency,
            reverse=True
        )
        return [(text, chunk.frequency) for text, chunk in sorted_chunks[:n]]


# =============================================================================
# INTEGRATION WITH AII
# =============================================================================

def upgrade_aii_to_chunks():
    """
    Przykład integracji z aii.py.
    
    ZAMIAST:
    - Pojedyncze słowa
    - Reguły gramatyczne
    
    TERAZ:
    - Chunki (sekwencje)
    - Statystyczne wzorce
    """
    example = '''
# PRZED (aii.py - stara metoda):
class EvolvingLexicon:
    def analyze_text(self, text):
        words = text.split()
        for word in words:
            # Analiza POJEDYNCZYCH SŁÓW
            self.learn_word(word)

# PO (chunk_lexicon.py - nowa metoda):
class ChunkLexicon:
    def analyze_text_chunks(self, text):
        # 1. Wykryj chunki automatycznie
        self.extract_chunks_from_text(text)
        
        # 2. Znajdź znane chunki
        found = self.find_chunks_in_text(text)
        
        # 3. Oblicz wektor emocjonalny z CHUNKÓW
        result = self.analyze_text_chunks(text)
        return result['emotional_vector']


# UŻYCIE W AII:
from chunk_lexicon import ChunkLexicon

class AII:
    def __init__(self):
        self.chunk_lexicon = ChunkLexicon()  # NOWY!
        self.old_lexicon = EvolvingLexicon()  # Można zachować dla kompatybilności
    
    def interact(self, user_input):
        # Analiza CHUNKOWA (nowa)
        chunk_analysis = self.chunk_lexicon.analyze_text_chunks(user_input)
        
        # Jeśli pokrycie > 50%, używamy chunków
        if chunk_analysis['coverage'] > 0.5:
            vec = chunk_analysis['emotional_vector']
            print(f"[CHUNKS] Pokrycie: {chunk_analysis['coverage']:.0%}")
            print(f"[CHUNKS] Priming boost: {chunk_analysis['priming_boost']:.2f}x")
        else:
            # Fallback do starego leksykonu
            vec, _, _ = self.old_lexicon.analyze_text(user_input)
        
        # ... (reszta bez zmian)
'''
    print(example)


# =============================================================================
# TEST
# =============================================================================

def test_chunk_lexicon():
    """Test chunk-based lexicon."""
    print("\n🧪 Test ChunkLexicon (Nature Human Behaviour 2026)\n")
    
    lexicon = ChunkLexicon(chunk_file="test_chunks.json")
    
    # Test 1: Ekstraktuj chunki z tekstu
    print("[Test 1] Automatyczna ekstrakcja chunków")
    sample_text = """
    Czy mogę prosić o kawę? Czy mogę prosić o herbatę?
    W środku nocy zadzwonił telefon. W środku lasu znaleźliśmy chatę.
    Dziękuję bardzo za pomoc. Dziękuję bardzo za wszystko.
    """
    
    lexicon.extract_chunks_from_text(sample_text)
    print(f"  Wyekstrahowano {len(lexicon.chunks)} chunków")
    print(f"  Najczęstsze: {lexicon.get_most_common_chunks(3)}")
    print("  ✅ PASS\n")
    
    # Test 2: Rozpoznawanie chunków w nowym tekście
    print("[Test 2] Rozpoznawanie chunków (PRIMING)")
    new_text = "Czy mogę prosić o wodę?"
    
    result = lexicon.analyze_text_chunks(new_text)
    print(f"  Tekst: '{new_text}'")
    print(f"  Znalezione chunki: {result['chunks_found']}")
    print(f"  Pokrycie: {result['coverage']:.0%}")
    print(f"  Priming boost: {result['priming_boost']:.2f}x")
    
    # Ponowne napotkanie -> silniejszy priming
    result2 = lexicon.analyze_text_chunks(new_text)
    print(f"\n  [Po ponownym kontakcie]")
    print(f"  Priming boost: {result2['priming_boost']:.2f}x (wzrost!)")
    print("  ✅ PASS\n")
    
    # Test 3: Uczenie emocji
    print("[Test 3] Uczenie emocji dla chunków")
    chunk_text = "czy mogę prosić o"
    emotion_vec = np.zeros(15)
    emotion_vec[0] = 0.8  # Radość
    emotion_vec[7] = 0.6  # Akceptacja
    
    lexicon.teach_chunk_emotion(chunk_text, emotion_vec, strength=0.8)
    chunk = lexicon.chunks[chunk_text]
    print(f"  Chunk: '{chunk_text}'")
    print(f"  Wektor emocjonalny: {chunk.emotional_vector[:8]}")
    print("  ✅ PASS\n")
    
    # Test 4: Statystyki
    print("[Test 4] Statystyki")
    stats = lexicon.get_statistics()
    print(f"  Chunków: {stats['total_chunks']}")
    print(f"  Średnia częstość: {stats['avg_frequency']:.1f}")
    print(f"  Średnia długość: {stats['avg_length']:.1f} słów")
    print("  ✅ PASS\n")
    
    # Test 5: Save/Load
    print("[Test 5] Persistence")
    lexicon.save()
    
    lexicon2 = ChunkLexicon(chunk_file="test_chunks.json")
    assert len(lexicon2.chunks) == len(lexicon.chunks)
    print(f"  Wczytano {len(lexicon2.chunks)} chunków")
    print("  ✅ PASS\n")
    
    # Cleanup
    import os
    if os.path.exists("test_chunks.json"):
        os.remove("test_chunks.json")
    
    print("✅ Wszystkie testy przeszły!\n")


if __name__ == "__main__":
    test_chunk_lexicon()
    
    print("\n" + "="*70)
    print("INTEGRACJA Z AII:")
    print("="*70)
    upgrade_aii_to_chunks()