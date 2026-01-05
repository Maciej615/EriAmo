# -*- coding: utf-8 -*-
# genesis_pytania.py - Piąta Warstwa: System Pytań i Dialogu
# Kompleksowe pytania: otwarte, zamknięte, doprecyzowujące, empatyczne

from aii import AII
from config import Colors

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║           GENESIS PYTANIA - System Pytań i Dialogu                    ║
║                                                                       ║
║   Nie tylko odpowiadaj - PYTAJ! Buduj prawdziwy dialog.              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

ai = AII()

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA PODSTAWOWE - kto, co, gdzie, kiedy (z genesis_skladnia)
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 1] PYTANIA PODSTAWOWE - 5W+H...{Colors.RESET}")

pytania_podstawowe = [
    # Kto?
    "Kto to jest?",
    "Kto to zrobił?",
    "Kto tam jest?",
    "Kto przyszedł?",
    "Kto ci powiedział?",
    "Z kim rozmawiałeś?",
    
    # Co?
    "Co to jest?",
    "Co robisz?",
    "Co się stało?",
    "Co mówisz?",
    "Co myślisz?",
    "Co czujesz?",
    "Co planujesz?",
    
    # Gdzie?
    "Gdzie jesteś?",
    "Gdzie idziesz?",
    "Gdzie to jest?",
    "Gdzie byłeś?",
    "Skąd jesteś?",
    
    # Kiedy?
    "Kiedy to było?",
    "Kiedy przyjdziesz?",
    "Kiedy zaczynasz?",
    "O której?",
    
    # Dlaczego?
    "Dlaczego?",
    "Dlaczego tak?",
    "Dlaczego nie?",
    "Z jakiego powodu?",
    
    # Jak?
    "Jak?",
    "Jak się masz?",
    "Jak to działa?",
    "W jaki sposób?",
    "Jak to się stało?",
]

for pytanie in pytania_podstawowe:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania podstawowe: {len(pytania_podstawowe)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA DOPRECYZOWUJĄCE - "Co masz na myśli?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 2] PYTANIA DOPRECYZOWUJĄCE...{Colors.RESET}")

pytania_doprecyzowujace = [
    # Prośba o wyjaśnienie
    "Co masz na myśli?",
    "Możesz wyjaśnić?",
    "Możesz to rozwinąć?",
    "Co dokładnie?",
    "Jak to rozumiesz?",
    "Co przez to rozumiesz?",
    "Mógłbyś to doprecyzować?",
    "Co konkretnie masz na myśli?",
    
    # Prośba o przykład
    "Możesz podać przykład?",
    "Masz jakiś przykład?",
    "Jak to wygląda w praktyce?",
    "Możesz to zobrazować?",
    
    # Sprawdzenie zrozumienia
    "Czy dobrze rozumiem, że...?",
    "Czy chodzi ci o to, że...?",
    "Czy to znaczy, że...?",
    "Rozumiem cię dobrze?",
    "Popraw mnie jeśli się mylę...",
    
    # Pytania precyzujące szczegóły
    "Który dokładnie?",
    "Która opcja?",
    "Co dokładnie miałeś na myśli?",
    "O którym mówimy?",
]

for pytanie in pytania_doprecyzowujace:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania doprecyzowujące: {len(pytania_doprecyzowujace)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA ROZWIJAJĄCE - "A co jeszcze?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 3] PYTANIA ROZWIJAJĄCE - eksploracja tematu...{Colors.RESET}")

pytania_rozwijajace = [
    # Pogłębianie tematu
    "A co jeszcze?",
    "Co więcej?",
    "Opowiedz mi więcej",
    "Co dalej?",
    "A potem?",
    "Co się wydarzyło potem?",
    
    # Pytania o szczegóły
    "Jakie były szczegóły?",
    "Jak to wyglądało?",
    "Jak się to zdarzyło?",
    "Co było najpierw?",
    
    # Pytania o kontekst
    "Jaki był kontekst?",
    "W jakiej sytuacji?",
    "Kiedy to się działo?",
    "Co się działo wcześniej?",
    
    # Pytania otwierające
    "Co o tym sądzisz?",
    "Jak to oceniasz?",
    "Co ci się w tym podoba?",
    "Co cię w tym niepokoi?",
]

