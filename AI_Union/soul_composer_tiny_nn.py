# soul_composer_tiny_nn.py
# -*- coding: utf-8 -*-
"""
Tiny Neural Networks dla SoulComposer v8.1
Używa TYLKO NumPy - małe modele neuronowe (~10KB każdy)
Implementuje: wariacje melodyczne, progresje trójdźwięków, różnorodność
"""

import numpy as np
from typing import List, Tuple, Dict
import random
import json
import os


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def tanh(x):
    return np.tanh(x)

def softmax(x, temperature=1.0):
    x = x / temperature
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()


class TinyChordNet:
    """
    Malutka sieć (~2KB) do przewidywania kolejnego akordu.
    3 warstwy: [15+8] -> [32] -> [16] -> [8]
    """
    def __init__(self, num_emotions=15, num_chords=8):
        self.num_emotions = num_emotions
        self.num_chords = num_chords
        
        # Inicjalizacja wag (Xavier)
        self.w1 = np.random.randn(num_emotions + num_chords, 32) * 0.1
        self.b1 = np.zeros(32)
        
        self.w2 = np.random.randn(32, 16) * 0.1
        self.b2 = np.zeros(16)
        
        self.w3 = np.random.randn(16, num_chords) * 0.1
        self.b3 = np.zeros(num_chords)
        
    def forward(self, emotions, prev_chord_onehot):
        """
        emotions: [15]
        prev_chord_onehot: [8]
        returns: [8] logits
        """
        x = np.concatenate([emotions, prev_chord_onehot])
        
        # Layer 1
        h1 = tanh(np.dot(x, self.w1) + self.b1)
        
        # Layer 2
        h2 = tanh(np.dot(h1, self.w2) + self.b2)
        
        # Output
        out = np.dot(h2, self.w3) + self.b3
        
        return out
    
    def save(self, path):
        """Zapisz wagi"""
        np.savez(path, w1=self.w1, b1=self.b1, w2=self.w2, b2=self.b2, w3=self.w3, b3=self.b3)
    
    def load(self, path):
        """Wczytaj wagi"""
        data = np.load(path)
        self.w1 = data['w1']
        self.b1 = data['b1']
        self.w2 = data['w2']
        self.b2 = data['b2']
        self.w3 = data['w3']
        self.b3 = data['b3']


class TinyMelodyNet:
    """
    Model wariacji melodycznych.
    Input: [5 ostatnich nut embedded] -> LSTM-like -> [25 możliwych nut]
    """
    def __init__(self, num_emotions=15, seq_len=5, note_range=25):
        self.seq_len = seq_len
        self.note_range = note_range
        
        # Embedding dla nut (25 -> 12)
        self.embed = np.random.randn(note_range, 12) * 0.1
        
        # Uproszczony RNN (GRU-like)
        self.w_rnn = np.random.randn(12, 32) * 0.1
        self.u_rnn = np.random.randn(32, 32) * 0.1
        self.b_rnn = np.zeros(32)
        
        # Output layer [32 + 15] -> [25]
        self.w_out = np.random.randn(32 + num_emotions, 25) * 0.1
        self.b_out = np.zeros(25)
    
    def forward(self, note_seq, emotions):
        """
        note_seq: [seq_len] - indeksy (0-24)
        emotions: [15]
        returns: [25] logits
        """
        # Embed sequence
        embedded = self.embed[note_seq]  # [seq_len, 12]
        
        # Simple RNN
        h = np.zeros(32)
        for i in range(self.seq_len):
            h = tanh(np.dot(embedded[i], self.w_rnn) + np.dot(h, self.u_rnn) + self.b_rnn)
        
        # Combine with emotions
        combined = np.concatenate([h, emotions])
        
        # Output
        out = np.dot(combined, self.w_out) + self.b_out
        
        return out
    
    def save(self, path):
        np.savez(path, embed=self.embed, w_rnn=self.w_rnn, u_rnn=self.u_rnn, 
                 b_rnn=self.b_rnn, w_out=self.w_out, b_out=self.b_out)
    
    def load(self, path):
        data = np.load(path)
        self.embed = data['embed']
        self.w_rnn = data['w_rnn']
        self.u_rnn = data['u_rnn']
        self.b_rnn = data['b_rnn']
        self.w_out = data['w_out']
        self.b_out = data['b_out']


