# test_quantum_emotions.py

def test_basic_emotions():
    """Test podstawowych operacji"""
    
    # Utwórz stan
    state = QuantumEmotionalState()
    print("Initial state:", state)
    print(f"Entropy: {state.entropy():.2f} bits")
    
    # Ustaw konkretną emocję
    state.set_emotion('joy', magnitude=0.8, phase=0.0)
    state.set_emotion('fear', magnitude=0.3, phase=np.pi)  # Przeciwfaza!
    print("\nAfter setting joy & fear:", state)
    
    # Pomiar
    for i in range(5):
        measured = state.measure()
        print(f"Measurement {i+1}: {measured}")
    
    # Dominant emotion
    emotion, prob = state.dominant_emotion()
    print(f"\nDominant: {emotion} ({prob:.1%})")

if __name__ == "__main__":
    test_basic_emotions()