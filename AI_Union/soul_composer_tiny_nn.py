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


# (Pozostałe klasy TinyMelodyNet, TinyTriadNet, TinyDiversityNet – bez zmian, kopiuj z oryginalnego)

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
    
    # (Pozostałe metody _count_params, _print_stats, _try_load_models, save_models – bez zmian)

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
        Przewiduje następny akord z dynamiczną temperaturą.
        """
        emotions = self._emotions_to_vector(metrics)
        
        # One-hot poprzedniego akordu
        prev_onehot = np.zeros(8)
        prev_onehot[prev_chord_idx] = 1.0
        
        # Forward pass
        logits = self.chord_net.forward(emotions, prev_onehot)
        
        # DYNAMICZNA TEMPERATURA
        chaos_val = metrics.get('chaos', 0.0)
        kreacja_val = metrics.get('kreacja', 0.0)
        temperature = 0.8 + 0.8 * (chaos_val / 9.0) + 0.4 * (kreacja_val / 9.0)
        
        # Temperature sampling
        probs = softmax(logits, temperature)
        next_chord_idx = np.random.choice(8, p=probs)
        
        # Mapuj na konkretny akord
        chord_type = self.CHORD_TYPES[next_chord_idx]
        
        # Root offsets - muzycznie sensowne przejścia (tu dokończ z oryginalnego kodu)
        # ...
        
        return next_chord_idx, chord_type

    # Dodaj podobne dynamiczne temperature do innych predict_* metod (melody, triad itp.)