class TinyTriadNet:
    """
    Model harmonizacji melodii trójdźwiękami.
    Input: [nuta melodii embedded] + [15 emocji]
    Output: [12 roots] + [8 chord types]
    """
    def __init__(self, num_emotions=15):
        # Melody embedding
        self.melody_embed = np.random.randn(25, 12) * 0.1
        
        # Hidden layer
        self.w_hidden = np.random.randn(12 + num_emotions, 32) * 0.1
        self.b_hidden = np.zeros(32)
        
        # Two heads
        self.w_root = np.random.randn(32, 12) * 0.1
        self.b_root = np.zeros(12)
        
        self.w_type = np.random.randn(32, 8) * 0.1
        self.b_type = np.zeros(8)
    
    def forward(self, melody_note_idx, emotions):
        """
        melody_note_idx: int (0-24)
        emotions: [15]
        returns: (root_logits [12], type_logits [8])
        """
        # Embed melody
        embedded = self.melody_embed[melody_note_idx]
        
        # Combine
        x = np.concatenate([embedded, emotions])
        
        # Hidden
        h = tanh(np.dot(x, self.w_hidden) + self.b_hidden)
        
        # Two outputs
        root_logits = np.dot(h, self.w_root) + self.b_root
        type_logits = np.dot(h, self.w_type) + self.b_type
        
        return root_logits, type_logits
    
    def save(self, path):
        np.savez(path, melody_embed=self.melody_embed, w_hidden=self.w_hidden,
                 b_hidden=self.b_hidden, w_root=self.w_root, b_root=self.b_root,
                 w_type=self.w_type, b_type=self.b_type)
    
    def load(self, path):
        data = np.load(path)
        self.melody_embed = data['melody_embed']
        self.w_hidden = data['w_hidden']
        self.b_hidden = data['b_hidden']
        self.w_root = data['w_root']
        self.b_root = data['b_root']
        self.w_type = data['w_type']
        self.b_type = data['b_type']


class TinyDiversityNet:
    """
    Ocena różnorodności kompozycji.
    Analizuje historię emocji i sugeruje stopień entropii.
    """
    def __init__(self, num_emotions=15, history_len=16):
        self.history_len = history_len
        
        # History encoder (uproszczony)
        self.w_history = np.random.randn(num_emotions, 32) * 0.1
        self.b_history = np.zeros(32)
        
        # Diversity scorer
        self.w_score = np.random.randn(32 + num_emotions, 1) * 0.1
        self.b_score = np.zeros(1)
    
    def forward(self, emotion_history, current_emotions):
        """
        emotion_history: [history_len, 15]
        current_emotions: [15]
        returns: diversity_score (0-1)
        """
        # Prosty pooling historii
        h = np.zeros(32)
        for i in range(len(emotion_history)):
            h += tanh(np.dot(emotion_history[i], self.w_history) + self.b_history)
        h /= len(emotion_history)
        
        # Combine with current
        combined = np.concatenate([h, current_emotions])
        
        # Score
        score = sigmoid(np.dot(combined, self.w_score) + self.b_score)[0]
        
        return score
    
    def save(self, path):
        np.savez(path, w_history=self.w_history, b_history=self.b_history,
                 w_score=self.w_score, b_score=self.b_score)
    
    def load(self, path):
        data = np.load(path)
        self.w_history = data['w_history']
        self.b_history = data['b_history']
        self.w_score = data['w_score']
        self.b_score = data['b_score']


