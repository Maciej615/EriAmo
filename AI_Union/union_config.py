"""
EriAmo Union - Centralna Konfiguracja
======================================
SINGLE SOURCE OF TRUTH dla wszystkich definicji osi i konfiguracji systemu.

Wszystkie moduły MUSZĄ importować definicje stąd:
    from union_config import UnionConfig, AXES, DIMENSION, Colors
"""

import os
from typing import List, Dict, Set
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINICJE OSI - SINGLE SOURCE OF TRUTH
# ═══════════════════════════════════════════════════════════════════════════════

# Główna lista 15 osi (8 biologicznych + 7 metafizycznych)
AXES: List[str] = [
    # Biologiczne (Plutchik) - indeksy 0-7
    'radość', 'smutek', 'strach', 'gniew',
    'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
    # Metafizyczne - indeksy 8-14
    'logika', 'wiedza', 'czas', 'kreacja',
    'byt', 'przestrzeń', 'chaos'
]

# Wymiarowość
DIMENSION: int = 15
BIO_DIM: int = 8    # Wymiary biologiczne (emocje Plutchika)
META_DIM: int = 7   # Wymiary metafizyczne

# Podział funkcjonalny
BIO_AXES: List[str] = AXES[:BIO_DIM]   # Emocje biologiczne
META_AXES: List[str] = AXES[BIO_DIM:]  # Wymiary metafizyczne

# Indeksy dla szybkiego dostępu
AXES_INDEX: Dict[str, int] = {axis: i for i, axis in enumerate(AXES)}

# ═══════════════════════════════════════════════════════════════════════════════
# KLASYFIKACJA OSI DLA SYSTEMU MUZYCZNEGO
# (zastępuje stare EPHEMERAL_AXES / PERSISTENT_AXES z amocore.py)
# ═══════════════════════════════════════════════════════════════════════════════

# Osie efemeryczne - szybko wygasające stany emocjonalne
EPHEMERAL_AXES: List[str] = [
    'radość', 'smutek', 'strach', 'gniew', 'zaskoczenie'
]

# Osie trwałe - stabilne cechy i preferencje
PERSISTENT_AXES: List[str] = [
    'miłość', 'wstręt', 'akceptacja',
    'logika', 'wiedza', 'kreacja', 'byt', 'przestrzeń'
]

# Osie dynamiczne - zmienne w czasie
DYNAMIC_AXES: List[str] = ['czas', 'chaos']

# Zbiory dla szybkiego sprawdzania przynależności
EPHEMERAL_SET: Set[str] = set(EPHEMERAL_AXES)
PERSISTENT_SET: Set[str] = set(PERSISTENT_AXES)
DYNAMIC_SET: Set[str] = set(DYNAMIC_AXES)

# ═══════════════════════════════════════════════════════════════════════════════
# ALIASY DLA KOMPATYBILNOŚCI WSTECZNEJ
# (dla modułów używających starych nazw z amocore.py)
# ═══════════════════════════════════════════════════════════════════════════════

# Alias dla starego AXES_LIST z amocore.py
AXES_LIST: List[str] = AXES


# ═══════════════════════════════════════════════════════════════════════════════
# KOLORY TERMINALA
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Kolory ANSI dla terminala."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RESET = '\033[0m'  # Alias dla kompatybilności z explorer.py
    
    # Aliasy dla emocji
    JOY = GREEN
    SADNESS = BLUE
    FEAR = MAGENTA
    ANGER = RED
    LOVE = '\033[38;5;213m'  # Różowy
    DISGUST = '\033[38;5;58m'  # Oliwkowy
    SURPRISE = YELLOW
    ACCEPTANCE = CYAN


# ═══════════════════════════════════════════════════════════════════════════════
# GŁÓWNA KLASA KONFIGURACJI
# ═══════════════════════════════════════════════════════════════════════════════

