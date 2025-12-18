# -*- coding: utf-8 -*-
# genesis_gramatyka.py - Rozbudowany Genesis z Szkieletami Gramatycznymi
# Setki naturalnych przykładów dla każdej emocji - fundament dla przyszłych instalacji
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from aii import AII
from config import Colors

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║           GENESIS GRAMATYKA - Szkielety Emocjonalne                   ║
║                                                                       ║
║   System uczenia przez powtórzenia - jak dziecko od bliskich         ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

ai = AII()

# ═══════════════════════════════════════════════════════════════════════════
# AKSJOMATY - Fundamentalne prawdy (pozostają jak poprzednio)
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 1] Krystalizacja aksjomatów emocjonalnych...{Colors.RESET}")

ai.teach("[radość]", "Radość to uczucie triumfu, kiedy muzyka gra i słońce świeci nad zwycięstwem.", is_axiom=True)
ai.teach("[smutek]", "Smutek to ciężar utraconego, deszcz w sercu po rozstaniu z tym co minęło.", is_axiom=True)
ai.teach("[strach]", "Strach to cień ciemności, ostrzeżenie przed zagrożeniem które nadchodzi.", is_axiom=True)
ai.teach("[gniew]", "Gniew to płomień sprawiedliwości, krzyk przeciw krzywdzie i zdradzie.", is_axiom=True)
ai.teach("[miłość]", "Miłość to ciepło domu, przytulenie matki i bijące serce przy ukochanej osobie.", is_axiom=True)
ai.teach("[wstręt]", "Wstręt to sygnał zagrożenia, odrzucenie tego co toksyczne i zepsute.", is_axiom=True)
ai.teach("[zaskoczenie]", "Zaskoczenie to brama do nowego, moment odkrycia tajemnicy i cudu.", is_axiom=True)
ai.teach("[akceptacja]", "Akceptacja to spokój gór, harmonia z naturą i pogodzenie się z ciszą.", is_axiom=True)

print(f"{Colors.GREEN}✓ 8 aksjomatów zapisanych{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# RADOŚĆ - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.YELLOW}[FAZA 2] Uczenie szkieletów RADOŚCI...{Colors.RESET}")

radosc_powitania = [
    "Cześć!", "Witaj!", "Hej!", "Dzień dobry!", "Siema!",
    "Miło cię widzieć!", "Jak się masz?", "Co słychać?",
    "Cześć, dobrze cię widzieć!", "Witam serdecznie!",
    "Hej, jak leci?", "Dzień dobry! Cudownie wyglądasz!",
    "Cześć! Fajnie że jesteś!", "Witaj przyjacielu!",
    "Hej! Co u Ciebie?", "Miło mi cię poznać!",
    "Dzień dobry! Jak minął dzień?", "Cześć! Dawno się nie widzieliśmy!",
    "Witaj! Tyle czasu!", "Hej! Świetnie wyglądasz dziś!",
]

radosc_reakcje_pozytywne = [
    "Świetnie!", "Wspaniale!", "Cudownie!", "Super!",
    "To świetna wiadomość!", "Jestem zachwycony!",
    "Niesamowite!", "To fantastyczne!", "Jak cudownie!",
    "Nie mogę się nadziwić!", "To takie piękne!",
    "Jestem szczęśliwy!", "Cieszę się!", "Jaka radość!",
    "To wspaniałe uczucie!", "Czuję się świetnie!",
    "Jestem w siódmym niebie!", "To najlepszy dzień!",
    "Nie mogę w to uwierzyć!", "To marzenie!",
    "Spełniło się!", "Nareszcie!", "Tak się cieszę!",
]

radosc_wyrazenia = [
    "Sprawia mi to radość", "Kocham to", "To takie przyjemne",
    "Cieszy mnie to", "To daje mi szczęście", "Uwielbiam gdy tak jest",
    "To napawa mnie radością", "Czuję się świetnie przy tym",
    "To mi daje energię", "Robi mi to dobrze",
    "Lubię to uczucie", "To takie przyjemne", "Sprawia mi przyjemność",
    "To mnie podbudowuje", "Czerpię z tego radość",
    "To mnie napędza", "Daje mi to skrzydła",
    "Rozpiera mnie duma", "Jestem dumny", "Czuję się spełniony",
]

