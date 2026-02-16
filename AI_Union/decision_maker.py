# decision_maker.py

import numpy as np
from typing import List, Tuple
from quantum_emotions import QuantumEmotionalState
from emotional_interference import EmotionalInterference


class QuantumDecisionMaker:
    """
    Hybrid quantum-classical decision making
    
    Phase 1: Emotional amplification (quantum-like, fast)
    Phase 2: Logical verification (classical, precise)
    """
    
    def __init__(self, 
                 emotional_state: QuantumEmotionalState,
                 interference: EmotionalInterference):
        self.emotional_state = emotional_state
        self.interference = interference
        
    def generate_options(self, situation: dict) -> List[dict]:
        """Generate possible actions/responses"""
        return [
            {'action': 'ignore', 'emotional_cost': {'anger': 0.3, 'sadness': 0.2}},
            {'action': 'defend', 'emotional_cost': {'anger': 0.7, 'fear': 0.3}},
            {'action': 'reflect', 'emotional_cost': {'sadness': 0.4, 'logic': 0.6}},
            {'action': 'thank', 'emotional_cost': {'trust': 0.5, 'joy': 0.3}},
        ]
    
    def emotional_resonance(self, option: dict) -> float:
        """Jak opcja rezonuje z obecnym stanem emocjonalnym?"""
        simulated_state = QuantumEmotionalState()
        
        for emotion, weight in option['emotional_cost'].items():
            if emotion in simulated_state.DIMENSIONS:
                current = self.emotional_state.amplitudes[emotion]
                simulated_state.amplitudes[emotion] = current + weight * 0.5
        
        simulated_state.normalize()
        resonance = self.interference.resonance_strength(simulated_state)
        return resonance
    
    def amplify_good_options(self, options: List[dict], 
                            iterations: int = None) -> List[Tuple[dict, float]]:
        """Grover-style amplitude amplification"""
        if iterations is None:
            iterations = int(np.sqrt(len(options)))
        
        amplitudes = {i: 1.0/np.sqrt(len(options)) 
                     for i in range(len(options))}
        
        for _ in range(iterations):
            resonances = {i: self.emotional_resonance(opt) 
                         for i, opt in enumerate(options)}
            mean_resonance = np.mean(list(resonances.values()))
            
            for i in range(len(options)):
                if resonances[i] > mean_resonance:
                    amplitudes[i] *= -1
                mean_amp = np.mean(list(amplitudes.values()))
                amplitudes[i] = 2 * mean_amp - amplitudes[i]
        
        total = sum(abs(a)**2 for a in amplitudes.values())
        if total < 1e-10:
            total = 1.0
        probabilities = {i: abs(amplitudes[i])**2 / total 
                        for i in range(len(options))}
        
        ranked = sorted(
            [(options[i], probabilities[i]) for i in range(len(options))],
            key=lambda x: x[1],
            reverse=True
        )
        
        return ranked
    
    def decide(self, situation: dict, verify: bool = True) -> dict:
        """Make decision: emotional narrowing + optional logical verification"""
        options = self.generate_options(situation)
        ranked_options = self.amplify_good_options(options)
        candidates = ranked_options[:3]
        
        if verify:
            final = self._logical_verification(candidates)
        else:
            final = candidates[0]
        
        return {
            'action': final[0]['action'],
            'confidence': final[1],
            'reasoning': 'hybrid_quantum_classical',
            'alternatives': candidates,
        }
    
    def _logical_verification(self, candidates: List[Tuple[dict, float]]) -> Tuple[dict, float]:
        """Classical verification step (placeholder for conscience)"""
        return candidates[0]