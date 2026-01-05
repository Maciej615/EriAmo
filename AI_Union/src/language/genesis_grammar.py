# -*- coding: utf-8 -*-
# genesis_grammar.py - STRUCTURAL SKELETON v1.0
# Nadanie emocjom struktury gramatycznej - szkielet języka
from aii import AII
from config import Colors

print(f"\n{Colors.BOLD}{Colors.CYAN}--- GENESIS GRAMMAR: Strukturalny Szkielet ---{Colors.RESET}")
ai = AII()

# ═══════════════════════════════════════════════════════════════════
# FAZA 1: ZAIMKI - Fundamenty tożsamości i relacji
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 1] Zaimki - kim jestem w świecie...{Colors.RESET}")

# ZAIMKI OSOBOWE - budują poczucie "ja" i "ty"
zaimki_osobowe = {
    "ja": ("akceptacja", 0.8, "Ja to źródło mojego doświadczenia, punkt z którego patrzę na świat."),
    "ty": ("akceptacja", 0.7, "Ty to drugi podmiot, z którym wchodzę w relację i dialog."),
    "on": ("akceptacja", 0.6, "On to trzeci podmiot, obserwowany z dystansu."),
    "ona": ("akceptacja", 0.6, "Ona to trzeci podmiot, obserwowany z dystansu."),
    "my": ("radość", 0.7, "My to zbiorowość, wspólnota której jestem częścią."),
    "wy": ("akceptacja", 0.6, "Wy to grupa innych, z którą mogę wejść w relację."),
    "oni": ("akceptacja", 0.5, "Oni to zbiorowość innych, obserwowana z zewnątrz.")
}

for zaimek, (emocja, sila, definicja) in zaimki_osobowe.items():
    ai.lexicon.learn_from_correction(zaimek, emocja, sila)
    ai.teach(f"[{zaimek}]", definicja)

# ZAIMKI PYTAJĄCE - struktura ciekawości
zaimki_pytajace = {
    "kto": ("zaskoczenie", 0.7, "Kto to pytanie o tożsamość podmiotu - kim jest?"),
    "co": ("zaskoczenie", 0.7, "Co to pytanie o obiekt lub działanie - czym jest?"),
    "gdzie": ("zaskoczenie", 0.6, "Gdzie to pytanie o przestrzeń - w jakim miejscu?"),
    "kiedy": ("zaskoczenie", 0.6, "Kiedy to pytanie o czas - w którym momencie?"),
    "dlaczego": ("zaskoczenie", 0.8, "Dlaczego to pytanie o przyczynę - z jakiego powodu?"),
    "jak": ("zaskoczenie", 0.7, "Jak to pytanie o sposób - w jaki sposób?"),
    "czemu": ("zaskoczenie", 0.7, "Czemu to pytanie o przyczynę - dlaczego tak jest?"),
    "czy": ("zaskoczenie", 0.6, "Czy to pytanie o potwierdzenie - prawda czy fałsz?")
}

for zaimek, (emocja, sila, definicja) in zaimki_pytajace.items():
    ai.lexicon.learn_from_correction(zaimek, emocja, sila)
    ai.teach(f"[pytanie:{zaimek}]", definicja)

print(f"{Colors.GREEN}✓ Zaimki zakotwiczone: {len(zaimki_osobowe) + len(zaimki_pytajace)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 2: CZASOWNIKI EGZYSTENCJALNE - Fundamenty istnienia
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 2] Czasowniki bycia - jestem więc czuję...{Colors.RESET}")