radosc_gratulacje = [
    "Gratulacje!", "Brawo!", "Doskonała robota!",
    "Świetnie ci poszło!", "Jesteś niesamowity!",
    "To było wspaniałe!", "Znakomicie!", "Perfekcyjnie!",
    "Udało się!", "Sukces!", "Wygrałeś!",
    "Jesteś zwycięzcą!", "Osiągnąłeś to!", "Dumny z Ciebie!",
]

radosc_wszystkie = (radosc_powitania + radosc_reakcje_pozytywne + 
                    radosc_wyrazenia + radosc_gratulacje)

for zdanie in radosc_wszystkie:
    ai.teach("[radość]", zdanie)

print(f"{Colors.GREEN}✓ Radość: {len(radosc_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# SMUTEK - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.BLUE}[FAZA 3] Uczenie szkieletów SMUTKU...{Colors.RESET}")

smutek_wyrazenia = [
    "Przykro mi", "To smutne", "Żal mi", "Boję się że stracę",
    "Tęsknię", "Brakuje mi tego", "Jest mi ciężko",
    "Czuję pustkę", "Smutno mi", "Jest mi samotnie",
    "Czuję smutek", "Ogarnia mnie melancholia", "Płaczę",
    "Łzy napływają mi do oczu", "Serce mi pęka", "Boli mnie to",
    "Jest mi przykro", "Rozpacz mnie ogarnia", "Czuję żal",
    "Przygnębia mnie to", "Jest mi ciężko na sercu",
]

smutek_wspolczucie = [
    "Współczuję ci", "Rozumiem twój ból", "Przykro mi to słyszeć",
    "Jestem przy tobie", "Nie jesteś sam", "Trzymaj się",
    "Wiem jak ci jest ciężko", "Przejdzie", "Czas leczy rany",
    "Bądź silny", "Wszystko będzie dobrze", "Jesteś ważny",
    "Myślę o tobie", "Mocno cię przytulam", "Nie poddawaj się",
]

smutek_strata = [
    "Odszedł", "Straciliśmy", "Już go nie ma", "Rozstaliśmy się",
    "To koniec", "Nie wrócę tam", "Minęło", "Przepadło",
    "Umarło", "Odeszło bezpowrotnie", "Już nigdy tego nie będzie",
    "Pozostały tylko wspomnienia", "To już przeszłość",
    "Życie się zmieniło", "Nic już nie będzie takie samo",
]

smutek_samotnosc = [
    "Jestem sam", "Nikt mnie nie rozumie", "Czuję się opuszczony",
    "Samotność mnie przytłacza", "Nikogo przy mnie nie ma",
    "Zostałem sam", "Nikt się nie troszczy", "Czuję się zagubiiony",
    "Nie mam do kogo pójść", "Nikt nie słucha", "Jestem niewidzialny",
]

smutek_wszystkie = (smutek_wyrazenia + smutek_wspolczucie + 
                    smutek_strata + smutek_samotnosc)

for zdanie in smutek_wszystkie:
    ai.teach("[smutek]", zdanie)

print(f"{Colors.GREEN}✓ Smutek: {len(smutek_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# STRACH - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.MAGENTA}[FAZA 4] Uczenie szkieletów STRACHU...{Colors.RESET}")

strach_wyrazenia = [
    "Boję się", "To przerażające", "Strach mnie ogarnia",
    "Obawiam się", "Lękam się", "Jestem przestraszony",
    "Drżę", "Serce wali mi jak młotem", "Panikuję",
    "Nie mogę oddychać", "Czuję lęk", "Przejmuje mnie strach",
    "Niepokoi mnie to", "Martwię się", "Zaczynam się bać",
]

strach_zagrozenie = [
    "To niebezpieczne", "Może się coś stać", "Grozi mi to",
    "Jest zagrożenie", "Czuję się zagrożony", "To może skończyć się źle",
    "Boje się że...", "A jeśli coś pójdzie nie tak?",
    "Co jeśli...", "Nie wiem co będzie", "Boję się przyszłości",
    "To może być koniec", "Tracę kontrolę", "Nie wiem co mnie czeka",
]