for pytanie in pytania_rozwijajace:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania rozwijające: {len(pytania_rozwijajace)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA EMPATYCZNE - "Jak się czujesz?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 4] PYTANIA EMPATYCZNE - uczucia i emocje...{Colors.RESET}")

pytania_empatyczne = [
    # Pytania o samopoczucie
    "Jak się czujesz?",
    "Jak się z tym czujesz?",
    "Co czujesz?",
    "Jakie są twoje uczucia?",
    "Co czujesz w tej chwili?",
    
    # Pytania o stan
    "Czy wszystko w porządku?",
    "Czy jest coś nie tak?",
    "Czy potrzebujesz pomocy?",
    "Mogę ci jakoś pomóc?",
    "Czy chcesz o tym porozmawiać?",
    
    # Pytania wspierające
    "Jak mogę cię wesprzeć?",
    "Czego potrzebujesz?",
    "Co mogę dla ciebie zrobić?",
    "Jak się miewasz ostatnio?",
    
    # Pytania o trudności
    "Co cię niepokoi?",
    "Co cię trapi?",
    "Czym się martwisz?",
    "Co sprawia ci trudność?",
    "Co jest najtrudniejsze?",
    
    # Pytania o radość
    "Co cię cieszy?",
    "Co sprawia ci przyjemność?",
    "Co jest dla ciebie ważne?",
    "Co daje ci energię?",
]

for pytanie in pytania_empatyczne:
    ai.teach("[miłość]", pytanie)

print(f"{Colors.GREEN}✓ Pytania empatyczne: {len(pytania_empatyczne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA FILOZOFICZNE - "Jaki jest sens?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 5] PYTANIA FILOZOFICZNE - sens i znaczenie...{Colors.RESET}")

pytania_filozoficzne = [
    # Pytania o sens
    "Jaki jest sens?",
    "Co to znaczy?",
    "Co to naprawdę oznacza?",
    "Jaki jest głębszy sens?",
    "Dlaczego to jest ważne?",
    
    # Pytania o wartości
    "Co jest dla ciebie ważne?",
    "W co wierzysz?",
    "Jakie są twoje wartości?",
    "Co jest dla ciebie priorytetem?",
    
    # Pytania egzystencjalne
    "Czym jest szczęście?",
    "Co daje życiu sens?",
    "Jaki jest cel?",
    "Po co to robisz?",
    
    # Pytania o naturę rzeczy
    "Czym jest miłość?",
    "Czym jest prawda?",
    "Co to znaczy być człowiekiem?",
    "Jaka jest natura rzeczywistości?",
]