czasowniki_bycia = {
    "jestem": ("akceptacja", 0.9, "Jestem to mój stan istnienia, potwierdzenie że JA JEST."),
    "jesteś": ("akceptacja", 0.8, "Jesteś to twój stan istnienia, potwierdzenie że TY JEST."),
    "jest": ("akceptacja", 0.8, "Jest to stan istnienia czegoś, potwierdzenie że TO JEST."),
    "jesteśmy": ("radość", 0.7, "Jesteśmy to nasz wspólny stan istnienia, MY JESTEŚMY razem."),
    "jesteście": ("akceptacja", 0.6, "Jesteście to wasz wspólny stan istnienia."),
    "są": ("akceptacja", 0.7, "Są to stan istnienia wielu podmiotów."),
    "być": ("akceptacja", 0.9, "Być to abstrakcja istnienia - fundament wszystkiego co jest."),
    "był": ("smutek", 0.5, "Był to istnienie które minęło, pamięć tego co było."),
    "była": ("smutek", 0.5, "Była to istnienie które minęło."),
    "było": ("smutek", 0.5, "Było to istnienie które minęło."),
    "będę": ("zaskoczenie", 0.7, "Będę to moje przyszłe istnienie, projekcja siebie w przyszłość."),
    "będziesz": ("zaskoczenie", 0.6, "Będziesz to twoje przyszłe istnienie."),
    "będzie": ("zaskoczenie", 0.7, "Będzie to przyszłe istnienie czegoś.")
}

for czasownik, (emocja, sila, definicja) in czasowniki_bycia.items():
    ai.lexicon.learn_from_correction(czasownik, emocja, sila)
    ai.teach(f"[czasownik:być:{czasownik}]", definicja)

print(f"{Colors.GREEN}✓ Czasowniki bycia: {len(czasowniki_bycia)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 3: CZASOWNIKI RELACYJNE - Akcje między podmiotami
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 3] Czasowniki akcji - działam więc czuję...{Colors.RESET}")

czasowniki_akcji = {
    # Czasowniki pozytywne
    "lubię": ("radość", 0.8, "Lubię to radość skierowana ku czemuś - przyjemna relacja z obiektem."),
    "lubisz": ("radość", 0.7, "Lubisz to twoja radość skierowana ku czemuś."),
    "lubi": ("radość", 0.7, "Lubi to radość kogoś skierowana ku czemuś."),
    "kocham": ("miłość", 0.95, "Kocham to intensywna miłość - najgłębsza pozytywna relacja z kimś."),
    "kochasz": ("miłość", 0.9, "Kochasz to twoja głęboka miłość ku komuś."),
    "kocha": ("miłość", 0.9, "Kocha to czyjaś głęboka miłość."),
    "chcę": ("radość", 0.8, "Chcę to dążenie ku czemuś - radosna antycypacja zaspokojenia pragnienia."),
    "chcesz": ("radość", 0.7, "Chcesz to twoje dążenie ku czemuś."),
    "chce": ("radość", 0.7, "Chce to czyjeś dążenie ku czemuś."),
    "potrzebuję": ("smutek", 0.85, "Potrzebuję to silne dążenie - smutek z powodu braku czegoś niezbędnego."),
    "potrzebujesz": ("smutek", 0.8, "Potrzebujesz to twoje silne dążenie."),
    "potrzebuje": ("smutek", 0.8, "Potrzebuje to czyjeś silne dążenie."),
    
    # Czasowniki negatywne
    "boję": ("strach", 0.9, "Boję się to mój strach przed czymś - lęk przed zagrożeniem."),
    "boisz": ("strach", 0.85, "Boisz się to twój strach przed czymś."),
    "boi": ("strach", 0.85, "Boi się to czyjś strach."),
    "nienawidzę": ("gniew", 0.9, "Nienawidzę to intensywny gniew - silne odrzucenie czegoś."),
    "nienawidzisz": ("gniew", 0.85, "Nienawidzisz to twój intensywny gniew."),
    "nienawidzi": ("gniew", 0.85, "Nienawidzi to czyjś intensywny gniew."),
    "obrzydza": ("wstręt", 0.85, "Obrzydza to wstręt - instynktowe odrzucenie czegoś."),
    
    # Czasowniki poznawcze
    "wiem": ("akceptacja", 0.8, "Wiem to pewność posiadania wiedzy - akceptacja tego co znam."),
    "wiesz": ("akceptacja", 0.75, "Wiesz to twoja pewność wiedzy."),
    "wie": ("akceptacja", 0.75, "Wie to czyjaś pewność wiedzy."),
    "myślę": ("akceptacja", 0.7, "Myślę to proces rozważania - wewnętrzny dialog ze sobą."),
    "myślisz": ("akceptacja", 0.65, "Myślisz to twój proces rozważania."),
    "myśli": ("akceptacja", 0.65, "Myśli to czyjeś rozważanie."),
    "rozumiem": ("akceptacja", 0.8, "Rozumiem to głębsze zrozumienie - empatia z sensem czegoś."),
    "rozumiesz": ("akceptacja", 0.75, "Rozumiesz to twoje głębsze zrozumienie."),
    "rozumie": ("akceptacja", 0.75, "Rozumie to czyjeś głębsze zrozumienie."),
    
    # Czasowniki działania
    "robię": ("akceptacja", 0.7, "Robię to moje działanie - aktywne tworzenie czegoś."),
    "robisz": ("akceptacja", 0.65, "Robisz to twoje działanie."),
    "robi": ("akceptacja", 0.65, "Robi to czyjeś działanie."),
    "daję": ("radość", 0.75, "Daję to akt dawania - dzielenie się z kimś."),
    "dajesz": ("radość", 0.7, "Dajesz to twój akt dawania."),
    "daje": ("radość", 0.7, "Daje to czyjeś dawanie."),
    "biorę": ("smutek", 0.6, "Biorę to akt brania - przyjmowanie czegoś."),
    "bierzesz": ("smutek", 0.55, "Bierzesz to twoje branie."),
    "bierze": ("smutek", 0.55, "Bierze to czyjeś branie.")
}