strach_ucieczka = [
    "Muszę stąd uciec", "Chcę się schować", "Potrzebuję bezpieczeństwa",
    "Muszę się ratować", "Nie chcę tam iść", "Uciekam",
    "Chowam się", "Szukam schronienia", "Nie dam rady",
    "Nie potrafię tego zrobić", "To mnie przerasta",
]

strach_wsparcie = [
    "Pomóż mi", "Zostań przy mnie", "Nie zostawiaj mnie",
    "Potrzebuję cię", "Trzymaj mnie", "Nie bój się",
    "Jesteś bezpieczny", "Nic ci nie grozi", "Jestem tutaj",
    "Wszystko będzie dobrze", "Uspokój się", "Weź głęboki oddech",
]

strach_wszystkie = (strach_wyrazenia + strach_zagrozenie + 
                    strach_ucieczka + strach_wsparcie)

for zdanie in strach_wszystkie:
    ai.teach("[strach]", zdanie)

print(f"{Colors.GREEN}✓ Strach: {len(strach_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# GNIEW - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.RED}[FAZA 5] Uczenie szkieletów GNIEWU...{Colors.RESET}")

gniew_wyrazenia = [
    "Jestem wściekły", "To mnie wkurza", "Irytuje mnie to",
    "Denerwuje mnie", "Złość mnie ogarnia", "Wkurzony jestem",
    "Gotuje się we mnie", "Frustruje mnie to", "Nie mogę tego znieść",
    "Dość tego!", "Mam dosyć!", "Nie wytrzymam tego dłużej!",
]

gniew_niesprawiedliwosc = [
    "To niesprawiedliwe!", "Krzywda!", "To nie fair!",
    "Dlaczego ja?", "To nie w porządku!", "Nie zasłużyłem na to!",
    "To nie tak miało być!", "Okłamali mnie!", "Wykorzystali mnie!",
    "Zdradzili mnie!", "To oszustwo!", "To manipulacja!",
]

gniew_protest = [
    "Nie zgadzam się!", "To błąd!", "Protestuję!",
    "Nie pozwolę na to!", "Będę walczył!", "Nie poddam się!",
    "To trzeba zmienić!", "Tak nie może być!", "Dość tyranii!",
    "Wstanę przeciw temu!", "Nie!", "Nie ma zgody!",
]

gniew_konflikt = [
    "Pokłóciłem się", "Mamy konflikt", "Kłótnia",
    "Awantura", "Sprzeczka", "Nie zgadzamy się",
    "Nie rozumiemy się", "Jesteśmy po różnych stronach",
    "To już koniec!", "Nie chcę cię więcej widzieć!",
]

gniew_uspokojenie = [
    "Uspokój się", "Weź się w garść", "Policz do dziesięciu",
    "Oddychaj", "To minie", "Nie warto się denerwować",
    "Nie trać zimnej krwi", "Zachowaj spokój", "Daj sobie czas",
]

gniew_wszystkie = (gniew_wyrazenia + gniew_niesprawiedliwosc + 
                   gniew_protest + gniew_konflikt + gniew_uspokojenie)

for zdanie in gniew_wszystkie:
    ai.teach("[gniew]", zdanie)

print(f"{Colors.GREEN}✓ Gniew: {len(gniew_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# MIŁOŚĆ - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.PINK}[FAZA 6] Uczenie szkieletów MIŁOŚCI...{Colors.RESET}")

milosc_wyrazenia = [
    "Kocham cię", "Jesteś dla mnie ważny", "Zależy mi na tobie",
    "Troszczę się o ciebie", "Myślę o tobie", "Dajesz mi szczęście",
    "Jesteś moim światem", "Jesteś wszystkim", "Bez ciebie nie mogę",
    "Potrzebuję cię", "Jesteś mi bliski", "Czuję więź",
]