class UnionConfig:
    """
    Centralna konfiguracja systemu EriAmo Union.
    
    Użycie:
        from union_config import UnionConfig
        
        print(UnionConfig.AXES)      # Atrybut klasowy
        print(UnionConfig.DIMENSION) # Atrybut klasowy
    """
    
    # === OSIE (atrybuty KLASOWE - dostępne bez instancji) ===
    AXES = AXES
    DIMENSION = DIMENSION
    BIO_DIM = BIO_DIM
    META_DIM = META_DIM
    
    BIO_AXES = BIO_AXES
    META_AXES = META_AXES
    
    EPHEMERAL_AXES = EPHEMERAL_AXES
    PERSISTENT_AXES = PERSISTENT_AXES
    DYNAMIC_AXES = DYNAMIC_AXES
    
    # Alias dla kompatybilności wstecznej
    AXES_LIST = AXES_LIST
    
    # === ŚCIEŻKI ===
    BASE_DIR = Path(__file__).parent
    SOUL_DIR = Path(__file__).parent / "souls"
    MUSIC_DIR = Path(__file__).parent / "music"
    LOGS_DIR = Path(__file__).parent / "logs"
    
    # === PAMIĘĆ ===
    MEMORY_DECAY = 0.95
    EMOTION_DECAY = 0.85
    MAX_MEMORY_SIZE = 10000
    
    # === MUZYKA ===
    DEFAULT_BPM = 120
    DEFAULT_SOUNDFONT = "FluidR3_GM.sf2"
    
    # === SYSTEM ===
    VERSION = "8.7.0"
    DEBUG = False
    
    @classmethod
    def init_dirs(cls):
        """Tworzy katalogi jeśli nie istnieją."""
        for dir_path in [cls.SOUL_DIR, cls.MUSIC_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_axis_index(cls, axis_name: str) -> int:
        """Zwraca indeks osi po nazwie."""
        return AXES_INDEX.get(axis_name, -1)
    
    @classmethod
    def is_ephemeral(cls, axis_name: str) -> bool:
        """Sprawdza czy oś jest efemeryczna."""
        return axis_name in EPHEMERAL_SET
    
    @classmethod
    def is_persistent(cls, axis_name: str) -> bool:
        """Sprawdza czy oś jest trwała."""
        return axis_name in PERSISTENT_SET
    
    @classmethod
    def is_biological(cls, axis_name: str) -> bool:
        """Sprawdza czy oś jest biologiczna (emocja Plutchika)."""
        return axis_name in BIO_AXES
    
    @classmethod
    def is_metaphysical(cls, axis_name: str) -> bool:
        """Sprawdza czy oś jest metafizyczna."""
        return axis_name in META_AXES


# ═══════════════════════════════════════════════════════════════════════════════
# ALIASY DLA KOMPATYBILNOŚCI WSTECZNEJ
# (dla plików importujących z config.py)
# ═══════════════════════════════════════════════════════════════════════════════

# Alias klasy Config -> UnionConfig
Config = UnionConfig


# ═══════════════════════════════════════════════════════════════════════════════
# EKSPORTY MODUŁU
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Główne definicje osi
    'AXES',
    'DIMENSION',
    'BIO_DIM',
    'META_DIM',
    'BIO_AXES',
    'META_AXES',
    'AXES_INDEX',
    
    # Klasyfikacja osi
    'EPHEMERAL_AXES',
    'PERSISTENT_AXES',
    'DYNAMIC_AXES',
    'EPHEMERAL_SET',
    'PERSISTENT_SET',
    'DYNAMIC_SET',
    
    # Aliasy kompatybilności
    'AXES_LIST',
    
    # Klasy
    'UnionConfig',
    'Config',  # Alias dla kompatybilności
    'Colors',
]


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"{Colors.CYAN}=== EriAmo Union Config ==={Colors.END}")
    print(f"\n{Colors.GREEN}AXES ({DIMENSION}):{Colors.END}")
    
    for i, axis in enumerate(AXES):
        category = "BIO" if i < BIO_DIM else "META"
        ephemeral = "⚡" if axis in EPHEMERAL_SET else ""
        persistent = "🔒" if axis in PERSISTENT_SET else ""
        dynamic = "🔄" if axis in DYNAMIC_SET else ""
        print(f"  [{i:2d}] {axis:12s} ({category}) {ephemeral}{persistent}{dynamic}")
    
    print(f"\n{Colors.YELLOW}Klasyfikacja:{Colors.END}")
    print(f"  Efemeryczne: {EPHEMERAL_AXES}")
    print(f"  Trwałe:      {PERSISTENT_AXES}")
    print(f"  Dynamiczne:  {DYNAMIC_AXES}")