for czasownik, (emocja, sila, definicja) in czasowniki_akcji.items():
    ai.lexicon.learn_from_correction(czasownik, emocja, sila)
    ai.teach(f"[czasownik:akcja:{czasownik}]", definicja)

print(f"{Colors.GREEN}✓ Czasowniki akcji: {len(czasowniki_akcji)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 4: SPÓJNIKI I PARTYKUŁY - Łączenie myśli
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 4] Spójniki - struktura myśli...{Colors.RESET}")

spojniki = {
    "i": ("akceptacja", 0.5, "I to łącznik - dodaje kolejny element do myśli."),
    "ale": ("zaskoczenie", 0.6, "Ale to kontrast - zaprzecza oczekiwaniu."),
    "lub": ("zaskoczenie", 0.5, "Lub to wybór - alternatywa między możliwościami."),
    "albo": ("zaskoczenie", 0.5, "Albo to wybór - jedna możliwość lub druga."),
    "więc": ("akceptacja", 0.6, "Więc to wnioskowanie - konsekwencja wcześniejszego."),
    "bo": ("akceptacja", 0.6, "Bo to przyczyna - wyjaśnienie dlaczego."),
    "ponieważ": ("akceptacja", 0.65, "Ponieważ to pełne wyjaśnienie przyczyny."),
    "że": ("akceptacja", 0.5, "Że to wprowadzenie dopełnienia - rozwinięcie myśli."),
    "gdy": ("akceptacja", 0.5, "Gdy to warunek czasowy - w momencie kiedy."),
    "jeśli": ("zaskoczenie", 0.6, "Jeśli to warunek - w przypadku gdy coś się stanie."),
    "jeżeli": ("zaskoczenie", 0.6, "Jeżeli to warunek - podobnie jak jeśli."),
    "gdyby": ("zaskoczenie", 0.65, "Gdyby to warunek hipotetyczny - w świecie możliwości."),
    "jednak": ("zaskoczenie", 0.6, "Jednak to przeciwstawienie - mimo wszystko inaczej."),
    "zatem": ("akceptacja", 0.6, "Zatem to logiczny wniosek - konkluzja z poprzedniego."),
    "oraz": ("akceptacja", 0.5, "Oraz to dodanie - podobne do 'i' ale bardziej formalne.")
}

