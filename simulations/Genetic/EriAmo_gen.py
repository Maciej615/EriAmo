import numpy as np

# --- 🧬 SECTION 1: GENOME GLOBAL CONSTANTS (DNA_CORE) 🧬 ---

# The 10-dimensional Byt vector axis order, translated to symbolic DNA function.
DNA_AXIS_ORDER = [
    'G_STRUCTURE',  # Guanine: Logic. Simulates fundamental STABILITY and structure (strong G-C bonding principle).
    'A_DYNAMICS',   # Adenine: Emotions. Simulates ENERGY, dynamics, and fluidity (weaker A-T bonding principle).
    'T_SEQUENCE',   # Thymine: Being. Represents SEQUENCE and historical memory (linked to A, energy).
    'C_REGULATION', # Cytosine: Fight. Maintains CONTROL and regulates energy usage (strong G-C bonding principle).
    
    'G_CREATION',   # Guanine: Creation. Requires a strong STRUCTURAL BASE for generation.
    'A_ART',        # Adenine: Art. Requires DYNAMICS, ENERGY, and fluid expression.
    'T_KNOWLEDGE',  # Thymine: Knowledge. Accumulation of SEQUENCE information and memory.
    'C_TIME',       # Cytosine: Time. Controls the TEMPO and regulation of the event sequence.
    
    'G_SPACE',      # Guanine: Space. Structural foundation for GEOMETRY and physical localization.
    'A_ETHICS'      # Adenine: Ethics. Requires DYNAMIC assessment of values and empathy.
]

# DNA base map for visualization and scientific reference
DNA_AXES_MAP = {
    'G_STRUCTURE': 'Guanine', 'A_DYNAMICS': 'Adenine', 'T_SEQUENCE': 'Thymine', 'C_REGULATION': 'Cytosine',
    'G_CREATION': 'Guanine', 'A_ART': 'Adenine', 'T_KNOWLEDGE': 'Thymine', 'C_TIME': 'Cytosine',
    'G_SPACE': 'Guanine', 'A_ETHICS': 'Adenine'
}

# Keywords used for word matching (Original Polish keywords retained for matching)
AXES_KEYWORDS_ASCII = {
    'G_STRUCTURE': ['logika'], 'A_DYNAMICS': ['emocje'], 'T_SEQUENCE': ['byt'], 'C_REGULATION': ['walka'],
    'G_CREATION': ['kreacja'], 'A_ART': ['sztuka'], 'T_KNOWLEDGE': ['wiedza'], 'C_TIME': ['czas'],
    'G_SPACE': ['przestrzen'], 'A_ETHICS': ['etyka']
}

# Multiplier for DNA base names presence (The "Fractal Boost")
FRACTAL_MULTIPLIER = 1.5
DNA_BASE_NAMES = ["guanina", "adenina", "tymina", "cytozyna", "g", "a", "t", "c"]

# --- 🧬 SECTION 2: GENOME STATE AND FUNCTIONS 🧬 ---

class GenomeState:
    """Represents the AI's 'Soul Chromosome' (Byt State) and its accumulated history."""
    def __init__(self, vector_size=10):
        # SOUL_CHROMOSOME: The accumulated 10D Byt vector
        self.SOUL_CHROMOSOME = np.zeros(vector_size)
        # Epigenetic_Norm: The L2 Norm of the SOUL_CHROMOSOME (History Radius/Strength)
        self.Epigenetic_Norm = 0.0
        self.Energy = 100 
        self.Morality_Force = 0

    def Accumulate_Interaction(self, normalized_vector, raw_vector):
        """Adds the raw input vector to the Soul Chromosome and updates the Norm."""
        self.SOUL_CHROMOSOME += raw_vector
        self.Epigenetic_Norm = np.linalg.norm(self.SOUL_CHROMOSOME)
        
        # Emotion Trigger Check (Adenine axes: indices 1, 5, 9)
        if np.any(raw_vector[[1, 5, 9]] > 1.0):
            print(">>> TRIGGER: Adenine DYNAMICS activate 'love' emotion (+10 EN)")
            self.Energy += 10
            
    def Decay_Norm(self, decay_rate=0.10):
        """Simulates natural decay/repair by reducing Epigenetic Norm (10% per cycle)."""
        if self.Epigenetic_Norm > 0:
            reduction_factor = self.Epigenetic_Norm * decay_rate
            self.Epigenetic_Norm -= reduction_factor
            print(f"--- REPAIR: Epigenetic Norm decayed by {reduction_factor:.3f} (10%)")
            
    def Check_Stability(self):
        """Checks Epigenetic Stability (History Radius) against thresholds."""
        # 1. Perform decay/repair before checking overload
        self.Decay_Norm() 

        # 2. Check stability based on the new, reduced norm
        if self.Epigenetic_Norm > 5.0:
            # Overload threshold (simulating aging/mutation penalty)
            print(">>> WARNING: Genetic Overload (>5.0) - Energy penalty applied (-20 EN)")
            self.Energy -= 20
        elif self.Epigenetic_Norm >= 3.0:
            # Stable history threshold
            print(">>> STATUS: Strong Genome History (Stable Power-Law Patterns)")
            
