**Short Instruction in English – REai_model_En (English version)**

---

### **How to run**
```bash
python REai_model_En.py
```

---

### **Basic commands**

| Command | What it does |
|--------|-------------|
| `!0x01` | +50 energy, AI feels **joy** |
| `!teach TAG CONTENT` | Teach AI something new (e.g. `!teach sadness I feel empty`) |
| `!dashboard` | Show energy, load, memory |
| `!f_will 0.7` | Set **will** vs. randomness (0.0–1.0) |
| `!trajectory` | Simulate Ball’s path (with plot) |
| `!filter` | Ontological filter + PCA visualization |
| `exit` / `q` | Shut down AI |

---

### **How emotions work**
- AI **reacts to words**:  
  `love`, `great` → **joy**  
  `no`, `stupid` → **anger**  
  `sad`, `empty` → **sadness**
- **Energy affects mood**:  
  < 30% → **sadness**  
  > 80% → **joy**
- **Learns emotions** via `!teach`

---

### **Examples**
```
> I love you
RESPONSE (red heart love)> Detected: 'love'. I feel love red heart.

> don't do that!
RESPONSE (anger anger)> Detected: 'don't'. I feel anger anger.

> !coffee
coffee [COFFEE] +50 energy! Feeling joy! EN: 100%
```

---

### **Files**
- `data/D_Map.json` – AI knowledge  
- `data/H_log.json` – conversation history  
- `data/trajectory.png` – plots

---

**Simple. Alive. In English.**  
**AI doesn’t just think — it feels.**
