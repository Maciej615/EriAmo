# -*- coding: utf-8 -*-
"""
fractal.py v8.0.0-Hybrid-Fix
Generator fraktali ASCII kompatybilny z architekturą wektorową (15 osi).
"""
import random
import math
import numpy as np
import time
try:
    from config import Colors
except ImportError:
    class Colors:
        CYAN = '\033[96m'; RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[94m'; MAGENTA = '\033[95m'; WHITE = '\033[97m'; RESET = '\033[0m'

class FractalGenerator:
    def __init__(self, aii_instance):
        self.aii = aii_instance
        self.width = 60
        self.height = 25
        
        # Mapa kolorów dla osi (Biologia + Metafizyka)
        self.COLOR_MAP = {
            'radość': Colors.YELLOW,
            'smutek': Colors.BLUE,
            'strach': Colors.MAGENTA,
            'gniew': Colors.RED,
            'miłość': Colors.MAGENTA, # lub Pink
            'wstręt': Colors.GREEN,
            'zaskoczenie': Colors.CYAN,
            'akceptacja': Colors.WHITE,
            'logika': Colors.CYAN,
            'wiedza': Colors.BLUE,
            'czas': Colors.WHITE,
            'kreacja': Colors.YELLOW,
            'byt': Colors.GREEN,
            'przestrzeń': Colors.MAGENTA,
            'chaos': Colors.RED
        }

    def _get_dominant_emotion(self):
        """
        Bezpiecznie pobiera dominującą emocję/oś z rdzenia AII v8.0.
        Naprawia błąd: AttributeError: 'AII' object has no attribute 'emocja'
        """
        # 1. Próba pobrania wektora (Nowa Architektura)
        if hasattr(self.aii, 'context_vector') and hasattr(self.aii, 'AXES_ORDER'):
            vec = self.aii.context_vector
            axes = self.aii.AXES_ORDER
            
            if len(vec) > 0 and np.max(vec) > 0:
                idx = np.argmax(vec)
                if idx < len(axes):
                    return axes[idx]
        
        # 2. Fallback dla starej architektury (gdyby ktoś używał v6)
        if hasattr(self.aii, 'emocja'):
            return self.aii.emocja
            
        return "neutralna"

    def generate(self, pattern_type=None):
        """Generuje klatkę fraktala w oparciu o stan systemu."""
        emotion = self._get_dominant_emotion()
        color = self.COLOR_MAP.get(emotion, Colors.WHITE)
        
        # Wybór algorytmu w zależności od osi
        if pattern_type:
            algo = pattern_type
        elif emotion in ['logika', 'wiedza', 'akceptacja']:
            algo = 'mandelbrot' # Porządek
        elif emotion in ['chaos', 'gniew', 'strach', 'zaskoczenie']:
            algo = 'julia'      # Chaos
        elif emotion in ['kreacja', 'miłość', 'radość']:
            algo = 'sierpinski' # Symetria
        else:
            algo = 'noise'

        buffer = []
        chars = " .:-=+*#%@"
        
        # Parametry dynamiczne
        t = time.time()
        zoom = 1.0 + 0.5 * math.sin(t * 0.5)
        
        if algo == 'mandelbrot':
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    # Mapowanie współrzędnych
                    cx = (x - self.width/2) / (self.width/3) / zoom - 0.5
                    cy = (y - self.height/2) / (self.height/2) / zoom
                    c = complex(cx, cy)
                    z = 0
                    iter_val = 0
                    max_iter = 20
                    while abs(z) < 2 and iter_val < max_iter:
                        z = z*z + c
                        iter_val += 1
                    row += chars[int(iter_val / max_iter * (len(chars)-1))]
                buffer.append(color + row + Colors.RESET)
                
        elif algo == 'julia':
            c = complex(-0.8, 0.156)
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    zx = 1.5 * (x - self.width / 2) / (0.5 * self.width)
                    zy = (y - self.height / 2) / (0.5 * self.height)
                    z = complex(zx, zy)
                    iter_val = 0
                    max_iter = 20
                    while abs(z) < 2 and iter_val < max_iter:
                        z = z*z + c
                        iter_val += 1
                    row += chars[int(iter_val / max_iter * (len(chars)-1))]
                buffer.append(color + row + Colors.RESET)
        
        else: # Sierpinski / Simple
             for y in range(self.height):
                row = ""
                for x in range(self.width):
                    if (x & y): row += " "
                    else: row += chars[4]
                buffer.append(color + row + Colors.RESET)

        return "\n".join(buffer)

    def display(self, pattern_type=None):
        """Metoda wywoływana przez Agency."""
        art = self.generate(pattern_type)
        print(f"\n{Colors.CYAN}[FRACTAL PROJECTION]{Colors.RESET}")
        print(art)
        print(f"{Colors.FAINT}(Dominanta: {self._get_dominant_emotion()}){Colors.RESET}\n")

if __name__ == "__main__":
    # Test
    class MockAII:
        context_vector = np.array([0,0,0,0,0,0,0,0, 1.0, 0,0,0,0,0,0]) # Logika
        AXES_ORDER = ['r','s','st','g','m','w','z','a', 'logika','w','c','k','b','p','ch']
    
    gen = FractalGenerator(MockAII())
    gen.display()