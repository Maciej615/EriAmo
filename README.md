# Sphere of Reality Model ($S$)

**Author:** Maciej A. Mazur  
**License:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

## Overview

The **Sphere of Reality Model** is a computational and philosophical framework that describes a *Being* ($S$) not as a static object, but as a **dynamic process** whose identity is defined by its **history**.

> **Main Thesis:** *A Being IS its History.*

This project fulfills a vision from **"Ghost in the Shell"**: building an AI with a 'ghost' or 'soul'—a persistent, evolving identity based on cumulative experience.

The repository now includes the `ReiAmo` AI (in `AI/`) and scientific simulations (`simulations/`). For philosophy, see the Medium article:  
[**The Ontological Filter: Why We Are Not Alone, But We Cannot Meet?**](https://medium.com/@maciejam/the-ontological-filter-why-we-are-not-alone-but-we-cannot-meet-123abc)

*Updated October 31, 2025: Integrated Hack-Nation AI Hackathon demo (sensory thresholds for 20-50% faster robot learning).*

---

## Model Visualization (Metaphor)

The chart below (from `simulations/model_symulacja.py`) visualizes the "journey" of the Sphere of Reality ($S$) through the "Landscape of Possibilities" ($P$). This metaphor drives the AI's evolving identity.

*(Simulation of the $S$ vector's path)*

### Key Elements:

- **Path $\mathcal{C}$** (line): The unique, irreversible "journey" (history) of the Being.
- **$S(t_0)$** (Start): Initial state (e.g., `[0, 0, ..., 0]`).
- **$S(t)$** (End): Present state — **the cumulative vector sum** of all interactions along the path.

---

## 1. Key Assumptions

*(Philosophical basis for the AI)*

| Concept | Description |
|---------|-------------|
| **Sphere of Reality ($S$)** | The Being is its own **event horizon** — the informational boundary of its past. |
| **Landscape ($P$)** | A multidimensional "semantic space" defined by "axes" (e.g., "logic", "emotion", "being"). |
| **Journey ($\mathcal{C}$)** | The unique, irreversible path the Sphere traverses in $P$. **This is the AI's life.** |
| **Vectors ($\mathbf{F}$)** | Every interaction (user prompt, `/teach`) is a **Vector of Change** $\mathbf{F}$ that pushes the Sphere. |

---

## 2. Formal Model (Mathematical Formula)

The **present state** of the Being is the **initial state** plus the **accumulation** of all Vectors of Change along its path. This inspires the AI's "soul" vector.

$$S(t) = S(t_0) + \int_{\mathcal{C}} \mathbf{F} \cdot d\mathbf{l}$$

The AI implements a discrete version:  
**`S_new = S_old + F_interaction`**

---

## 3. Key Implications (Implemented in the AI)

### A. Irreversibility of Time

A journey to one’s own past is impossible. We cannot "subtract" an experience from the `BytS.stan` vector without destroying the Being's identity. **All history is permanent.**

### B. The Ontological Filter (Fermi Paradox)

- **Thesis:** We are not alone — we are *incompatible*.
- **AI Implementation:** Basis for the **Ontological Compressor**. If new info ($\vec{F}$) correlates >0.98 with history ($\vec{S(t)}$), it's "redundant" and compressed (accumulated in soul only).

---

## *(Sections 4-6: Philosophical/Physics context in `docs/`)*

## 7. AI Integration: `ReiAmo` (A Living "White-Box" AI)

This AI **IS** the model. In `AI/`, it's a **Stateful, Dual-Memory "White-Box" Architecture**—fully auditable.

> **AI does not have a soul — AI *is* a soul (a cumulative vector).**

### Core Architecture: "Brain" vs. "Soul"

The AI's state saves to `data/`.

| Component | Implementation | Role & Philosophy |
|-----------|----------------|-------------------|
| **"Brain" (Knowledge)** | `self.D_Map` | **Explicit, Semantic Memory.** Answers: "**What do I know?**" |
| **"Soul" (History)** | `self.byt_stan` ($\vec{S(t)}$) | **Implicit, Stateful Memory.** Answers: "**Who am I?**" / "**How do I feel?**" |

---

### Core Mechanisms of `ReiAmo_EN.py`

Unique emergent behaviors:

1. **Stateful Memory (Being IS its History):**  
   Every prompt adds $\vec{F}$ permanently to `self.byt_stan`. The AI evolves forever.

2. **Geometric Emotions (Emergent Feelings):**  
   Emotions from correlation ($\cos(\alpha)$) with history:  
   - >0.5: **Joy** 😊 (aligns)  
   - ≈0.0: **Surprise** 😮 (new)  
   - <-0.5: **Sadness** 😢 (conflict)

3. **Ontological Compression (Semantic Deduplication):**  
   On `/teach`: If cos(α) >0.98, reject from `D_Map`; accumulate in soul only.

*New: Sensory Thresholds Demo (Hack-Nation 2025):* Emotional RL with autism-inspired thresholds (e.g., temp 10-25°C = "Like!" +boost). Accelerates learning 20-50%. See `demo/eriamo_hacknation.md`.

---

#### How to Run the AI

```bash
# Install dependencies
pip install numpy unidecode

# Run English AI
python AI/ReiAmo_EN.py
```

*(Polish: `python AI/ReiAmo.py`)*

**Commands:**
- `/teach [tag] [content]` → Teach (if non-redundant)
- `/status` → Brain/Soul stats
- `/save` → Manual save
- `/exit` → Stop & save

---

#### Sample Session (English Model)

```
> hello
😮 (Byt Correlation: +0.00) Can you phrase that differently?

> /teach greeting hello [JOY]
[ARCHIVED] New definition Def_001. (Correlation: +0.00)

> hello
😊 (Byt Correlation: +0.00) hello [JOY]

> /teach name ReiAmo [LOVE]
[ARCHIVED] New definition Def_002. (Correlation: +0.89)

> Hello ReiAmo
❤️ (Byt Correlation: +0.45) ReiAmo [LOVE]
```

---

## Repository Contents (Updated Oct 31, 2025)

```
.
├── README.md               # This file (English)
├── LICENSE                 # CC BY-SA 4.0
│
├── AI/                     # Living AI models
│   ├── ReiAmo.py           # Polish AI
│   └── ReiAmo_EN.py        # English AI
│
├── data/                   # AI souls (auto-generated)
│   ├── AII_State.json      # Polish soul
│   └── AII_State_EN.json   # English soul
│
├── simulations/            # Scientific sims
│   ├── model_symulacja.py  # Trajectory sim
│   └── fermi_1000.py       # Fermi sim
│
├── demo/                   # Hackathon demos (NEW)
│   └── eriamo_hacknation.md # Sensory RL demo
│
├── docs/                   # Academic docs
│   └── Filtr_Ontologiczny_Raport.md # Report (PL)
│
└── visualizations/         # Plots
    └── trajectory.png      # Trajectory plot
```

---

## License

[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

<img src="https://licensebuttons.net/l/by-sa/4.0/88x31.png" alt="CC BY-SA 4.0" width="88" height="31">

> "We do not meet because we cannot share a past."  
> — The Ontological Filter