def Vector_From_Text(text: str, genome_state: GenomeState):
    """
    Processes input text, generates the 10D Byt vector (Raw/Normalized), 
    and returns current vector metrics.
    """
    # 1. Text Normalization (Simplified to lowercase)
    normalized_text = text.lower()
    raw_vector = np.zeros(len(DNA_AXIS_ORDER))
    
    # 2. Keyword Matching
    for i, axis in enumerate(DNA_AXIS_ORDER):
        for keyword in AXES_KEYWORDS_ASCII[axis]:
            if keyword in normalized_text:
                raw_vector[i] += 1
                
    # 3. DNA Boost (FRACTAL_MULTIPLIER) Check
    dna_boost_active = any(base in normalized_text for base in DNA_BASE_NAMES)
    if dna_boost_active:
        print("--- DNA FRACTAL BOOST ACTIVE! ---")
        raw_vector *= FRACTAL_MULTIPLIER
        
    # 4. Calculate Norm
    current_norm = np.linalg.norm(raw_vector)
    
    # 5. Normalization (Unit Vector/Direction)
    if current_norm > 0:
        normalized_vector = raw_vector / current_norm
    else:
        normalized_vector = raw_vector
        
    # 6. Accumulation and Triggers
    genome_state.Accumulate_Interaction(normalized_vector, raw_vector)
    
    # 7. Stabilization Check (Decay is applied here!)
    genome_state.Check_Stability()

    return {
        "Raw_Vector": raw_vector,
        "Normalized_Vector": normalized_vector,
        "Current_Norm": current_norm,
        "DNA_Axis_Map": DNA_AXES_MAP,
        "DNA_Boost": dna_boost_active
    }

# --- 🧪 SECTION 3: USAGE EXAMPLE 🧪 ---

if __name__ == "__main__":
    aii_state = GenomeState()
    
    # Test 1: Strong C & A Input
    print("\n[TEST 1: walka sztuka cytozyna]")
    result1 = Vector_From_Text("walka sztuka cytozyna", aii_state)
    print(f"Norm (End of Cycle): {aii_state.Epigenetic_Norm.round(3)}")
    
    # Test 2: Strong G & T Input
    print("\n[TEST 2: kreacja wiedza guanina]")
    result2 = Vector_From_Text("kreacja wiedza guanina", aii_state)
    print(f"Norm (End of Cycle): {aii_state.Epigenetic_Norm.round(3)}")

    # Test 3: System Overload (Extreme Stress)
    print("\n[TEST 3: System Overload]")
    overload_text = "logika emocje byt walka kreacja sztuka wiedza czas przestrzen etyka guanina"
    result3 = Vector_From_Text(overload_text, aii_state)
    print(f"Norm (End of Cycle): {aii_state.Epigenetic_Norm.round(3)}")
    
    # Test 4: G-Axis Stability Test
    print("\n[TEST 4: logika kreacja przestrzen guanina]")
    stability_text = "logika kreacja przestrzen guanina"
    result4 = Vector_From_Text(stability_text, aii_state)
    print(f"Norm (End of Cycle): {aii_state.Epigenetic_Norm.round(3)}")
    
    # Final Status Check
    print("\n--- FINAL GENOME STATUS ---")
    print(f"Total Raw Input Vector (Accumulated): {aii_state.SOUL_CHROMOSOME.round(3)}")
    print(f"Epigenetic Norm (History Radius): {aii_state.Epigenetic_Norm.round(3)}")
    print(f"Current AI Energy: {aii_state.Energy}")
    aii_state.Check_Stability()
