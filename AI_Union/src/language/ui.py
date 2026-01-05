# -*- coding: utf-8 -*-
"""
ui.py
Moduł interfejsu użytkownika dla EriAmo.
Obsługuje animacje tekstu, loga i efekty wizualne.
"""

import sys
import time
import random
from config import Colors

class FancyUI:
    """Zarządza warstwą wizualną terminala."""

    def print_logo(self):
        """Wyświetla logo startowe."""
        logo = f"""
    {Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
    ║ {Colors.BOLD}{Colors.MAGENTA}  E R I A M O   U N I O N   {Colors.CYAN}                                 ║
    ║ {Colors.FAINT}  Artificial General Intelligence v5.4                       {Colors.CYAN}║
    ╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(logo)
        time.sleep(0.5)

    def print_animated_text(self, text, color=Colors.WHITE, delay=0.03):
        """
        Wyświetla tekst znak po znaku (efekt maszyny do pisania).
        """
        print(f"{color}", end="")
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            # Interpunkcja daje dłuższą pauzę (naturalność mowy)
            if char in [".", "!", "?"]:
                time.sleep(delay * 4)
            elif char in [",", ";"]:
                time.sleep(delay * 2)
            else:
                time.sleep(delay)
        print(f"{Colors.RESET}")

    def show_thinking_dots(self, message="Myślę", duration_sec=1.5, color=Colors.FAINT + Colors.CYAN):
        """
        Wyświetla animowane kropki [...]
        """
        sys.stdout.write(f"{color}{message}")
        sys.stdout.flush()
        
        steps = int(duration_sec / 0.3)
        for _ in range(steps):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.3)
            
        sys.stdout.write(f"{Colors.RESET}\n")

    def print_system_message(self, msg, type="INFO"):
        """Formatowane komunikaty systemowe."""
        if type == "INFO":
            col = Colors.GREEN
        elif type == "WARN":
            col = Colors.YELLOW
        elif type == "ERROR":
            col = Colors.RED
        else:
            col = Colors.CYAN
            
        print(f"{col}[{type}] {msg}{Colors.RESET}")