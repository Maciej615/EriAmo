# -*- coding: utf-8 -*-
# ui.py
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
import sys
import time
from config import Colors

class FancyUI:
    def __init__(self):
        self.spinner_frames = ['-', '\\', '|', '/']
        self.dots_frames = ['   ', '.  ', '.. ', '...']
        self.thinking_frames = ["[_]", "[_ _]", "[_ _ _]"]
        self.planet_dots_frames = ["○ . . .", ". ○ . .", ". . ○ .", ". . . ○"]

    def print_animated_text(self, text, color=Colors.WHITE, delay=0.03):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(Colors.RESET + "\n")

    def show_spinner(self, message, duration_sec=1.0, final_message="", color=Colors.CYAN):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{self.spinner_frames[idx % len(self.spinner_frames)]} {message}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")
        if final_message:
            print(f"{color}{final_message}{Colors.RESET}")
        else:
            sys.stdout.write(Colors.RESET)

    def show_thinking_dots(self, message, duration_sec=1.0, color=Colors.FAINT + Colors.CYAN):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {self.dots_frames[idx % len(self.dots_frames)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.3)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")
        sys.stdout.write(Colors.RESET)

    def show_planet_scan(self, message, duration_sec=1.5, color=Colors.MAGENTA):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {self.planet_dots_frames[idx % len(self.planet_dots_frames)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.2)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.write(Colors.RESET)