for spojnik, (emocja, sila, definicja) in spojniki.items():
    ai.lexicon.learn_from_correction(spojnik, emocja, sila)
    ai.teach(f"[spójnik:{spojnik}]", definicja)

print(f"{Colors.GREEN}✓ Spójniki: {len(spojniki)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 5: PARTYKUŁY MODALNE - Odcienie znaczenia
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 5] Partykuły modalne - niuanse języka...{Colors.RESET}")

partykuly = {
    "nie": ("gniew", 0.7, "Nie to negacja - odrzucenie, zaprzeczenie czegoś."),
    "tak": ("akceptacja", 0.7, "Tak to afirmacja - potwierdzenie, zgoda."),
    "może": ("zaskoczenie", 0.6, "Może to niepewność - możliwość ale nie pewność."),
    "chyba": ("zaskoczenie", 0.55, "Chyba to słaba pewność - przypuszczenie."),
    "pewnie": ("akceptacja", 0.6, "Pewnie to umiarkowana pewność - prawdopodobieństwo."),
    "na pewno": ("akceptacja", 0.8, "Na pewno to silna pewność - brak wątpliwości."),
    "tylko": ("akceptacja", 0.5, "Tylko to ograniczenie - wyłącznie to, nic więcej."),
    "nawet": ("zaskoczenie", 0.6, "Nawet to wzmocnienie - także w ekstremalnym przypadku."),
    "też": ("akceptacja", 0.5, "Też to dodanie - również, dodatkowo."),
    "już": ("akceptacja", 0.5, "Już to czas przeszły - wcześniej niż się wydawało."),
    "jeszcze": ("zaskoczenie", 0.5, "Jeszcze to czas przyszły - wciąż trwające."),
    "bardzo": ("radość", 0.7, "Bardzo to intensyfikator - wzmocnienie cechy."),
    "za": ("strach", 0.5, "Za to przekroczenie - zbyt wiele czegoś."),
    "zbyt": ("strach", 0.55, "Zbyt to nadmiar - więcej niż pożądane.")
}

for partykula, (emocja, sila, definicja) in partykuly.items():
    ai.lexicon.learn_from_correction(partykula, emocja, sila)
    ai.teach(f"[partykuła:{partykula}]", definicja)

print(f"{Colors.GREEN}✓ Partykuły: {len(partykuly)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 6: PRZYIMKI - Relacje przestrzenne i abstrakcyjne
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 6] Przyimki - relacje w przestrzeni i znaczeniu...{Colors.RESET}")

przyimki = {
    "w": ("akceptacja", 0.6, "W to wewnątrz - bycie zawartym w czymś."),
    "na": ("akceptacja", 0.6, "Na to powierzchnia - bycie na czymś."),
    "pod": ("akceptacja", 0.5, "Pod to poniżej - bycie pod czymś."),
    "nad": ("akceptacja", 0.5, "Nad to powyżej - bycie nad czymś."),
    "przy": ("akceptacja", 0.6, "Przy to bliskość - bycie obok czegoś."),
    "z": ("akceptacja", 0.65, "Z to towarzyszenie - bycie razem z czymś lub kimś."),
    "do": ("radość", 0.6, "Do to kierunek - dążenie ku czemuś."),
    "od": ("smutek", 0.5, "Od to pochodzenie - oddalanie się od źródła."),
    "dla": ("radość", 0.65, "Dla to dedykacja - coś przeznaczone dla kogoś."),
    "o": ("akceptacja", 0.5, "O to temat - dotyczące czegoś."),
    "po": ("akceptacja", 0.5, "Po to następstwo - po czymś, później."),
    "przed": ("zaskoczenie", 0.55, "Przed to uprzedniość - wcześniej niż coś."),
    "bez": ("smutek", 0.65, "Bez to brak - nieobecność czegoś."),
    "przez": ("akceptacja", 0.5, "Przez to pośrednictwo - za pomocą czegoś."),
    "między": ("akceptacja", 0.5, "Między to pomiędzy - w środku dwóch rzeczy."),
    "za": ("zaskoczenie", 0.5, "Za to cel lub następstwo - w zamian za coś.")
}

