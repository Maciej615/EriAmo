# eriamo/visualizations.py

import matplotlib.pyplot as plt
import numpy as np

def plot_emotional_state(state: QuantumEmotionalState, title="Emotional State"):
    """Wykres stanu emocjonalnego"""
    probs = state.get_probabilities()
    
    emotions = list(probs.keys())
    probabilities = list(probs.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(emotions, probabilities)
    plt.xlabel('Emotion')
    plt.ylabel('Probability')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_bloch_sphere_2d(joy_amp: complex, fear_amp: complex):
    """
    2D projekcja sfery Blocha (joy vs fear)
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', alpha=0.3)
    
    # Joy vector
    joy_x = np.real(joy_amp)
    joy_y = np.imag(joy_amp)
    ax.arrow(0, 0, joy_x, joy_y, color='gold', width=0.02, 
             label=f'Joy: {abs(joy_amp):.2f}∠{np.degrees(np.angle(joy_amp)):.0f}°')
    
    # Fear vector
    fear_x = np.real(fear_amp)
    fear_y = np.imag(fear_amp)
    ax.arrow(0, 0, fear_x, fear_y, color='purple', width=0.02,
             label=f'Fear: {abs(fear_amp):.2f}∠{np.degrees(np.angle(fear_amp)):.0f}°')
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Emotional Amplitudes (Complex Plane)')
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    
    plt.show()