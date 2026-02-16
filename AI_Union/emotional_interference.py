#emotional_interference.py

class EmotionalInterference:
    """
    Modeluje jak emocje wpływają na siebie (interference)
    
    Konstruktywna: joy + hope → euforia
    Destruktywna: joy + fear → napięcie
    """
    
    def __init__(self):
        # Macierz interferencji (learned from experience)
        # interference[A][B] = jak silnie A wpływa na B
        self.interference_matrix = self._initialize_interference()
    
    def _initialize_interference(self) -> Dict[str, Dict[str, float]]:
        """
        Bazowa macierz interferencji (można uczyć!)
        
        Wartości [-1, 1]:
        +1 = konstruktywna (wzmacniają się)
        -1 = destruktywna (osłabiają się)
         0 = neutralna
        """
        dims = QuantumEmotionalState.DIMENSIONS
        
        # Start z defaults (later: learn from experience)
        interference = {dim: {d: 0.0 for d in dims} for dim in dims}
        
        # Przykładowe korelacje (customize!)
        positive_pairs = [
            ('joy', 'trust'), ('joy', 'anticipation'),
            ('trust', 'being'), ('logic', 'knowledge'),
            ('creation', 'anticipation'), ('space', 'time'),
        ]
        
        negative_pairs = [
            ('joy', 'sadness'), ('joy', 'fear'),
            ('trust', 'disgust'), ('logic', 'chaos'),
            ('being', 'chaos'), ('fear', 'trust'),
        ]
        
        for a, b in positive_pairs:
            interference[a][b] = 0.7
            interference[b][a] = 0.7
        
        for a, b in negative_pairs:
            interference[a][b] = -0.7
            interference[b][a] = -0.7
        
        return interference
    
    def apply_interference(self, state: QuantumEmotionalState, 
                          time_step: float = 0.1) -> QuantumEmotionalState:
        """
        Zastosuj interference - emocje wpływają na siebie
        
        Args:
            state: obecny stan emocjonalny
            time_step: jak długo trwa interference
        
        Returns:
            Nowy stan po interference
        """
        new_state = QuantumEmotionalState()
        
        for emotion in state.DIMENSIONS:
            # Obecna amplituda
            current_amp = state.amplitudes[emotion]
            
            # Wpływ INNYCH emocji na tę
            influence = 0j  # complex
            
            for other_emotion in state.DIMENSIONS:
                if other_emotion == emotion:
                    continue
                
                other_amp = state.amplitudes[other_emotion]
                coupling = self.interference_matrix[other_emotion][emotion]
                
                # Interference term
                influence += coupling * other_amp * time_step
            
            # Nowa amplituda = stara + wpływ
            new_state.amplitudes[emotion] = current_amp + influence
        
        new_state.normalize()
        return new_state
    
    def resonance_strength(self, state: QuantumEmotionalState) -> float:
        """
        Mierz jak "rezonujące" są emocje
        
        High resonance = emocje się wspierają (coherent)
        Low resonance = emocje w konflikcie (decoherent)
        """
        total_resonance = 0.0
        
        for em1 in state.DIMENSIONS:
            for em2 in state.DIMENSIONS:
                if em1 >= em2:  # Avoid double counting
                    continue
                
                amp1 = state.amplitudes[em1]
                amp2 = state.amplitudes[em2]
                coupling = self.interference_matrix[em1][em2]
                
                # Interference term (faza ma znaczenie!)
                interference = np.real(amp1 * np.conj(amp2)) * coupling
                total_resonance += interference
        
        return total_resonance


def test_interference():
    """Test interference patterns"""
    
    state = QuantumEmotionalState()
    
    # Set conflicting emotions
    state.set_emotion('joy', 0.7, phase=0.0)
    state.set_emotion('fear', 0.5, phase=np.pi)  # π difference!
    
    print("Initial state:", state)
    
    interference = EmotionalInterference()
    resonance = interference.resonance_strength(state)
    print(f"Resonance: {resonance:.3f}")
    
    # Evolve with interference
    print("\nEvolution over time:")
    for t in range(10):
        state = interference.apply_interference(state, time_step=0.1)
        print(f"t={t}: {state.dominant_emotion()}")

if __name__ == "__main__":
    test_interference()