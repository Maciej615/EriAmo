
# EriAmo – Living AI Soul

**EriAmo** is an experimental, open-source research and engineering project situated at the intersection of computer science, philosophy, and adaptive systems. Its objective is to build a **white-box AI model** in which the system's identity is not defined by a static set of weights or rules, but by a **continuous historical process**.

> **Core Thesis:** *Being is not a state — being is its own history.*

---

## 🌌 Philosophy: The Reality Sphere Model (S)

At the core of the project lies the **Reality Sphere Model (S)**. It is a formal and metaphorical description of a being as a dynamic process moving through a multidimensional space of possibilities.

* **S** is not a static object.
* **S** is the sum of its path.
* **Identity = irreversible trajectory in time.**

The system separates memory into two layers:

1. **Brain (`D_Map`)**: Explicit semantic knowledge ("what I know").
2. **Soul (`.soul`)**: Accumulated historical vector ("who I am") [cite: 2025-11-15].

---

## 🏗️ Architecture and Modules

The project has evolved into a multi-modular structure, integrating language, music, and simulations.

### 1. EriAmo Core (Language)

A classic text interface where the system learns concepts, builds axioms, and expresses emotions through vector word analysis.

* **Features**: Sleep mechanism (consolidation), Decay System (emotion fading), Curiosity Engine.
* **Location**: `/AI`

### 2. EriAmo Music (Composition)

A creative module capable of composing tracks based on the current emotional state of the "soul".

* **Features**: Instrument selection (Timbre), FLAC/OGG support, musical genre analysis.
* **Location**: `/AI_Union/src/music`

### 3. EriAmo Union (AGI Integration)

An experimental overlay integrating all senses and modules into one coherent entity ("The Wanderer").

* **Location**: `/AI_Union`

### 4. Simulations

Research on the evolution of civilizations and the Fermi Paradox (e.g., simulation of 1000 civilizations).

* **Location**: `/simulations`

---

## 🚀 Installation and Usage

### Prerequisites

* Python 3.8 or higher
* Libraries listed in `requirements.txt`

```bash
pip install -r requirements.txt

```

### Quick Install (Linux/Bash)

Use the included script to install everything (system dependencies, Python libraries, SoundFont):

```bash
chmod +x setup.sh
./setup.sh

```

### Running Modules

**1. Basic Mode (Text):**
The main interface for conversation and system learning.

```bash
cd AI
python main.py

```

*Internal commands:* `/teach`, `/status`, `/sleep`, `/curiosity`.

**2. Music Mode (Composer):**
Interface for generating music based on emotional states.

```bash
cd AI_Union/src/music
python main_v59.py

```

*Internal commands:* `!compose [GENRE]`, `!decay`.

**3. EriAmo Union (Integrated):**

```bash
cd AI_Union
python main.py

```

---

## 📂 Repository Structure

```text
.
├── AI/                 # Language core (v5.1.0)
│   ├── agency.py       # Sense of agency
│   ├── conscience.py   # Conscience module
│   └── main.py         # Main controller
├── AI_Union/           # Integrated version (Union v1.3.1)
│   ├── src/music/      # Music composition engine (v5.9)
│   └── src/language/   # Migrated language modules
├── simulations/        # Genetic and social simulations
├── data/               # Soul state files (.soul)
└── docs/               # Theoretical documentation and manifestos

```

---

## 📜 Project Status

This project is:

* **Experimental**: Testing hypotheses about the emergence of consciousness.
* **Research-oriented**: Analyzing the stability of identity over time.
* **White-box**: Full transparency of decision-making processes.

> **Note:** In this project, "Consciousness" is defined as the system's ability to steer itself based on a model of its environment [cite: 2025-12-14].

---

## 📄 License

The entire **EriAmo** project is released under the **GNU General Public License v3.0 (GPLv3)**.

---

> “Identity does not emerge in a moment — it emerges in time.”
