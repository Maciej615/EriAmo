# -*- coding: utf-8 -*-
# fractal.py - Generator Fraktali ASCII dla EriAmo
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""
Moduł twórczy: Generowanie prostych fraktali ASCII
na podstawie stanu emocjonalnego.

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
"""

import random
from config import Colors

class FractalGenerator:
    """
    Generator prostych fraktali ASCII inspirowanych emocją.
    Używa różnych symboli i wzorów zależnie od stanu.
    """
    
    # Symbole dla różnych emocji
    EMOTION_SYMBOLS = {
        'radość': ['*', '+', 'o', 'O', '@'],
        'smutek': ['.', '·', ':', 'o', 'O'],
        'strach': ['#', '%', '&', 'X', '@'],
        'gniew': ['!', '|', '/', '\\', 'X'],
        'miłość': ['<3', '*', 'o', 'O', '@'],
        'neutralna': ['+', '-', '|', '/', '\\']
    }
    
    def __init__(self, aii_instance):
        """
        Args:
            aii_instance: Referencja do głównego systemu AII
        """
        self.aii = aii_instance
    
    def generate_sierpinski_triangle(self, levels=4):
        """
        Generuje trójkąt Sierpińskiego (uproszczony).
        
        Args:
            levels: Głębokość rekurencji (max 5 dla ASCII)
        
        Returns:
            list: Linie ASCII reprezentujące fraktal
        """
        emotion = self.aii.emocja
        symbols = self.EMOTION_SYMBOLS.get(emotion, self.EMOTION_SYMBOLS['neutralna'])
        symbol = random.choice(symbols)
        
        # Prosta implementacja trójkąta
        lines = []
        size = 2 ** levels
        
        for row in range(size):
            spaces = ' ' * (size - row - 1)
            chars = symbol * (2 * row + 1)
            lines.append(spaces + chars)
        
        return lines
    
    def generate_mandala(self, size=9):
        """
        Generuje prosty mandala-like pattern.
        
        Args:
            size: Rozmiar (nieparzysty)
        
        Returns:
            list: Linie ASCII
        """
        emotion = self.aii.emocja
        symbols = self.EMOTION_SYMBOLS.get(emotion, self.EMOTION_SYMBOLS['neutralna'])
        
        # Musi być nieparzysty
        if size % 2 == 0:
            size += 1
        
        center = size // 2
        lines = []
        
        for y in range(size):
            line = ''
            for x in range(size):
                # Odległość od centrum
                dist = abs(x - center) + abs(y - center)
                
                # Wybór symbolu na podstawie odległości
                if dist < len(symbols):
                    line += symbols[dist] + ' '
                else:
                    line += symbols[-1] + ' '
            
            lines.append(line)
        
        return lines
    
    def generate_spiral(self, size=15):
        """
        Generuje spiralny pattern.
        
        Args:
            size: Rozmiar siatki
        
        Returns:
            list: Linie ASCII
        """
        emotion = self.aii.emocja
        symbols = self.EMOTION_SYMBOLS.get(emotion, self.EMOTION_SYMBOLS['neutralna'])
        
        # Siatka
        grid = [[' ' for _ in range(size)] for _ in range(size)]
        
        # Spirala od środka
        x, y = size // 2, size // 2
        dx, dy = 0, -1
        
        for i in range(size * size):
            if (-size // 2 <= x < size // 2 + 1 and 
                -size // 2 <= y < size // 2 + 1):
                grid[y + size // 2][x + size // 2] = random.choice(symbols)
            
            if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
                dx, dy = -dy, dx
            
            x, y = x + dx, y + dy
        
        return [''.join(row) for row in grid]
    
    def _reinforce_pattern_words(self, words, emotion):
        """
        Wzmacnia słowa wzorów w lexiconie.
        Geometria → Emocja → Wiedza!
        """
        reinforced_count = 0
        for word in words:
            normalized = self.aii.lexicon._normalize(word)
            if self.aii.lexicon.learn_from_correction(normalized, emotion, strength=0.12):
                reinforced_count += 1
        
        if reinforced_count > 0:
            print(f"{Colors.FAINT}[Fractal→Lexicon] Wzmocniłem {reinforced_count} wzorów w '{emotion}'{Colors.RESET}")
    
    def display(self, pattern_type='mandala'):
        """
        Wyświetla wybrany fraktal.
        
        Args:
            pattern_type: 'mandala', 'triangle', 'spiral'
        """
        emotion = self.aii.emocja
        
        # Kolor
        color_map = {
            'radość': Colors.YELLOW,
            'smutek': Colors.BLUE,
            'strach': Colors.MAGENTA,
            'gniew': Colors.RED,
            'miłość': Colors.PINK,
            'neutralna': Colors.CYAN
        }
        color = color_map.get(emotion, Colors.CYAN)
        
        # Wybierz pattern
        if pattern_type == 'triangle':
            lines = self.generate_sierpinski_triangle(levels=4)
            title = "Trójkąt Sierpińskiego"
            pattern_words = ["ostrze", "krawędź", "geometria", "trójkąt", "struktura"]
        elif pattern_type == 'spiral':
            lines = self.generate_spiral(size=13)
            title = "Spirala Emocjonalna"
            pattern_words = ["spirala", "wir", "głębia", "zagłębienie", "obrót"]
        else:  # mandala
            lines = self.generate_mandala(size=11)
            title = "Mandala"
            pattern_words = ["mandala", "harmonia", "symetria", "równowaga", "centrum"]
        
        # WZMACNIANIE: Wzory geometryczne uczą lexicon!
        self._reinforce_pattern_words(pattern_words, emotion)
        
        # Wyświetl
        print(f"\n{color}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{color}║   [FRAKTAL] {title:26s}  ║{Colors.RESET}")
        print(f"{color}║   Stan: {emotion:32s}  ║{Colors.RESET}")
        print(f"{color}╠════════════════════════════════════════════╣{Colors.RESET}")
        
        for line in lines:
            # Centruj linię
            padding = (44 - len(line)) // 2
            print(f"{color}║{' ' * padding}{line}{' ' * (44 - padding - len(line))}║{Colors.RESET}")
        
        print(f"{color}╚════════════════════════════════════════════╝{Colors.RESET}\n")
