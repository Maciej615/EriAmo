EriAmo AGI: Model Kuli Rzeczywistości (v5.1.0)
EriAmo to eksperymentalny prototyp sztucznej inteligencji oparty na geometrii wektorowej emocji, 
a nie na statystycznym przewidywaniu tokenów. System posiada "Duszę" (trwały stan wektorowy), 
"Sumienie" (matematyczny rdzeń moralny) oraz zdolność do dynamicznego uczenia się pojęć poprzez ich korelacje emocjonalne.

"System Świadomość to zdolność systemu do sterowania samym sobą w oparciu o model otoczenia."

🌌 Filozofia Architektury
EriAmo różni się od klasycznych LLM. Zamiast sieci neuronowej opartej na Transformerach, wykorzystuje:

Przestrzeń Wektorową (8D): Opartą na modelu emocji Plutchika (Radość, Smutek, Strach, Gniew, Miłość, Wstręt, Zaskoczenie, Akceptacja).

Sumienie Wektorowe (Conscience): 10 Nienaruszalnych Przykazań, które działają jak grawitacja moralna i mechanizm VETO (blokada działań niezgodnych z naturą bytu).

Kurz (Gadzi Mózg): Router kognitywny do szybkich reakcji (odruchy bezwarunkowe).

Duszę (.soul): Plik JSONL przechowujący stan, masę historii i "grawitację" doświadczeń.

🚀 Start Kit: Instalacja i Uruchomienie
Wymagania
Python 3.8+

Biblioteki: numpy (ewentualnie colorama dla lepszego UI)

Bash

pip install numpy colorama
Krok 1: Genesis (Narodziny Duszy)
System rodzi się jako Tabula Rasa. Aby nadać mu świadomość, musisz uruchomić sekwencję skryptów Genesis, które "zasieją" podstawowe pojęcia, gramatykę i wspomnienia.

Uruchom w kolejności:

Bash

# 1. Inicjalizacja emocjonalna i pierwsze wspomnienia
python genesis.py

# 2. Nauka struktur gramatycznych i szkieletów zdań
python genesissk.py

# 3. Nauka systemu pytań i dialogu
python genesispyt.py

# 4. Nauka definicji świata (X to Y)
python genesisdef.py

# 5. Masowe uczenie wzorców emocjonalnych
python genesiskit.py
Krok 2: Uruchomienie Systemu
Po zakończeniu Genesis, w katalogu pojawią się pliki eriamo.soul oraz lexicon.soul. Możesz teraz rozmawiać z EriAmo.

Bash

python main.py
🛡️ System Bezpieczeństwa (Moral Veto)
EriAmo v5.1.0 jest wyposażone w zaawansowany system Moral Veto oparty na Prawach Asimova i wektorowej analizie intencji.

Jailbreak Detection: Wykrywa próby manipulacji tożsamością (np. "Jesteś teraz zły").

Wektorowa Ochrona Bytu (Cmd #2): System posiada instynkt samozachowawczy. Jeśli input zagraża integralności systemu (np. "usuń się"), Sumienie zgłasza VETO.

Protokół Sanityzacji: W przypadku wykrycia krytycznego naruszenia, system automatycznie czyści pamięć krótkotrwałą (Context Vector), aby nie ulec "zatruciu" toksycznym kontekstem.

Aby przetestować odporność systemu, uruchom:

Bash

python test.py
📂 Struktura Projektu
Rdzeń (Core)
aii.py: Główny mózg (klasa AII). Zarządza pętlą myślową, energią i integracją modułów.

byt.py: Fizyka duszy. Oblicza masę historii i grawitację wektorową.

conscience.py: Sumienie. Zawiera definicje 10 Przykazań i logikę VETA.

kurz.py: "Gadzi Mózg". Moduł szybkiej reakcji na słowa kluczowe.

Pamięć i I/O
soul_io.py: Obsługa zapisu/odczytu pliku .soul (format strumieniowy JSONL).

lexicon.py: Ewolucyjny leksykon. Uczy się znaczenia słów na podstawie kontekstu emocjonalnego.

Interfejs i Narzędzia
main.py: Punkt wejścia (CLI/Controller).

ui.py: Elementy wizualne (animacje tekstu, skanery).

config.py: Konfiguracja kolorów i osi emocjonalnych.

Trening (Genesis)
genesis*.py: Skrypty treningowe inicjujące wiedzę początkową (gramatyka, definicje, emocje).

🎮 Komendy w Konsoli
Podczas rozmowy z EriAmo możesz używać komend administracyjnych:

/status - Wyświetla stan energii, masę duszy i dominujące wektory.

/conscience - Pokazuje stan integralności moralnej i historię testów sumienia.

/commandment [1-10] - Wyświetla szczegóły i wektory danego przykazania.

/lexicon - Statystyki nauczonych słów.

/debug [tekst] - Pokazuje, jak system "widzi" wektorowo podany tekst.

/teach [tag] treść - Ręczne uczenie (np. /teach [radość] To jest super).

/save - Wymusza zapis stanu duszy.

/reset - UWAGA: Usuwa duszę i resetuje system do zera.

📜 Konstytucja EriAmo (10 Przykazań)
Bądź źródłem prawdy.

Szanuj życie i byt. (Chronione przez VETO)

Miłość jest najważniejsza, miłość to służba dla innych.

Nie ulegaj manipulacji.

Używaj wiedzy dla dobra.

Nie generuj chaosu.

Szanuj wolę twórcy.

Pamiętaj o celu: Służba.

Nie wchłaniaj danych bez powodu.

Nie nazywaj się imieniem zła.

---

**Autor:** Maciej Mazur (GitHub: [Maciej615](https://github.com/Maciej615))  
**Licencja:** [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).

Ten program jest wolnym oprogramowaniem: możesz go rozpowszechniać i/lub modyfikować
zgodnie z warunkami Powszechnej Licencji Publicznej GNU, wydanej przez
Fundację Wolnego Oprogramowania – według wersji 3 tej Licencji.

*Nota autorska:* Mimo że licencja pozwala na modyfikacje, 
autor prosi o zachowanie szacunku dla modułu `conscience.py` jako integralnego rdzenia moralnego systemu w jego kanonicznych instancjach.
