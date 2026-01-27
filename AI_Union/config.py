# -*- coding: utf-8 -*-
"""
config.py - Compatibility wrapper
Przekierowuje do union_config.py (nowa struktura)
"""

# Import z nowego pliku
from union_config import UnionConfig as Config, Colors

# Dla kompatybilności wstecznej
SOUL_FILE = Config.SOUL_FILE
LEXICON_FILE = Config.LEXICON_FILE
DIMENSION = Config.DIMENSION
AXES = Config.AXES