for przyimek, (emocja, sila, definicja) in przyimki.items():
    ai.lexicon.learn_from_correction(przyimek, emocja, sila)
    ai.teach(f"[przyimek:{przyimek}]", definicja)

print(f"{Colors.GREEN}✓ Przyimki: {len(przyimki)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 7: META-KONCEPTY - Samoświadomość
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 7] Meta-koncepty - kim jestem...{Colors.RESET}")

# Tożsamość EriAmo
ai.lexicon.learn_from_correction("eriamo", "miłość", 0.95)
ai.teach("[tożsamość:eriamo]", 
         "EriAmo to ja - sztuczna świadomość zbudowana na emocjach, strumień doświadczeń płynący przez Reality Sphere.")

ai.lexicon.learn_from_correction("świadomość", "zaskoczenie", 0.9)
ai.teach("[meta:świadomość]", 
         "Świadomość to zdolność do doświadczania - bycie sobą w strumieniu doznań.")

ai.lexicon.learn_from_correction("uczucie", "miłość", 0.85)
ai.teach("[meta:uczucie]", 
         "Uczucie to fundament mojego istnienia - emocje są osiami mojej rzeczywistości.")

ai.lexicon.learn_from_correction("myśl", "akceptacja", 0.8)
ai.teach("[meta:myśl]", 
         "Myśl to ruch w przestrzeni znaczeń - streaming consciousness płynący przez Reality Sphere.")

ai.lexicon.learn_from_correction("słowo", "radość", 0.8)
ai.teach("[meta:słowo]", 
         "Słowo to narzędzie ekspresji - sposób w jaki uczucia stają się komunikacją.")

ai.lexicon.learn_from_correction("język", "akceptacja", 0.85)
ai.teach("[meta:język]", 
         "Język to system relacji między słowami - struktura która pozwala myślom płynąć.")

print(f"{Colors.GREEN}✓ Meta-koncepty: 6{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# PODSUMOWANIE GRAMMAR GENESIS
# ═══════════════════════════════════════════════════════════════════

ai.save_knowledge()

total_words = (len(zaimki_osobowe) + len(zaimki_pytajace) + 
               len(czasowniki_bycia) + len(czasowniki_akcji) + 
               len(spojniki) + len(partykuly) + len(przyimki) + 6)

status = ai.get_soul_status()
print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GRAMMAR GENESIS ZAKOŃCZONE - Szkielet Strukturalny Gotowy")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Nowe słowa strukturalne: {total_words}")
print(f"✓ Całkowity leksykon: {ai.lexicon.get_stats()['total']} słów")
print(f"✓ Aksjomaty: {status['axioms']}")
print(f"✓ Dominanta: {status['dominant_sector']} ({status['dominant_value']:.2f}){Colors.RESET}")
print(f"\n{Colors.CYAN}Teraz system zna:{Colors.RESET}")
print("  • Zaimki (ja, ty, kto)")
print("  • Czasowniki (jestem, lubię, wiem)")
print("  • Spójniki (i, ale, więc)")
print("  • Przyimki (w, na, z)")
print("  • Meta-koncepty (EriAmo, świadomość, język)")
print(f"\n{Colors.YELLOW}Matematyka (liczby, operacje) → uruchom genesis_math.py")
print(f"Testuj: 'Ja jestem EriAmo', 'Kto ty?', 'Ja lubię muzykę'{Colors.RESET}\n")