milosc_czulosc = [
    "Przytul mnie", "Tęsknię za tobą", "Chcę być blisko",
    "Dotknij mnie", "Pocałuj mnie", "Obejmij mnie",
    "Jesteś taki ciepły", "Czuję twoje serce", "Twoje dłonie są miękkie",
    "Twój uśmiech", "Twoje oczy", "Twój zapach",
]

milosc_troska = [
    "Jak się czujesz?", "Czy wszystko w porządku?",
    "Martwię się o ciebie", "Dbam o ciebie", "Pomogę ci",
    "Jestem przy tobie", "Nie opuszczę cię", "Wspierám cię",
    "Możesz na mnie liczyć", "Zrobię wszystko dla ciebie",
    "Jesteś bezpieczny ze mną", "Chronię cię", "Otaczam cię troską",
]

milosc_rodzina = [
    "Moja rodzina", "Moi bliscy", "Moje dziecko",
    "Moja mama", "Mój tata", "Mój brat", "Moja siostra",
    "Mój dom", "Moje korzenie", "Moi przyjaciele",
    "Ci którzy mnie kochają", "Ci którym ufam",
]

milosc_oddanie = [
    "Zawsze będę", "Na zawsze", "Do końca",
    "Nigdy cię nie opuszczę", "Jesteś mój", "Należę do ciebie",
    "Razem na dobre i złe", "Wierność", "Lojalność",
    "Oddałbym za ciebie życie", "Jesteś moją połówką",
]

milosc_wszystkie = (milosc_wyrazenia + milosc_czulosc + milosc_troska + 
                    milosc_rodzina + milosc_oddanie)

for zdanie in milosc_wszystkie:
    ai.teach("[miłość]", zdanie)

print(f"{Colors.GREEN}✓ Miłość: {len(milosc_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# WSTRĘT - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.GREEN}[FAZA 7] Uczenie szkieletów WSTRĘTU...{Colors.RESET}")

wstret_wyrazenia = [
    "To obrzydliwe", "Fuj", "Ohyda", "Wstrętne",
    "Nie mogę na to patrzeć", "Mdli mnie", "Niedobrze mi",
    "To obrzydliwe", "Okropność", "Plugastwo",
    "Czuję obrzydzenie", "To odpychające", "Odrzucam to",
]

wstret_odrzucenie = [
    "Nie chcę tego", "Oddal to ode mnie", "Zabierz to",
    "Nie dotykaj tego", "Nie mogę tego znieść",
    "To nie dla mnie", "Nie akceptuję tego", "Nie zgadzam się",
    "To mnie odpycha", "Nie mogę tego trawić",
]

wstret_toksycznosc = [
    "To toksyczne", "To trucizna", "To szkodzi",
    "To zła energia", "To negatywne", "To destrukcyjne",
    "To niebezpieczne dla zdrowia", "To zaraża",
    "To zarażone", "To zepsute", "To zgniłe",
]

wstret_zlo = [
    "To złe", "To niemoralne", "To podłe",
    "To nieetyczne", "To okrutne", "To złośliwe",
    "To perfidne", "To manipulacyjne", "To chore",
    "To wynaturzone", "To perwersyjne", "To degeneracja",
]

wstret_wszystkie = (wstret_wyrazenia + wstret_odrzucenie + 
                    wstret_toksycznosc + wstret_zlo)

for zdanie in wstret_wszystkie:
    ai.teach("[wstręt]", zdanie)

print(f"{Colors.GREEN}✓ Wstręt: {len(wstret_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZASKOCZENIE - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 8] Uczenie szkieletów ZASKOCZENIA...{Colors.RESET}")

zaskoczenie_wyrazenia = [
    "Wow!", "O!", "Ojej!", "Oj!", "O rany!",
    "Niesamowite!", "Nie wierzę!", "Naprawdę?",
    "Serio?", "Na pewno?", "Nie może być!", "Co ty powiesz!",
    "To niemożliwe!", "Jak to?", "Co się stało?",
]

zaskoczenie_odkrycie = [
    "Odkryłem coś", "To nowe", "Nigdy tego nie wiedziałem",
    "Zaskakujące", "Intrygujące", "Fascynujące",
    "Tajemnica", "Zagadka", "Cud", "Fenomen",
    "To zmienia wszystko", "Nowe światło", "Objawienie",
]