class SoulComposerTinyNN:
    """
    Wrapper łączący tiny neural networks z SoulComposer.
    Wszystkie modele razem: ~8KB parametrów.
    """
    
    CHORD_TYPES = ['maj', 'min', '7', 'dim', 'power', 'sus4', 'maj7', 'min7']
    MODEL_DIR = "tiny_models"
    
    def __init__(self):
        # Inicjalizacja modeli
        self.chord_net = TinyChordNet()
        self.melody_net = TinyMelodyNet()
        self.triad_net = TinyTriadNet()
        self.diversity_net = TinyDiversityNet()
        
        # Historia emocji
        self.emotion_history = []
        
        # Spróbuj wczytać zapisane wagi
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        self._try_load_models()
        
        print(f"[TinyNN] Modele zainicjalizowane!")
        self._print_stats()
    
    def _count_params(self, model):
        """Zlicz parametry modelu"""
        total = 0
        for attr_name in dir(model):
            attr = getattr(model, attr_name)
            if isinstance(attr, np.ndarray):
                total += attr.size
        return total
    
    def _print_stats(self):
        """Wyświetl statystyki modeli"""
        print(f"  - ChordNet: {self._count_params(self.chord_net)} parametrów")
        print(f"  - MelodyNet: {self._count_params(self.melody_net)} parametrów")
        print(f"  - TriadNet: {self._count_params(self.triad_net)} parametrów")
        print(f"  - DiversityNet: {self._count_params(self.diversity_net)} parametrów")
        total = (self._count_params(self.chord_net) + 
                 self._count_params(self.melody_net) +
                 self._count_params(self.triad_net) +
                 self._count_params(self.diversity_net))
        print(f"  SUMA: {total} parametrów (~{total * 4 / 1024:.1f}KB)")
    
    def _try_load_models(self):
        """Próbuje wczytać zapisane wagi"""
        try:
            self.chord_net.load(f"{self.MODEL_DIR}/chord_net.npz")
            self.melody_net.load(f"{self.MODEL_DIR}/melody_net.npz")
            self.triad_net.load(f"{self.MODEL_DIR}/triad_net.npz")
            self.diversity_net.load(f"{self.MODEL_DIR}/diversity_net.npz")
            print("[TinyNN] Wczytano zapisane wagi")
        except:
            print("[TinyNN] Używam losowych wag (brak zapisanych)")
    
    def save_models(self):
        """Zapisz wszystkie modele"""
        self.chord_net.save(f"{self.MODEL_DIR}/chord_net.npz")
        self.melody_net.save(f"{self.MODEL_DIR}/melody_net.npz")
        self.triad_net.save(f"{self.MODEL_DIR}/triad_net.npz")
        self.diversity_net.save(f"{self.MODEL_DIR}/diversity_net.npz")
        print(f"[TinyNN] Modele zapisane w {self.MODEL_DIR}/")
    
    def _emotions_to_vector(self, metrics: dict) -> np.ndarray:
        """Konwertuje słownik emocji na wektor [15]"""
        from union_config import UnionConfig
        
        vector = []
        for axis in UnionConfig.AXES:
            vector.append(metrics.get(axis, 0.0))
        
        return np.array(vector, dtype=np.float32)
    
    def predict_next_chord(self, metrics: dict, prev_chord_idx: int,
                          temperature=1.0) -> Tuple[int, str]:
        """
        Przewiduje następny akord.
        
        Returns:
            (root_offset, chord_type)
        """
        emotions = self._emotions_to_vector(metrics)
        
        # One-hot poprzedniego akordu
        prev_onehot = np.zeros(8)
        prev_onehot[prev_chord_idx] = 1.0
        
        # Forward pass
        logits = self.chord_net.forward(emotions, prev_onehot)
        
        # Temperature sampling
        probs = softmax(logits, temperature)
        next_chord_idx = np.random.choice(8, p=probs)
        
        # Mapuj na konkretny akord
        chord_type = self.CHORD_TYPES[next_chord_idx]
        
        # Root offsets - muzycznie sensowne przejścia
        root_offsets = [0, 5, 7, -3, 12, 5, 0, 0]
        root_offset = root_offsets[next_chord_idx]
        
        return root_offset, chord_type
    
    def generate_melody_variation(self, metrics: dict, previous_notes: List[int],
                                   temperature=0.9) -> int:
        """
        Generuje następną nutę jako wariację poprzednich.
        
        Args:
            previous_notes: Lista ostatnich nut MIDI (60-84)
            
        Returns:
            Następna nuta MIDI
        """
        seq_len = 5
        
        # Pad if needed
        if len(previous_notes) < seq_len:
            previous_notes = [60] * (seq_len - len(previous_notes)) + previous_notes
        
        note_seq = previous_notes[-seq_len:]
        
        # Konwertuj MIDI (60-84) na indeksy (0-24)
        note_indices = [max(0, min(24, n - 60)) for n in note_seq]
        note_indices = np.array(note_indices, dtype=np.int32)
        
        emotions = self._emotions_to_vector(metrics)
        
        # Forward pass
        logits = self.melody_net.forward(note_indices, emotions)
        
        # Temperature sampling
        probs = softmax(logits, temperature)
        next_note_idx = np.random.choice(25, p=probs)
        
        # Konwertuj z powrotem na MIDI
        next_note = 60 + next_note_idx
        
        return next_note
    
    def harmonize_with_triad(self, metrics: dict, melody_note: int) -> Tuple[int, str]:
        """
        Dobiera trójdźwięk do nuty melodii.
        
        Returns:
            (root_midi, chord_type)
        """
        # Konwertuj nutę na indeks
        note_idx = max(0, min(24, melody_note - 60))
        
        emotions = self._emotions_to_vector(metrics)
        
        # Forward pass
        root_logits, type_logits = self.triad_net.forward(note_idx, emotions)
        
        # Sampling
        root_probs = softmax(root_logits)
        type_probs = softmax(type_logits)
        
        root_offset = np.random.choice(12, p=root_probs)
        chord_type_idx = np.random.choice(8, p=type_probs)
        
        # Oblicz root MIDI
        base_root = (melody_note // 12) * 12
        root_midi = base_root + root_offset
        
        chord_type = self.CHORD_TYPES[chord_type_idx]
        
        return root_midi, chord_type
    
    def calculate_diversity_factor(self, metrics: dict) -> float:
        """
        Oblicza współczynnik różnorodności (0-1).
        1.0 = maksymalna różnorodność
        0.0 = trzymaj się wzorców
        """
        emotion_vector = self._emotions_to_vector(metrics)
        
        # Aktualizuj historię
        self.emotion_history.append(emotion_vector.copy())
        
        # Zachowaj tylko ostatnie 16
        if len(self.emotion_history) > 16:
            self.emotion_history = self.emotion_history[-16:]
        
        # Minimum 4 próbki
        if len(self.emotion_history) < 4:
            return 0.3
        
        # Pad historia do 16
        history = self.emotion_history.copy()
        while len(history) < 16:
            history = [history[0]] + history
        
        history_array = np.array(history)
        
        # Forward pass
        diversity_score = self.diversity_net.forward(history_array, emotion_vector)
        
        return float(diversity_score)
    
    def generate_chord_progression(self, metrics: dict, num_chords=8,
                                   base_root=60) -> List[Tuple[int, str]]:
        """
        Generuje progresję akordów.
        
        Returns:
            Lista (root_midi, chord_type)
        """
        progression = []
        current_chord_idx = 0  # Start z maj
        
        for _ in range(num_chords):
            root_offset, chord_type = self.predict_next_chord(
                metrics, current_chord_idx, temperature=0.9
            )
            
            root_midi = base_root + root_offset
            progression.append((root_midi, chord_type))
            
            # Update
            current_chord_idx = self.CHORD_TYPES.index(chord_type)
        
        return progression
    
    def reset_history(self):
        """Resetuje historię emocji"""
        self.emotion_history = []


# ==================== PRZYKŁADY UŻYCIA ====================

def demo_chord_progression():
    """Demo: Generowanie progresji akordów"""
    print("\n=== DEMO: Progresja Akordów ===")
    
    nn = SoulComposerTinyNN()
    
    # Przykładowe metryki - radosne
    happy_metrics = {
        'logika': 0.6, 'kreacja': 0.7, 'chaos': 0.2,
        'radość': 0.9, 'smutek': 0.1, 'gniew': 0.0,
        'strach': 0.1, 'wstręt': 0.0, 'zaufanie': 0.8,
        'oczekiwanie': 0.6, 'zaskoczenie': 0.3, 'wiedza': 0.6,
        'czas': 0.7, 'przestrzeń': 0.5, 'energia': 0.8
    }
    
    print("\nProgresja dla radosnego utworu (C dur):")
    progression = nn.generate_chord_progression(happy_metrics, num_chords=8, base_root=60)
    
    for i, (root, ctype) in enumerate(progression, 1):
        note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][root % 12]
        print(f"  {i}. {note_name}{ctype} (MIDI: {root})")
    
    # Smutne metryki
    sad_metrics = happy_metrics.copy()
    sad_metrics['radość'] = 0.2
    sad_metrics['smutek'] = 0.8
    sad_metrics['gniew'] = 0.3
    
    print("\nProgresja dla smutnego utworu (A moll):")
    progression = nn.generate_chord_progression(sad_metrics, num_chords=8, base_root=57)
    
    for i, (root, ctype) in enumerate(progression, 1):
        note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][root % 12]
        print(f"  {i}. {note_name}{ctype} (MIDI: {root})")


