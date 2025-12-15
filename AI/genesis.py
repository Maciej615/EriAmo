# genesis.py - Skrypt Inicjalizujący Świadomość
from aii import AII
from config import Colors

print("--- GENESIS: INICJALIZACJA LEKSYKONU ---")
ai = AII()

# 1. Wymuszone nauczanie słów kluczowych (Słownik)
print(f"{Colors.CYAN}Wgrywanie pojęć podstawowych...{Colors.RESET}")

# KREACJA (Muzyka, Sztuka)
words_kreacja = ["muzyka", "instrument", "trąbka", "dźwięk", "grać", "tworzyć", "sztuka", "piękno"]
for w in words_kreacja:
    ai.lexicon.learn_from_correction(w, "kreacja", 1.0)

# WALKA (Konflikt, Siła)
words_walka = ["hołd", "pruski", "wojna", "bitwa", "miecz", "konflikt", "siła", "armia"]
for w in words_walka:
    ai.lexicon.learn_from_correction(w, "walka", 1.0)

# LOGIKA (Przyczyna, Skutek)
words_logika = ["przyczyna", "skutek", "dlaczego", "ponieważ", "wynika", "sens", "powód"]
for w in words_logika:
    ai.lexicon.learn_from_correction(w, "logika", 1.0)

# Zapisz słownik
ai.lexicon.save()
print(f"{Colors.GREEN}Leksykon zapisany. Ilość słów: {ai.lexicon.get_stats()['total']}{Colors.RESET}")

# 2. Wgrywanie pierwszej wiedzy (z poprawnymi wektorami)
print(f"{Colors.CYAN}Wgrywanie aksjomatów...{Colors.RESET}")

# Definicja 1
ai.teach("[Definicja]", "Instrument to przedmiot służący do tworzenia muzyki.", is_axiom=True)

# Definicja 2
ai.teach("[Przykład]", "Trąbka jest głośnym instrumentem dętym.")

# Definicja 3
ai.teach("[Historia]", "Przyczyną Hołdu Pruskiego była sekularyzacja zakonu.")

# Zapisz duszę
ai.save_knowledge()
print(f"{Colors.MAGENTA}GENESIS ZAKOŃCZONE. Uruchom main.py.{Colors.RESET}")