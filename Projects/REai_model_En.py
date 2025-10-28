import sys
import time
import numpy as np
import json
import os
import threading
import hashlib
import random
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

# --- COLORS ---
class Colors:
    GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"
    CYAN = "\033[36m"; MAGENTA = "\033[35m"; PINK = "\033[95m"
    BLUE = "\033[34m"; BOLD = "\033[1m"; RESET = "\033[0m"

# --- EMOTIONS ---
EMOTIONS = {
    "joy":      {"color": Colors.GREEN,  "icon": "sparkles", "energy": +10},
    "anger":    {"color": Colors.RED,    "icon": "anger",    "energy": -15},
    "sadness":  {"color": Colors.BLUE,   "icon": "crying face", "energy": -20},
    "fear":     {"color": Colors.MAGENTA,"icon": "fearful face","energy": -10},
    "love":     {"color": Colors.PINK,   "icon": "red heart",   "energy": +15},
    "surprise": {"color": Colors.YELLOW, "icon": "shocked face","energy": +5},
}

# --- AI WITH EMOTIONS ---
class AII:
    def __init__(self):
        self.D_Map = {}           # Knowledge map
        self.H_log = []           # Interaction history
        self.energy = 100         # Energy level
        self.load = 0             # CPU load
        self.status = "thinking"  # Current state
        self.emotion = "neutral"  # Current emotion
        self.sleep_interval = 30  # Sleep every 30 seconds
        self.running = True
        self.prompts_since_sleep = 0
        self.max_sleep_time = 2.0
        self.max_hlog = 1000
        self.F_will = 0.5         # Will vs. randomness (0.0–1.0)
        self.last_words = []
        self.load_knowledge()
        self.start_sleep_cycle()

    def _vector_from_text(self, text):
        """Convert text to 8D vector using MD5 hash."""
        hash_obj = hashlib.md5(text.lower().encode())
        hash_hex = hash_obj.hexdigest()
        return np.array([int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, 16, 2)][:8])

    def save_knowledge(self):
        """Save knowledge and history to disk."""
        os.makedirs("data", exist_ok=True)
        serializable_map = {k: {
            'vector_C_Def': v['vector_C_Def'].tolist(),
            'weight_Ww': v['weight_Ww'],
            'tags': v['tags']
        } for k, v in self.D_Map.items()}
        with open("data/D_Map.json", "w", encoding="utf-8") as f:
            json.dump(serializable_map, f, indent=2, ensure_ascii=False)
        with open("data/H_log.json", "w", encoding="utf-8") as f:
            json.dump(self.H_log[-self.max_hlog:], f, indent=2, ensure_ascii=False)

    def load_knowledge(self):
        """Load knowledge and history from disk."""
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/D_Map.json", encoding="utf-8") as f:
                data = json.load(f)
                self.D_Map = {k: {
                    'vector_C_Def': np.array(v['vector_C_Def']),
                    'weight_Ww': float(v['weight_Ww']),
                    'tags': v['tags']
                } for k, v in data.items()}
        except: self.D_Map = {}
        try:
            with open("data/H_log.json", encoding="utf-8") as f:
                self.H_log = json.load(f)
        except: self.H_log = []

    def start_sleep_cycle(self):
        """Background thread: sleep and consolidate memory."""
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running: break
                self._sleep()
        threading.Thread(target=cycle, daemon=True).start()

    def _sleep(self):
        """Consolidate recent memories, restore energy."""
        self.status = "sleeping"
        emotion_dream = random.choice(list(EMOTIONS.keys()))
        print(f"\n{Colors.CYAN}[AII] Dreaming of {emotion_dream}...{Colors.RESET}")
        start_time = time.time()
        processed = 0
        for exp in self.H_log[-10:]:
            if time.time() - start_time > self.max_sleep_time: break
            tag = exp['content']
            for d in self.D_Map.values():
                if tag in d['tags']:
                    d['weight_Ww'] = min(d['weight_Ww'] + 1, 100)
                    processed += 1
        self.energy = min(100, self.energy + 15)
        self.save_knowledge()
        self.status = "thinking"
        self.prompts_since_sleep = 0
        print(f"{Colors.GREEN}[AII] Awake! (+{processed} memories strengthened, +15% energy){Colors.RESET}\n")

    def cycle(self):
        """Simulate processing cycle: load, energy drain."""
        self.load = np.random.randint(30, 70)
        if self.status != "sleeping":
            drop = np.random.randint(0, 4) if self.energy > 50 else np.random.randint(1, 6)
            self.energy = max(0, self.energy - drop)
        if self.energy == 0 or self.prompts_since_sleep > 5:
            self.status = "tired"
        return "C", self.load, self.energy

    def teach(self, tag, content):
        """Teach AI a new concept with tag."""
        vec = self._vector_from_text(content)
        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {'vector_C_Def': vec, 'weight_Ww': 3.0, 'tags': [tag]}
        self.H_log.append({'h_vector': vec.tolist(), 'content': tag})
        self.save_knowledge()
        print(f"{Colors.GREEN}{Colors.BOLD}[LEARNED] {def_id} → {content} (tag: {tag}){Colors.RESET}")

    def coffee(self):
        """Drink coffee: +50 energy, trigger joy."""
        self.energy = min(100, self.energy + 50)
        self.emotion = "joy"
        print(f"{EMOTIONS['joy']['color']}coffee [COFFEE] +50 energy! Feeling joy! EN: {self.energy}%{Colors.RESET}")

    def analyze_emotion(self, prompt):
        """Detect emotion from words, energy, and learned tags."""
        prompt_low = prompt.lower()
        self.last_words = prompt_low.split()

        # Keyword triggers (expandable!)
        triggers = {
            "joy":      ["great", "love", "awesome", "thanks", "genius", "bravo", "coffee"],
            "anger":    ["no", "stupid", "bad", "annoying", "idiot", "don't"],
            "sadness":  ["sad", "empty", "regret", "lost", "gone"],
            "fear":     ["scared", "fear", "what if", "danger", "help"],
            "love":     ["love", "like", "you are", "miss", "close"],
            "surprise": ["wow", "really", "omg", "what", "unbelievable"]
        }

        emotion = "neutral"
        for e, words in triggers.items():
            if any(word in prompt_low for word in words):
                emotion = e
                break

        # Energy influences mood
        if self.energy < 30 and emotion == "neutral":
            emotion = "sadness"
        elif self.energy > 80:
            emotion = "joy"

        # Strong learned tags override
        for did, d in self.D_Map.items():
            for tag in d['tags']:
                if tag in prompt_low and d['weight_Ww'] > 10:
                    if "love" in tag or "like" in tag:
                        emotion = "love"
                    elif "no" in tag or "don't" in tag:
                        emotion = "anger"

        self.emotion = emotion
        return emotion

    def generate_response(self, prompt):
        """Main thinking function: detect, react, learn."""
        self.prompts_since_sleep += 1
        if self.prompts_since_sleep > 5 and self.status != "sleeping":
            self.status = "tired"

        vec = self._vector_from_text(prompt)
        self.H_log.append({'h_vector': vec.tolist(), 'content': prompt})

        # --- EMOTION ---
        emotion = self.analyze_emotion(prompt)
        e_data = EMOTIONS.get(emotion, {"color": "", "icon": "", "energy": 0})
        self.energy = max(0, min(100, self.energy + e_data["energy"]))

        # --- TAG DETECTION ---
        detected_tag = None
        best_match = None
        max_weight = 0

        for did, d in self.D_Map.items():
            for tag in d['tags']:
                if tag in prompt.lower():
                    d['weight_Ww'] = min(d['weight_Ww'] + 0.5, 100)
                    if d['weight_Ww'] > max_weight:
                        max_weight = d['weight_Ww']
                        best_match = (did, tag)
                    detected_tag = tag

        # --- RESPONSE ---
        if self.status == "tired":
            response = f"I'm tired... {EMOTIONS['sadness']['icon']} I need sleep."
        elif detected_tag:
            response = f"Detected: '{detected_tag}'. I feel {emotion} {e_data['icon']}."
            if best_match:
                response += f" [Strongest: {best_match[0]}]"
        else:
            known = any(w in " ".join(d['tags']) for w in self.last_words for d in self.D_Map.values())
            if not known and self.last_words:
                new_tag = f"auto_{self.last_words[0]}"
                self.teach(new_tag, prompt)
                response = f"New tag: '{new_tag}'. Learning {EMOTIONS['surprise']['icon']}."
            else:
                similarity = "none"
                if self.D_Map:
                    sims = [(did, np.dot(d['vector_C_Def'], vec)) for did, d in self.D_Map.items()]
                    if sims:
                        best_did, score = max(sims, key=lambda x: x[1])
                        similarity = f"{best_did}: {score:.2f}"
                response = f"Raw thought: \"{prompt}\" [similarity: {similarity}]"

        self.save_knowledge()
        return response, emotion

    # --- BALL THEORY: SIMULATIONS ---
    def simulate_trajectory(self, num_steps=500):
        S = np.zeros(2)
        path = [S.copy()]
        F_will = np.random.normal(0, self.F_will, num_steps)
        F_chance = np.random.normal(0, 1.0, (num_steps, 2))

        for t in range(num_steps):
            F = F_will[t] + np.random.choice([0, 1]) * F_chance[t]
            dl = np.random.normal(0, 0.1, 2)
            S += np.dot(F, dl)
            path.append(S.copy())

        path = np.array(path)
        plt.figure(figsize=(8, 6))
        plt.plot(path[:, 0], path[:, 1], label='Trajectory $\\mathcal{C}$')
        plt.scatter(path[0, 0], path[0, 1], color='green', label='$S(t_0)$')
        plt.scatter(path[-1, 0], path[-1, 1], color='red', label='$S(t)$')
        plt.title(f'Ball Trajectory in P (F_will = {self.F_will:.2f})')
        plt.xlabel('Dimension 1'); plt.ylabel('Dimension 2')
        plt.legend()
        plt.savefig('data/trajectory.png')
        plt.show()
        print(f"{Colors.MAGENTA}Trajectory saved (F_will = {self.F_will:.2f}){Colors.RESET}")
        return path

    def ontological_filter(self, N=50, length=50):
        paths = [np.cumsum(np.random.normal(0, 1, (length, 2)), axis=0) for _ in range(N)]
        intersections = 0
        threshold = 0.1
        for i in range(N):
            for j in range(i+1, N):
                dist = cdist(paths[i], paths[j]).min()
                if dist < threshold:
                    intersections += 1
        prob = intersections / (N * (N-1) / 2)
        print(f"{Colors.CYAN}Filter: P(intersection) = {prob:.4f}{Colors.RESET}")

        all_paths = np.vstack(paths)
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(all_paths)
        plt.figure(figsize=(8, 6))
        for i, path in enumerate(paths[:10]):
            reduced_path = pca.transform(path)
            plt.plot(reduced_path[:, 0], reduced_path[:, 1], alpha=0.7, label=f'History {i+1}')
        plt.title('PCA: Divergence of Histories')
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.legend()
        plt.savefig('data/filter.png')
        plt.show()
        print(f"{Colors.MAGENTA}PCA saved{Colors.RESET}")

    def set_f_will(self, value):
        self.F_will = max(0, min(1, value))
        print(f"{Colors.YELLOW}F_will set to {self.F_will:.2f} (will vs. chance){Colors.RESET}")

    def dashboard(self):
        total_weight = sum(d['weight_Ww'] for d in self.D_Map.values())
        bar_energy = "█" * int(self.energy // 5)
        bar_load = "█" * int(self.load // 5)
        bar_weight = "█" * min(int(total_weight // 5), 20)
        print(f"\n{Colors.BOLD}--- WORK DASHBOARD ---{Colors.RESET}")
        print(f"Energy:   [{Colors.GREEN}{bar_energy:<20}{Colors.RESET}] {self.energy}%")
        print(f"Load:     [{Colors.RED}{bar_load:<20}{Colors.RESET}] {self.load}%")
        print(f"Memory:   [{Colors.MAGENTA}{bar_weight:<20}{Colors.RESET}] {total_weight:.1f}")
        print(f"Status: {self.status} | Interactions: {len(self.H_log)} | F_will: {self.F_will:.2f}")

# --- RETRO TERMINAL INTERFACE ---
def retro_terminal_interface():
    core = AII()
    dots = ["", ".", "..", "...", "....", "....."]
    pulse = ["-", "\\", "|", "/"]

    print(f"{Colors.GREEN}{Colors.BOLD}═" * 68)
    print("   AII v3.9.0 – AI WITH EMOTIONS | IT FEELS, NOT JUST KNOWS")
    print("═" * 68 + Colors.RESET)

    try:
        while True:
            e_data = EMOTIONS.get(core.emotion, {"color": "", "icon": ""})
            status_color = {"thinking": Colors.GREEN, "sleeping": Colors.CYAN, "tired": Colors.RED}.get(core.status, Colors.YELLOW)
            prompt = input(f"\nPROMPT> [{status_color}{core.status}{Colors.RESET} | {e_data['color']}{e_data['icon']} {core.emotion}{Colors.RESET} | EN:{core.energy:3d}%] ")

            if prompt.lower() in ["exit", "quit", "q"]:
                core.running = False
                break

            # --- COMMANDS ---
            if prompt.startswith("!teach "):
                rest = prompt[7:].strip()
                if not rest:
                    print(f"{Colors.RED}Usage: !teach TAG CONTENT{Colors.RESET}")
                    continue
                parts = rest.split(" ", 1)
                tag, content = parts[0], parts[1] if len(parts) > 1 else parts[0]
                core.teach(tag, content)
                continue

            if prompt == "!coffee":
                core.coffee()
                continue

            if prompt == "!dashboard":
                core.dashboard()
                continue

            if prompt.startswith("!f_will "):
                try:
                    value = float(prompt.split()[1])
                    core.set_f_will(value)
                except:
                    print(f"{Colors.RED}Usage: !f_will 0.5 (0-1){Colors.RESET}")
                continue

            if prompt == "!trajectory":
                core.simulate_trajectory()
                continue

            if prompt == "!filter":
                core.ontological_filter()
                continue

            # --- THINKING ANIMATION ---
            for i in range(6):
                mode, load, energy = core.cycle()
                sys.stdout.write(f"\r{mode} | EN:{energy:3d}% LOAD:{load:3d}% {dots[i]} {pulse[i%4]}")
                sys.stdout.flush()
                time.sleep(0.15)

            response, emotion = core.generate_response(prompt)
            e_data = EMOTIONS.get(emotion, {"color": "", "icon": ""})
            print(f"\rRESPONSE ({e_data['color']}{e_data['icon']} {emotion}{Colors.RESET})> {response}")

    except KeyboardInterrupt:
        core.running = False
        print(f"\n{Colors.RED}--- AII SHUTDOWN – but emotions remain. ---{Colors.RESET}")

if __name__ == "__main__":
    retro_terminal_interface()