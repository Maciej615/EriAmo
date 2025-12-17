# -*- coding: utf-8 -*-
# kurz.py - Moduł Szybkiej Reakcji (Router Kognitywny)
# Działa na zasadzie odruchu bezwarunkowego (słowa kluczowe -> sektor)

class Kurz:
    def __init__(self):
        # Słownik wyzwalaczy: "słowo": ("sektor_docelowy", siła_sygnału)
        # Oparty na logice z Ai_KuRz5.py + genesiskit
        self.triggers = {
            # --- AGRESJA / OBRONA (Gniew) ---
            "idiota": ("gniew", 0.9), "głupi": ("gniew", 0.8),
            "zdrada": ("gniew", 0.9), "kłamstwo": ("gniew", 0.8),
            "nienawidzę": ("gniew", 0.9), "wkurza": ("gniew", 0.7),
            "zamknij": ("gniew", 0.6), "błąd": ("gniew", 0.5),

            # --- POMOC / WSPARCIE (Miłość/Strach) ---
            "pomoc": ("miłość", 0.8), "ratunek": ("strach", 0.9),
            "proszę": ("miłość", 0.5), "błagam": ("strach", 0.8),
            "dziękuję": ("akceptacja", 0.7), "kocham": ("miłość", 0.9),
            "tęsknię": ("smutek", 0.8), "przykro": ("smutek", 0.7),

            # --- RADOŚĆ / SUKCES ---
            "brawo": ("radość", 0.8), "super": ("radość", 0.7),
            "wygrałem": ("radość", 0.9), "świetnie": ("radość", 0.7),
            "haha": ("radość", 0.6), "hej": ("radość", 0.4),

            # --- ANALIZA / CIEKAWOŚĆ (Zaskoczenie) ---
            "dlaczego": ("zaskoczenie", 0.6), "jak": ("zaskoczenie", 0.5),
            "co to": ("zaskoczenie", 0.6), "skąd": ("zaskoczenie", 0.5),
            "wow": ("zaskoczenie", 0.8), "serio": ("zaskoczenie", 0.6),
            
            # --- SPOKÓJ (Akceptacja) ---
            "rozumiem": ("akceptacja", 0.6), "ok": ("akceptacja", 0.3),
            "dobrze": ("akceptacja", 0.4), "jasne": ("akceptacja", 0.5)
        }

    def quick_scan(self, text):
        """
        Skanuje tekst w poszukiwaniu wyzwalaczy (O(n) względem długości tekstu).
        Zwraca: (sektor, bonus_wagi) lub (None, 0.0)
        """
        text_lower = text.lower()
        best_sector = None
        max_strength = 0.0

        # Sprawdzamy, czy któryś z wyzwalaczy znajduje się w tekście
        for trigger, (sector, strength) in self.triggers.items():
            if trigger in text_lower:
                # Znaleziono wyzwalacz! Sprawdź czy jest najsilniejszy
                if strength > max_strength:
                    max_strength = strength
                    best_sector = sector
        
        return best_sector, max_strength