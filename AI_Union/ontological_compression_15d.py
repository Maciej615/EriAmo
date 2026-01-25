# -*- coding: utf-8 -*-
"""
ontological_compression_15d.py
Moduł odpowiedzialny za weryfikację kompresji ontologicznej w przestrzeni 15D/21D.
"""

import numpy as np

class OntologicalCompressor:
    """
    Sprawdza, czy nowy bodziec (F) jest 'kompresją' obecnego stanu (S),
    czyli czy leży na tej samej trajektorii w przestrzeni wielowymiarowej.
    """

    # Skalibrowane progi (z testów v8.1)
    THRESHOLD_COMPRESSION = 0.995  # Tożsamość (prawie ten sam kierunek)
    THRESHOLD_HARMONY     = 0.800  # Zbieżność (podobny kierunek)
    THRESHOLD_NOVELTY     = 0.400  # Nowość (inny kierunek)
    # Poniżej 0.0 to Konflikt (przeciwny kierunek)

    def __init__(self, current_vector):
        """
        Inicjalizuje kompresor obecnym stanem bytu (S).
        Args:
            current_vector (np.array): Wektor stanu (15D lub 21D).
        """
        if current_vector is None:
            self.S = np.zeros(15) 
        else:
            self.S = np.array(current_vector)
            
        # Normalizacja S
        norm_S = np.linalg.norm(self.S)
        if norm_S > 1e-9:
            self.S_norm = self.S / norm_S
            self.S_len = norm_S
        else:
            self.S_norm = np.zeros_like(self.S)
            self.S_len = 0.0

    def check_compression(self, F_vector):
        """
        Sprawdza relację między wektorem wpływu (F) a stanem (S).
        Returns: (is_compressed: bool, cos_alpha: float)
        """
        F = np.array(F_vector)
        
        # Zabezpieczenie wymiarów (padding zerami)
        if len(F) < len(self.S):
            F = np.pad(F, (0, len(self.S) - len(F)), 'constant')
        elif len(F) > len(self.S):
            # Tymczasowe rozszerzenie S
            padded_S = np.pad(self.S_norm, (0, len(F) - len(self.S)), 'constant')
            norm_F = np.linalg.norm(F)
            if norm_F < 1e-9: return False, 0.0
            cos_alpha = np.dot(padded_S, F) / norm_F
            return cos_alpha >= self.THRESHOLD_COMPRESSION, cos_alpha

        norm_F = np.linalg.norm(F)
        if norm_F < 1e-9 or self.S_len < 1e-9:
            return False, 0.0

        cos_alpha = np.dot(self.S_norm, F) / norm_F
        cos_alpha = max(-1.0, min(1.0, cos_alpha))

        return cos_alpha >= self.THRESHOLD_COMPRESSION, cos_alpha

    def interpret_alignment(self, cos_alpha):
        """Zwraca tekstową interpretację wartości cosinus alpha."""
        if cos_alpha >= self.THRESHOLD_COMPRESSION:
            return "KOMPRESJA (Tożsamość)"
        elif cos_alpha >= self.THRESHOLD_HARMONY:
            return "HARMONIA (Zbieżność)"
        elif abs(cos_alpha) < self.THRESHOLD_NOVELTY:
            return "NOWOŚĆ (Ortogonalność)"
        elif cos_alpha < -0.8:
            return "KONFLIKT (Przeciwieństwo)"
        else:
            return "DYZONANS (Rozbieżność)"