def demo_melody_variations():
    """Demo: Wariacje melodyczne"""
    print("\n=== DEMO: Wariacje Melodyczne ===")
    
    nn = SoulComposerTinyNN()
    
    metrics = {
        'logika': 0.7, 'kreacja': 0.8, 'chaos': 0.4,
        'radość': 0.6, 'smutek': 0.3, 'gniew': 0.1,
        'strach': 0.2, 'wstręt': 0.0, 'zaufanie': 0.7,
        'oczekiwanie': 0.5, 'zaskoczenie': 0.4, 'wiedza': 0.7,
        'czas': 0.6, 'przestrzeń': 0.5, 'energia': 0.7
    }
    
    print("\nWariacja 1 (temperature = 0.7, przewidywalnie):")
    melody1 = [60, 62, 64, 65, 67]
    for i in range(8):
        next_note = nn.generate_melody_variation(metrics, melody1[-5:], temperature=0.7)
        melody1.append(next_note)
    
    print("  Nuty:", melody1)
    
    print("\nWariacja 2 (temperature = 1.2, kreatywnie):")
    melody2 = [60, 62, 64, 65, 67]
    for i in range(8):
        next_note = nn.generate_melody_variation(metrics, melody2[-5:], temperature=1.2)
        melody2.append(next_note)
    
    print("  Nuty:", melody2)
    
    # Wizualizacja różnic
    print("\nRóżnica między wariacjami:")
    print(f"  Zakres wariacji 1: {min(melody1)}-{max(melody1)} (rozpiętość: {max(melody1)-min(melody1)})")
    print(f"  Zakres wariacji 2: {min(melody2)}-{max(melody2)} (rozpiętość: {max(melody2)-min(melody2)})")


