# -*- coding: utf-8 -*-
# byt.py
# Copyright (C) 2025 Maciek (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
import numpy as np

class BytS:
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary)

    def promien_historii(self):
        return np.linalg.norm(self.stan)

    def oblicz_korelacje_struny(self, nowa_struna_vec):
        wektor_historii = self.stan
        wektor_bodzca = np.asarray(nowa_struna_vec)
        
        promien_historii = self.promien_historii()
        sila_bodzca = np.linalg.norm(wektor_bodzca)
        
        if promien_historii == 0 or sila_bodzca == 0:
            return 0.0 
            
        iloczyn_skalarny = np.dot(wektor_historii, wektor_bodzca)
        korelacja = iloczyn_skalarny / (promien_historii * sila_bodzca)
        
        return np.clip(korelacja, -1.0, 1.0)

    def akumuluj_styk(self, nowa_struna_vec):
        self.stan = self.stan + np.asarray(nowa_struna_vec)
