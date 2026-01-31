# visualizer.py v3.0.0 [15-AXES MODEL]
# -*- coding: utf-8 -*-
"""
Wizualizator Stanu Emocjonalnego EriAmo Union v3.0.0

Pełna migracja do modelu 15-osiowego:
- 8 osi Plutchika (biologiczne): radość, smutek, strach, gniew, miłość, wstręt, zaskoczenie, akceptacja
- 7 osi metafizycznych: logika, wiedza, czas, kreacja, byt, przestrzeń, chaos
"""

import numpy as np
from typing import Optional, List, Tuple
from union_config import AXES, DIMENSION, EPHEMERAL_AXES, PERSISTENT_AXES, Colors


class EmotionVisualizer:
    """
    Wizualizacja stanu 15-wymiarowego rdzenia EriAmo.
    Obsługuje wyświetlanie tekstowe (terminal) i generowanie danych do GUI.
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PALETA KOLORÓW DLA 15 OSI
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Kolory ANSI dla terminala
    AXIS_COLORS_ANSI = {
        # Plutchik (0-7)
        'radość':     '\033[93m',   # Jasny żółty
        'smutek':     '\033[34m',   # Niebieski
        'strach':     '\033[35m',   # Magenta
        'gniew':      '\033[91m',   # Czerwony
        'miłość':     '\033[95m',   # Jasny magenta / Różowy
        'wstręt':     '\033[32m',   # Zielony (jak w Pixar)
        'zaskoczenie': '\033[96m',  # Cyjan
        'akceptacja': '\033[92m',   # Jasny zielony
        
        # Metafizyczne (8-14)
        'logika':     '\033[97m',   # Biały
        'wiedza':     '\033[33m',   # Żółty/złoty
        'czas':       '\033[90m',   # Szary
        'kreacja':    '\033[94m',   # Jasny niebieski
        'byt':        '\033[37m',   # Jasny szary
        'przestrzeń': '\033[36m',   # Cyjan
        'chaos':      '\033[31m',   # Ciemny czerwony
    }
    
    # Kolory RGB dla GUI (0-255)
    AXIS_COLORS_RGB = {
        # Plutchik (0-7)
        'radość':     (255, 223, 0),    # Złoty
        'smutek':     (65, 105, 225),   # Royal Blue
        'strach':     (138, 43, 226),   # Blue Violet
        'gniew':      (220, 20, 60),    # Crimson
        'miłość':     (255, 105, 180),  # Hot Pink
        'wstręt':     (0, 128, 0),      # Green
        'zaskoczenie': (0, 206, 209),   # Dark Turquoise
        'akceptacja': (144, 238, 144),  # Light Green
        
        # Metafizyczne (8-14)
        'logika':     (245, 245, 245),  # White Smoke
        'wiedza':     (218, 165, 32),   # Goldenrod
        'czas':       (128, 128, 128),  # Gray
        'kreacja':    (100, 149, 237),  # Cornflower Blue
        'byt':        (210, 180, 140),  # Tan
        'przestrzeń': (72, 209, 204),   # Medium Turquoise
        'chaos':      (139, 0, 0),      # Dark Red
    }
    
    # Symbole dla każdej osi (do wizualizacji tekstowej)
    AXIS_SYMBOLS = {
        'radość':     '☀',
        'smutek':     '☁',
        'strach':     '⚡',
        'gniew':      '🔥',
        'miłość':     '♥',
        'wstręt':     '☠',
        'zaskoczenie': '✦',
        'akceptacja': '☮',
        'logika':     '⚙',
        'wiedza':     '📚',
        'czas':       '⏰',
        'kreacja':    '✨',
        'byt':        '●',
        'przestrzeń': '◉',
        'chaos':      '∞',
    }

    def __init__(self, core=None, width: int = 40):
        """
        Args:
            core: Referencja do EriAmoCore (opcjonalna)
            width: Szerokość paska wizualizacji
        """
        self.core = core
        self.bar_width = width

    def get_state_vector(self) -> np.ndarray:
        """Pobiera wektor stanu z rdzenia lub zwraca zerowy."""
        if self.core and hasattr(self.core, 'state'):
            return np.array(self.core.state)
        return np.zeros(DIMENSION)

    def visualize_bar(self, value: float, max_val: float = 100.0, 
                      color: str = Colors.WHITE) -> str:
        """
        Generuje pasek wizualizacji dla pojedynczej wartości.
        
        Args:
            value: Aktualna wartość
            max_val: Wartość maksymalna (dla normalizacji)
            color: Kod koloru ANSI
            
        Returns:
            str: Pasek ASCII z kolorem
        """
        normalized = min(abs(value) / max_val, 1.0)
        filled = int(normalized * self.bar_width)
        
        if value >= 0:
            bar = '█' * filled + '░' * (self.bar_width - filled)
        else:
            # Ujemne wartości - odwrócony pasek
            bar = '░' * (self.bar_width - filled) + '▓' * filled
            
        return f"{color}{bar}{Colors.RESET}"

    def print_state(self, title: str = "STAN EMOCJONALNY"):
        """
        Wyświetla pełny stan 15-wymiarowy w terminalu.
        
        Args:
            title: Tytuł sekcji
        """
        state = self.get_state_vector()
        max_val = max(abs(state.max()), abs(state.min()), 1.0)
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.CYAN}{title:^60}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
        
        # Plutchik
        print(f"\n{Colors.YELLOW}OSIE BIOLOGICZNE (Plutchik){Colors.RESET}")
        print("-" * 60)
        
        for i, axis in enumerate(AXES[:8]):
            val = state[i]
            color = self.AXIS_COLORS_ANSI.get(axis, Colors.WHITE)
            symbol = self.AXIS_SYMBOLS.get(axis, '•')
            eph = "⚡" if axis in EPHEMERAL_AXES else "  "
            bar = self.visualize_bar(val, max_val, color)
            
            print(f"{symbol} {color}{axis:12s}{Colors.RESET} {eph} [{bar}] {val:+7.2f}")
        
        # Metafizyczne
        print(f"\n{Colors.YELLOW}OSIE METAFIZYCZNE{Colors.RESET}")
        print("-" * 60)
        
        for i, axis in enumerate(AXES[8:], start=8):
            val = state[i]
            color = self.AXIS_COLORS_ANSI.get(axis, Colors.WHITE)
            symbol = self.AXIS_SYMBOLS.get(axis, '•')
            eph = "⚡" if axis in EPHEMERAL_AXES else "  "
            bar = self.visualize_bar(val, max_val, color)
            
            print(f"{symbol} {color}{axis:12s}{Colors.RESET} {eph} [{bar}] {val:+7.2f}")
        
        # Podsumowanie
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
        
        # Dominująca emocja
        dominant_idx = np.argmax(np.abs(state))
        dominant_axis = AXES[dominant_idx]
        dominant_val = state[dominant_idx]
        dominant_color = self.AXIS_COLORS_ANSI.get(dominant_axis, Colors.WHITE)
        
        print(f"Dominanta: {dominant_color}{dominant_axis.upper()}{Colors.RESET} = {dominant_val:+.2f}")
        
        # Norma wektora (energia całkowita)
        energy = np.linalg.norm(state)
        print(f"Energia:   {energy:.2f}")
        
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

    def print_compact(self):
        """Kompaktowy widok stanu (jedna linia)."""
        state = self.get_state_vector()
        
        parts = []
        for i, axis in enumerate(AXES):
            val = state[i]
            if abs(val) > 0.1:  # Tylko niezerowe
                symbol = self.AXIS_SYMBOLS.get(axis, '•')
                color = self.AXIS_COLORS_ANSI.get(axis, Colors.WHITE)
                parts.append(f"{color}{symbol}{val:+.1f}{Colors.RESET}")
        
        print(" ".join(parts) if parts else "[stan neutralny]")

    def get_dominant_emotion(self) -> Tuple[str, float]:
        """
        Zwraca nazwę i wartość dominującej osi.
        
        Returns:
            Tuple[str, float]: (nazwa_osi, wartość)
        """
        state = self.get_state_vector()
        dominant_idx = np.argmax(np.abs(state))
        return AXES[dominant_idx], state[dominant_idx]

    def get_plutchik_summary(self) -> dict:
        """
        Zwraca podsumowanie tylko osi Plutchika (0-7).
        
        Returns:
            dict: {nazwa_osi: wartość}
        """
        state = self.get_state_vector()
        return {AXES[i]: state[i] for i in range(8)}

    def get_metaphysical_summary(self) -> dict:
        """
        Zwraca podsumowanie tylko osi metafizycznych (8-14).
        
        Returns:
            dict: {nazwa_osi: wartość}
        """
        state = self.get_state_vector()
        return {AXES[i]: state[i] for i in range(8, 15)}

    def get_rgb_color_for_state(self) -> Tuple[int, int, int]:
        """
        Oblicza kolor RGB reprezentujący aktualny stan.
        Miksuje kolory osi proporcjonalnie do ich wartości.
        
        Returns:
            Tuple[int, int, int]: (R, G, B)
        """
        state = self.get_state_vector()
        
        # Normalizuj do wartości dodatnich
        weights = np.abs(state)
        total_weight = weights.sum()
        
        if total_weight < 0.01:
            return (128, 128, 128)  # Szary dla stanu neutralnego
        
        weights = weights / total_weight
        
        r, g, b = 0.0, 0.0, 0.0
        for i, axis in enumerate(AXES):
            color = self.AXIS_COLORS_RGB.get(axis, (128, 128, 128))
            r += color[0] * weights[i]
            g += color[1] * weights[i]
            b += color[2] * weights[i]
        
        return (int(r), int(g), int(b))

    def get_data_for_gui(self) -> dict:
        """
        Zwraca dane do wizualizacji w GUI.
        
        Returns:
            dict z pełnymi danymi stanu
        """
        state = self.get_state_vector()
        dominant_axis, dominant_val = self.get_dominant_emotion()
        
        return {
            'axes': AXES,
            'values': state.tolist(),
            'dimension': DIMENSION,
            'dominant': {
                'axis': dominant_axis,
                'value': dominant_val,
                'color_rgb': self.AXIS_COLORS_RGB.get(dominant_axis)
            },
            'energy': float(np.linalg.norm(state)),
            'plutchik': self.get_plutchik_summary(),
            'metaphysical': self.get_metaphysical_summary(),
            'mixed_color': self.get_rgb_color_for_state(),
            'ephemeral': list(EPHEMERAL_AXES),
            'persistent': list(PERSISTENT_AXES)
        }

    def print_axis_legend(self):
        """Wyświetla legendę osi z kolorami i symbolami."""
        print(f"\n{Colors.CYAN}{'='*50}")
        print("LEGENDA OSI (Model 15D)")
        print(f"{'='*50}{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}PLUTCHIK (0-7):{Colors.RESET}")
        for i, axis in enumerate(AXES[:8]):
            color = self.AXIS_COLORS_ANSI.get(axis, Colors.WHITE)
            symbol = self.AXIS_SYMBOLS.get(axis, '•')
            eph = "⚡ efem." if axis in EPHEMERAL_AXES else ""
            print(f"  [{i}] {symbol} {color}{axis:12s}{Colors.RESET} {eph}")
        
        print(f"\n{Colors.YELLOW}METAFIZYCZNE (8-14):{Colors.RESET}")
        for i, axis in enumerate(AXES[8:], start=8):
            color = self.AXIS_COLORS_ANSI.get(axis, Colors.WHITE)
            symbol = self.AXIS_SYMBOLS.get(axis, '•')
            eph = "⚡ efem." if axis in EPHEMERAL_AXES else ""
            print(f"  [{i}] {symbol} {color}{axis:12s}{Colors.RESET} {eph}")
        
        print(f"\n{Colors.CYAN}{'='*50}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: Prosty radar chart (ASCII)
# ═══════════════════════════════════════════════════════════════════════════════

class ASCIIRadarChart:
    """Prosty wykres radarowy w ASCII dla 8 osi Plutchika."""
    
    def __init__(self, size: int = 10):
        self.size = size
    
    def draw(self, values: List[float], labels: List[str] = None) -> str:
        """
        Rysuje wykres radarowy dla 8 wartości.
        
        Args:
            values: Lista 8 wartości (osie Plutchika)
            labels: Opcjonalne etykiety
            
        Returns:
            str: ASCII art
        """
        if len(values) != 8:
            return "[Radar wymaga dokładnie 8 wartości]"
        
        # Normalizuj wartości do 0-1
        max_val = max(abs(v) for v in values) or 1.0
        normalized = [abs(v) / max_val for v in values]
        
        labels = labels or AXES[:8]
        
        # Uproszczony widok
        lines = []
        lines.append("        {:^12s}".format(labels[0][:6]))
        lines.append("    {:^6s}     {:^6s}".format(labels[7][:4], labels[1][:4]))
        lines.append("")
        lines.append("  {:^4s}    ●    {:^4s}".format(labels[6][:4], labels[2][:4]))
        lines.append("")
        lines.append("    {:^6s}     {:^6s}".format(labels[5][:4], labels[3][:4]))
        lines.append("        {:^12s}".format(labels[4][:6]))
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TEST: Visualizer v3.0.0 (15 osi)")
    print("=" * 60)
    
    viz = EmotionVisualizer()
    
    # Test 1: Legenda
    viz.print_axis_legend()
    
    # Test 2: Stan (zerowy bez core)
    viz.print_state("STAN TESTOWY")
    
    # Test 3: Kolor RGB
    rgb = viz.get_rgb_color_for_state()
    print(f"Kolor RGB: {rgb}")
    
    # Test 4: Dane dla GUI
    data = viz.get_data_for_gui()
    print(f"\nDane GUI:")
    print(f"  Wymiar: {data['dimension']}")
    print(f"  Dominanta: {data['dominant']}")
    print(f"  Energia: {data['energy']:.2f}")
    
    print("\n✅ Testy visualizer zakończone!")