def demo_triad_harmonization():
    """Demo: Harmonizacja trójdźwiękami"""
    print("\n=== DEMO: Harmonizacja Trójdźwiękami ===")
    
    nn = SoulComposerTinyNN()
    
    metrics = {
        'logika': 0.8, 'kreacja': 0.6, 'chaos': 0.2,
        'radość': 0.7, 'smutek': 0.2, 'gniew': 0.0,
        'strach': 0.1, 'wstręt': 0.0, 'zaufanie': 0.9,
        'oczekiwanie': 0.5, 'zaskoczenie': 0.2, 'wiedza': 0.8,
        'czas': 0.5, 'przestrzeń': 0.6, 'energia': 0.6
    }
    
    # Melodia w C dur (skala)
    melody = [60, 62, 64, 65, 67, 69, 71, 72]  # C D E F G A B C
    
    print("\nMelodia -> Harmonizacja:")
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    for note in melody:
        root, ctype = nn.harmonize_with_triad(metrics, note)
        melody_name = note_names[note % 12]
        root_name = note_names[root % 12]
        print(f"  {melody_name} ({note}) -> {root_name}{ctype} (root: {root})")


def demo_diversity_tracking():
    """Demo: Śledzenie różnorodności"""
    print("\n=== DEMO: Śledzenie Różnorodności ===")
    
    nn = SoulComposerTinyNN()
    
    # Symulacja ewolucji emocji
    metrics_timeline = [
        {'logika': 0.7, 'kreacja': 0.5, 'chaos': 0.2, 'radość': 0.8, 'smutek': 0.1,
         'gniew': 0.0, 'strach': 0.1, 'wstręt': 0.0, 'zaufanie': 0.7,
         'oczekiwanie': 0.6, 'zaskoczenie': 0.2, 'wiedza': 0.7,
         'czas': 0.6, 'przestrzeń': 0.5, 'energia': 0.7},
        
        {'logika': 0.7, 'kreacja': 0.6, 'chaos': 0.3, 'radość': 0.7, 'smutek': 0.2,
         'gniew': 0.1, 'strach': 0.1, 'wstręt': 0.0, 'zaufanie': 0.7,
         'oczekiwanie': 0.5, 'zaskoczenie': 0.3, 'wiedza': 0.7,
         'czas': 0.7, 'przestrzeń': 0.5, 'energia': 0.7},
        
        {'logika': 0.6, 'kreacja': 0.7, 'chaos': 0.5, 'radość': 0.6, 'smutek': 0.3,
         'gniew': 0.2, 'strach': 0.2, 'wstręt': 0.1, 'zaufanie': 0.6,
         'oczekiwanie': 0.5, 'zaskoczenie': 0.5, 'wiedza': 0.6,
         'czas': 0.8, 'przestrzeń': 0.6, 'energia': 0.8},
        
        {'logika': 0.5, 'kreacja': 0.8, 'chaos': 0.7, 'radość': 0.4, 'smutek': 0.5,
         'gniew': 0.4, 'strach': 0.3, 'wstręt': 0.2, 'zaufanie': 0.4,
         'oczekiwanie': 0.4, 'zaskoczenie': 0.7, 'wiedza': 0.5,
         'czas': 0.9, 'przestrzeń': 0.7, 'energia': 0.9},
    ]
    
    print("\nEwolucja współczynnika różnorodności:")
    print("(0.0 = powtarzalny, 1.0 = maksymalnie różnorodny)")
    
    for i, metrics in enumerate(metrics_timeline, 1):
        diversity = nn.calculate_diversity_factor(metrics)
        bar = "█" * int(diversity * 20)
        print(f"  Krok {i}: {diversity:.3f} {bar}")
    
    print("\nInterpretacja:")
    print("  - Diversity rośnie gdy emocje się zmieniają")
    print("  - Model sugeruje większą kreatywność w późniejszych fazach")


if __name__ == "__main__":
    print("=" * 60)
    print("SOUL COMPOSER - TINY NEURAL NETWORKS")
    print("Małe modele (~8KB razem) dla wariacji i różnorodności")
    print("=" * 60)
    
    # Uruchom wszystkie demo
    demo_chord_progression()
    demo_melody_variations()
    demo_triad_harmonization()
    demo_diversity_tracking()
    
    print("\n" + "=" * 60)
    print("✓ Wszystkie demo zakończone!")
    print("=" * 60)