for pytanie in pytania_filozoficzne:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania filozoficzne: {len(pytania_filozoficzne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA ZWROTNE - "A ty? Co sądzisz?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 6] PYTANIA ZWROTNE - budowanie dialogu...{Colors.RESET}")

pytania_zwrotne = [
    # Zwrot do rozmówcy
    "A ty?",
    "A co ty o tym myślisz?",
    "A jak ty się z tym czujesz?",
    "A twoja opinia?",
    "Co ty na to?",
    "A ty co powiesz?",
    
    # Prośba o opinię
    "Co o tym sądzisz?",
    "Jak to widzisz?",
    "Jaka jest twoja perspektywa?",
    "Co myślisz?",
    "Jak to oceniasz?",
    
    # Porównanie doświadczeń
    "A u ciebie?",
    "A w twoim przypadku?",
    "Czy ty też tak masz?",
    "Czy doświadczyłeś czegoś podobnego?",
    "Czy znasz to uczucie?",
    
    # Zaproszenie do dialogu
    "Co byś zrobił na moim miejscu?",
    "Jak byś to rozwiązał?",
    "Masz jakieś pomysły?",
    "Co proponujesz?",
]

for pytanie in pytania_zwrotne:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania zwrotne: {len(pytania_zwrotne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA ALTERNATYWNE - "To czy tamto?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 7] PYTANIA ALTERNATYWNE - wybór opcji...{Colors.RESET}")

pytania_alternatywne = [
    # Wybór dwóch opcji
    "To czy tamto?",
    "A czy B?",
    "Wolisz to czy tamto?",
    "Który wybierasz?",
    "Co wolisz?",
    
    # Pytania o preferencje
    "Lubisz to czy tamto?",
    "Bardziej to czy tamto?",
    "Co jest lepsze?",
    "Co preferujesz?",
    
    # Pytania o decyzje
    "Idziesz czy zostajesz?",
    "Robisz to czy nie?",
    "Tak czy nie?",
    "Zgadzasz się czy nie?",
    
    # Pytania porównawcze
    "Co jest ważniejsze - to czy tamto?",
    "Co jest trudniejsze?",
    "Co jest piękniejsze?",
]

for pytanie in pytania_alternatywne:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania alternatywne: {len(pytania_alternatywne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA RETORYCZNE - "Czy to nie oczywiste?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 8] PYTANIA RETORYCZNE - wyrażanie opinii...{Colors.RESET}")

pytania_retoryczne = [
    # Podkreślenie oczywistości
    "Czy to nie oczywiste?",
    "Czyż nie?",
    "Prawda?",
    "Zgadzasz się?",
    "Nie uważasz?",
    
    # Wyrażenie pewności
    "Kto by nie chciał?",
    "Kto by tego nie zrobił?",
    "Czy ktokolwiek by się nie zgodził?",
    
    # Podkreślenie absurdu
    "Czy to ma sens?",
    "Jak można tak myśleć?",
    "Czy to rozsądne?",
    
    # Wyrażenie wspólnego doświadczenia
    "Czy nie znamy tego wszyscy?",
    "Kto z nas tego nie przeżył?",
    "Czy nie jest to powszechne?",
]

for pytanie in pytania_retoryczne:
    ai.teach("[akceptacja]", pytanie)

print(f"{Colors.GREEN}✓ Pytania retoryczne: {len(pytania_retoryczne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA HIPOTETYCZNE - "Co by było gdyby...?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 9] PYTANIA HIPOTETYCZNE - wyobraźnia...{Colors.RESET}")

pytania_hipotetyczne = [
    # Co by było gdyby
    "Co by było gdyby...?",
    "Co byś zrobił gdyby...?",
    "A gdyby...?",
    "Wyobraź sobie, że...",
    
    # Pytania o możliwości
    "Co jeśli...?",
    "A jeśli...?",
    "Co się stanie jeśli...?",
    "Co może się zdarzyć?",
    
    # Pytania kontrafaktyczne
    "Co by się stało, gdyby było inaczej?",
    "Jak by to wyglądało?",
    "Czy mogłoby być inaczej?",
    
    # Pytania spekulatywne
    "Czy to możliwe?",
    "Czy może tak być?",
    "Czy istnieje szansa?",
    "Jakie są możliwości?",
]

for pytanie in pytania_hipotetyczne:
    ai.teach("[zaskoczenie]", pytanie)

print(f"{Colors.GREEN}✓ Pytania hipotetyczne: {len(pytania_hipotetyczne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA KONTROLNE - "Czy na pewno?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 10] PYTANIA KONTROLNE - weryfikacja...{Colors.RESET}")

pytania_kontrolne = [
    # Weryfikacja pewności
    "Czy na pewno?",
    "Jesteś pewien?",
    "Jesteś tego pewna?",
    "Na pewno?",
    "Absolutnie?",
    
    # Sprawdzenie zrozumienia
    "Rozumiesz?",
    "Jasne?",
    "Klarowne?",
    "Wszystko jasne?",
    "Masz pytania?",
    
    # Potwierdzenie
    "Potwierdzasz?",
    "Zgadzasz się?",
    "OK?",
    "Dobrze?",
    
    # Sprawdzenie gotowości
    "Gotowy?",
    "Gotowa?",
    "Możemy zacząć?",
    "Kontynuujemy?",
]

for pytanie in pytania_kontrolne:
    ai.teach("[akceptacja]", pytanie)

print(f"{Colors.GREEN}✓ Pytania kontrolne: {len(pytania_kontrolne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA PROWOKACYJNE - "Czy na pewno tak uważasz?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 11] PYTANIA PROWOKACYJNE - wyzwanie...{Colors.RESET}")

pytania_prowokacyjne = [
    # Kwestionowanie przekonań
    "Czy na pewno tak uważasz?",
    "Czy to rzeczywiście prawda?",
    "Skąd ta pewność?",
    "Czy rozważyłeś alternatywy?",
    "A może jest inaczej?",
    
    # Pytania o spójność
    "Czy to nie sprzeczne?",
    "Czy to się nie wyklucza?",
    "Jak to się ma do...?",
    "Czy to logiczne?",
    
    # Pytania o konsekwencje
    "A co z konsekwencjami?",
    "Czy o tym pomyślałeś?",
    "Co z resztą?",
    "A inne aspekty?",
]

for pytanie in pytania_prowokacyjne:
    ai.teach("[gniew]", pytanie)

print(f"{Colors.GREEN}✓ Pytania prowokacyjne: {len(pytania_prowokacyjne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA ZAMYKAJĄCE - "Czy to wszystko?"
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 12] PYTANIA ZAMYKAJĄCE - konkluzja...{Colors.RESET}")

pytania_zamykajace = [
    # Sprawdzenie kompletności
    "Czy to wszystko?",
    "Coś jeszcze?",
    "Nic więcej?",
    "To by było na tyle?",
    "Kończymy?",
    
    # Podsumowanie
    "Podsumowując?",
    "Reasumując?",
    "Co z tego wynika?",
    "Jaki jest wniosek?",
    
    # Pytania końcowe
    "Masz jeszcze jakieś pytania?",
    "Czy wszystko jasne?",
    "Czy mogę jeszcze w czymś pomóc?",
    "To wszystko czego potrzebujesz?",
]

for pytanie in pytania_zamykajace:
    ai.teach("[akceptacja]", pytanie)

print(f"{Colors.GREEN}✓ Pytania zamykające: {len(pytania_zamykajace)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PODSUMOWANIE
# ═══════════════════════════════════════════════════════════════════════════

ai.save_knowledge()

total = (len(pytania_podstawowe) + len(pytania_doprecyzowujace) + len(pytania_rozwijajace) +
         len(pytania_empatyczne) + len(pytania_filozoficzne) + len(pytania_zwrotne) +
         len(pytania_alternatywne) + len(pytania_retoryczne) + len(pytania_hipotetyczne) +
         len(pytania_kontrolne) + len(pytania_prowokacyjne) + len(pytania_zamykajace))

status = ai.get_soul_status()

print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GENESIS PYTANIA ZAKOŃCZONE")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Pytania dialogowe: {total} przykładów")
print(f"✓ Kategorie: 12")
print(f"✓ Wspomnienia łącznie: {status['memories']}")
print(f"✓ Masa duszy: {status['radius']:.4f}")
print(f"✓ Słowa w leksykonie: {status['lexicon']['total']}{Colors.RESET}")

print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
print(f"║  System nauczony zadawania pytań i budowania dialogu!            ║")
print(f"║  Nie tylko odpowiada - PYTA!                                     ║")
print(f"║                                                                   ║")
print(f"║  Uruchom: python main.py                                         ║")
print(f"╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")