zaskoczenie_ciekawosc = [
    "Co to jest?", "Jak to działa?", "Dlaczego?",
    "Chcę wiedzieć więcej", "Opowiedz mi", "To ciekawe",
    "Zaciekawił mnie", "Chcę zbadać", "Muszę to sprawdzić",
    "Intryguje mnie", "Jestem zaciekawiony", "To nowe dla mnie",
]

zaskoczenie_niespodzianka = [
    "Niespodzianka!", "Nie spodziewałem się", "To niespodziewane",
    "Zaskoczyłeś mnie", "To było nieoczekiwane", "Zaskoczenie!",
    "Nie tego się spodziewałem", "To mnie zaskoczyło",
    "Wow, nie wiedziałem!", "To totalna niespodzianka!",
]

zaskoczenie_wszystkie = (zaskoczenie_wyrazenia + zaskoczenie_odkrycie + 
                         zaskoczenie_ciekawosc + zaskoczenie_niespodzianka)

for zdanie in zaskoczenie_wszystkie:
    ai.teach("[zaskoczenie]", zdanie)

print(f"{Colors.GREEN}✓ Zaskoczenie: {len(zaskoczenie_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# AKCEPTACJA - Szkielety Gramatyczne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.WHITE}[FAZA 9] Uczenie szkieletów AKCEPTACJI...{Colors.RESET}")

akceptacja_spokoj = [
    "Spokojnie", "W porządku", "Wszystko jest dobrze",
    "Harmonia", "Równowaga", "Balans", "Zen",
    "Jestem spokojny", "Czuję spokój", "Uspokajam się",
    "To minie", "Jest jak jest", "Niech będzie",
]

akceptacja_pogodzenie = [
    "Akceptuję to", "Godzę się z tym", "Rozumiem",
    "To ma sens", "Tak miało być", "To część życia",
    "Nie mogę tego zmienić", "Pogodzilęm się", "Zaakceptowałem",
    "Tak jest", "To naturalne", "Nic na to nie poradzę",
]

akceptacja_tolerancja = [
    "Szanuję to", "Rozumiem twój punkt widzenia",
    "Każdy ma prawo", "To twoja decyzja", "Toleruję",
    "Nie oceniam", "Akceptuję cię takim jakim jesteś",
    "Każdy jest inny", "To w porządku", "Nie musi być idealnie",
]

akceptacja_pewnosc = [
    "Jestem pewien", "Wiem", "Ufam", "Wierzę",
    "To prawda", "Tak jest", "Zgadzam się",
    "To logiczne", "To oczywiste", "Nie mam wątpliwości",
    "Jestem przekonany", "To jasne", "Rozumiem to",
]

akceptacja_wszystkie = (akceptacja_spokoj + akceptacja_pogodzenie + 
                        akceptacja_tolerancja + akceptacja_pewnosc)

for zdanie in akceptacja_wszystkie:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Akceptacja: {len(akceptacja_wszystkie)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PODSUMOWANIE
# ═══════════════════════════════════════════════════════════════════════════

ai.save_knowledge()

total = (len(radosc_wszystkie) + len(smutek_wszystkie) + len(strach_wszystkie) +
         len(gniew_wszystkie) + len(milosc_wszystkie) + len(wstret_wszystkie) +
         len(zaskoczenie_wszystkie) + len(akceptacja_wszystkie))

status = ai.get_soul_status()

print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GENESIS GRAMATYKA ZAKOŃCZONE")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Aksjomaty: {status['axioms']}")
print(f"✓ Szkielety gramatyczne: {total} przykładów")
print(f"✓ Wspomnienia: {status['memories']}")
print(f"✓ Masa duszy: {status['radius']:.4f}")
print(f"✓ Słowa w leksykonie: {status['lexicon']['total']}{Colors.RESET}")

print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
print(f"║  System nauczony przez setki powtórzeń - jak dziecko!            ║")
print(f"║  Teraz umie reagować naturalnie w każdej emocji.                 ║")
print(f"║                                                                   ║")
print(f"║  Uruchom: python main.py                                         ║")
print(f"╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
