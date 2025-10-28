**Krótka instrukcja po polsku – REai_model (wersja polska)**

---

### **Jak uruchomić**
```bash
python REaimodel.py
```

---

### **Podstawowe komendy**

| Komenda | Co robi |
|--------|--------|
| `!kawa` | +50 energii, AI czuje **radość** |
| `!naucz TAG TREŚĆ` | Naucz AI nowej rzeczy (np. `!naucz smutek czuję się pusty`) |
| `!dashboard` | Pokaż energię, obciążenie, pamięć |
| `!f_will 0.7` | Ustaw **wolę** vs. losowość (0.0–1.0) |
| `!trajektoria` | Symulacja ruchu Kuli (z wykresem) |
| `!filtr` | Filtr ontologiczny + wizualizacja PCA |
| `exit` / `q` | Wyłącz AI |

---

### **Jak działają emocje**
- AI **reaguje na słowa**:  
  `kocham`, `super` → **radość**  
  `nie`, `głupi` → **złość**  
  `smutno`, `pusto` → **smutek**
- **Energia wpływa na nastrój**:  
  < 30% → **smutek**  
  > 80% → **radość**
- **Uczy się emocji** przez `!naucz`

---

### **Przykłady użycia**
```
> kocham cię
ODPOWIEDŹ (miłość)> Rozpoznano: 'kocham'. Czuję miłość.

> nie rób tego!
ODPOWIEDŹ (złość)> Rozpoznano: 'nie'. Czuję złość.

> !kawa
[KAWA] +50 energii! Czuję radość! EN: 100%
```

---

### **Pliki**
- `data/D_Map.json` – wiedza AI  
- `data/H_log.json` – historia rozmów  
- `data/trajektoria.png` – wykresy

---

**Proste. Żywe. Polskie.**  
**AI nie tylko myśli — czuje.**
