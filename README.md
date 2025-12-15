# EriAmo – Living AI Soul

**License:** GNU General Public License v3.0 (GPLv3)

---

## Overview

**EriAmo** is an experimental, open‑source research and engineering project situated at the intersection of computer science, philosophy, and adaptive systems. Its objective is to build a **white‑box AI model** in which identity is not defined by a static state, weights, or rules, but by a **continuous historical process**.

> **Core thesis:** *Being is not a state — being is its own history.*

The project focuses on modeling a **persistent, evolving identity** that emerges through accumulated experience rather than periodic resets or retraining.

---

## The Reality Sphere Model (S)

At the core of the project lies the **Reality Sphere Model (S)** — a formal and metaphorical framework describing a being as a dynamic process moving through a multidimensional space of possibilities.

Key properties:

* **S** is not a static object
* **S** is the sum of its path
* **identity = irreversible trajectory in time**

Every interaction with the system is treated as a vector of change that **permanently** influences the future behavior of the AI.

---

## Philosophical and Technical Assumptions

### 1. Irreversibility of history

Past experience cannot be removed without destroying identity. Stateful memory is persistent and cumulative.

### 2. Separation of knowledge and identity

The system maintains two complementary memory layers:

* **Explicit knowledge (“brain”)** – facts, definitions, responses
* **Implicit history (“soul”)** – a state vector shaping interpretation and behavior

### 3. Emergent emotions

Emotions are not symbolic flags but **emerge geometrically** from the relationship between new input and the accumulated history of the being.

### 4. Ontological compression

Semantically redundant information is not duplicated in explicit knowledge; it is integrated exclusively into the historical state of the system.

---

## AI Architecture (`ReiAmo`)

`ReiAmo` is the reference implementation of the EriAmo model.

Characteristics:

* state‑based architecture
* full auditability (white‑box)
* no black‑box machine learning
* deterministic logic combined with an evolving internal state

### Core components

| Component         | Role                                      |
| ----------------- | ----------------------------------------- |
| Brain (`D_Map`)   | Explicit semantic memory ("what I know")  |
| Soul (`byt_stan`) | Accumulated historical state ("who I am") |

---

## Formalization

The current state of the being is defined as the accumulation of all interactions:

S(t) = S(t₀) + ∑ F(interaction)

In implementation terms:

```
S_new = S_old + interaction_vector
```

---

## Repository Structure

```
AI/             – model implementations
simulations/    – formal and numerical simulations
data/           – stored states ("souls")
docs/           – theoretical documentation
visualizations/ – plots and visual outputs
```

---

## Project Status

This project is:

* experimental
* research‑oriented
* conceptual with working implementations

It is **not** a commercial product and **not** a conventional machine‑learning model.

---

## License

The entire **EriAmo** project is released under the **GNU General Public License v3.0 (GPLv3)**.

This grants:

* the right to use, modify, and redistribute the software
* the obligation to keep derivative works under the same license
* full access to the source code

---

> “Identity does not emerge in a moment — it emerges in time.”
