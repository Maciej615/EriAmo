#!/bin/bash

echo "╔════════════════════════════════════════════╗"
echo "║      EriAmo Union - Setup Environment      ║"
echo "╚════════════════════════════════════════════╝"

# 1. Instalacja zależności systemowych (Linux/Debian/Ubuntu)
if [ -x "$(command -v apt-get)" ]; then
    echo "\n[SYSTEM] Instalowanie pakietów audio (fluidsynth, ffmpeg)..."
    sudo apt-get update
    sudo apt-get install -y fluidsynth ffmpeg
else
    echo "\n[UWAGA] Nie wykryto apt-get. Jeśli nie jesteś na Debian/Ubuntu, zainstaluj ręcznie: fluidsynth, ffmpeg."
fi

# 2. Instalacja zależności Python
echo "\n[PYTHON] Instalowanie bibliotek z requirements.txt..."
pip install -r requirements.txt

# 3. Pobranie SoundFontu (wymagane dla modułu muzycznego)
echo "\n[AUDIO] Pobieranie SoundFontu (FluidR3_GM.sf2)..."
python3 AI_Union/src/music/download_soundfont.py

echo "\n✅ Gotowe! Możesz uruchomić EriAmo."
echo "   -> Tekst: cd AI && python main.py"
echo "   -> Muzyka: cd AI_Union/src/music && python main_v59.py"
