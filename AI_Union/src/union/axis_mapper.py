# -*- coding: utf-8 -*-
"""
axis_mapper.py v1.0.0-Phase2
EriAmo Union - Axis Mapping System

Maps between:
- Language: 8 emotions (Plutchik model)
- Music: 9 ontological dimensions

Author: Claude & Maciej
Date: December 19, 2025
"""

import numpy as np
from typing import Dict, Tuple, List


class AxisMapper:
    """
    Maps emotional vectors (Language) to ontological dimensions (Music).
    
    Architecture:
    - Language: 8 emotions (ephemeral, change quickly)
    - Music: 9 axes (mixed ephemeral + persistent)
    
    Mapping strategy:
    - Emotions → ephemeral axes (direct, strong)
    - Emotions → persistent axes (indirect, accumulative)
    - Persistent → emotions (modulation, feedback)
    """
    
    # Language axes (from aii.py)
    LANG_AXES = [
        'radość', 'smutek', 'strach', 'gniew',
        'miłość', 'wstręt', 'zaskoczenie', 'akceptacja'
    ]
    
    # Music axes (from amocore_v58.py)
    MUSIC_AXES = [
        'logika', 'emocje', 'affections', 'wiedza',
        'czas', 'kreacja', 'byt', 'przestrzen', 'etyka'
    ]
    
    # Ephemeral (decay over time)
    MUSIC_EPHEMERAL = ['emocje', 'czas']
    
    # Persistent (build over time)
    MUSIC_PERSISTENT = ['logika', 'affections', 'wiedza', 'kreacja', 'byt', 'przestrzen', 'etyka']
    
    def __init__(self, verbose: bool = False):
        """
        Initialize mapping matrices.
        
        Args:
            verbose: Print debug information
        """
        self.verbose = verbose
        
        # Build mapping matrices
        self.E2E_matrix = self._build_emotion_to_ephemeral()
        self.E2P_matrix = self._build_emotion_to_persistent()
        self.P2E_matrix = self._build_persistent_to_emotion()
        
        if self.verbose:
            print(f"[AxisMapper] Initialized")
            print(f"  E→E matrix: {self.E2E_matrix.shape}")
            print(f"  E→P matrix: {self.E2P_matrix.shape}")
            print(f"  P→E matrix: {self.P2E_matrix.shape}")
    
    def _build_emotion_to_ephemeral(self) -> np.ndarray:
        """
        How emotions affect ephemeral axes (emocje, czas).
        
        Returns:
            8×2 matrix (emotions → [emocje, czas])
        
        Logic:
        - All emotions → 'emocje' (direct mapping)
        - High arousal emotions → 'czas' faster
        - Low arousal emotions → 'czas' slower
        """
        matrix = np.zeros((8, 2))
        
        # Column 0: emocje (direct emotional magnitude)
        # All emotions feed into 'emocje' axis
        matrix[:, 0] = 1.0
        
        # Column 1: czas (time perception)
        # High arousal → faster subjective time
        matrix[0, 1] = 0.8   # radość (joy) → time flies
        matrix[1, 1] = -0.6  # smutek (sadness) → time drags
        matrix[2, 1] = 0.9   # strach (fear) → heightened awareness
        matrix[3, 1] = 0.9   # gniew (anger) → urgency
        matrix[4, 1] = 0.5   # miłość (love) → timeless
        matrix[5, 1] = -0.4  # wstręt (disgust) → avoidance
        matrix[6, 1] = 0.7   # zaskoczenie (surprise) → attention
        matrix[7, 1] = -0.3  # akceptacja (acceptance) → present
        
        return matrix
    
    def _build_emotion_to_persistent(self) -> np.ndarray:
        """
        How emotions influence persistent axes (accumulative).
        
        Returns:
            8×7 matrix (emotions → persistent axes)
        
        Persistent: logika, affections, wiedza, kreacja, byt, przestrzen, etyka
        """
        matrix = np.zeros((8, 7))
        
        # Column 0: logika (rationality)
        matrix[0, 0] = 0.3   # radość → clear thinking
        matrix[1, 0] = -0.3  # smutek → clouded
        matrix[2, 0] = 0.6   # strach → defensive reasoning
        matrix[3, 0] = -0.5  # gniew → impaired logic
        matrix[4, 0] = 0.2   # miłość → biased but motivated
        matrix[5, 0] = 0.4   # wstręt → critical thinking
        matrix[6, 0] = 0.5   # zaskoczenie → attention boost
        matrix[7, 0] = 0.7   # akceptacja → rational acceptance
        
        # Column 1: affections (deep emotional memory)
        matrix[0, 1] = 0.6   # radość → positive imprint
        matrix[1, 1] = 0.9   # smutek → strong memory
        matrix[2, 1] = 0.7   # strach → trauma imprint
        matrix[3, 1] = 0.6   # gniew → grudge formation
        matrix[4, 1] = 0.9   # miłość → deep bonding
        matrix[5, 1] = 0.7   # wstręt → avoidance learning
        matrix[6, 1] = 0.4   # zaskoczenie → memorable
        matrix[7, 1] = 0.5   # akceptacja → integration
        
        # Column 2: wiedza (accumulated knowledge)
        matrix[0, 2] = 0.4   # radość → openness to learning
        matrix[1, 2] = 0.2   # smutek → introspection
        matrix[2, 2] = 0.3   # strach → threat detection
        matrix[3, 2] = -0.2  # gniew → tunnel vision
        matrix[4, 2] = 0.3   # miłość → understanding
        matrix[5, 2] = 0.4   # wstręt → discrimination
        matrix[6, 2] = 0.6   # zaskoczenie → learning opportunity
        matrix[7, 2] = 0.5   # akceptacja → wisdom
        
        # Column 3: kreacja (creative potential)
        matrix[0, 3] = 0.9   # radość → high creativity
        matrix[1, 3] = 0.4   # smutek → melancholic art
        matrix[2, 3] = 0.2   # strach → conservative
        matrix[3, 3] = 0.5   # gniew → aggressive expression
        matrix[4, 3] = 0.8   # miłość → inspired creation
        matrix[5, 3] = 0.1   # wstręt → critical
        matrix[6, 3] = 0.7   # zaskoczenie → novel ideas
        matrix[7, 3] = 0.3   # akceptacja → balanced
        
        # Column 4: byt (existence/identity)
        # All emotions contribute to sense of being
        matrix[:, 4] = 0.2
        matrix[4, 4] = 0.4   # miłość → stronger sense of self
        matrix[7, 4] = 0.5   # akceptacja → integrated identity
        
        # Column 5: przestrzen (spatial awareness)
        matrix[0, 5] = 0.3   # radość → expansive
        matrix[1, 5] = -0.3  # smutek → withdrawn
        matrix[2, 5] = 0.7   # strach → hypervigilant
        matrix[3, 5] = 0.5   # gniew → territorial
        matrix[4, 5] = 0.4   # miłość → inclusive
        matrix[5, 5] = -0.2  # wstręt → avoidant
        matrix[6, 5] = 0.6   # zaskoczenie → alert
        matrix[7, 5] = 0.3   # akceptacja → comfortable
        
        # Column 6: etyka (ethical sense)
        matrix[0, 6] = 0.2   # radość → generous
        matrix[1, 6] = 0.1   # smutek → empathetic
        matrix[2, 6] = -0.2  # strach → self-preservation
        matrix[3, 6] = -0.4  # gniew → justice (but harsh)
        matrix[4, 6] = 0.6   # miłość → compassionate
        matrix[5, 6] = 0.3   # wstręt → moral judgment
        matrix[6, 6] = 0.1   # zaskoczenie → questioning
        matrix[7, 6] = 0.5   # akceptacja → tolerant
        
        return matrix
    
    def _build_persistent_to_emotion(self) -> np.ndarray:
        """
        How persistent axes modulate emotional expression (feedback).
        
        Returns:
            7×8 matrix (persistent → emotions)
        
        This creates feedback loops where accumulated wisdom
        influences how we feel emotions.
        """
        matrix = np.zeros((7, 8))
        
        # Row 0: logika modulates emotions (generally dampens)
        matrix[0, :] = -0.2
        matrix[0, 7] = 0.3  # logika → akceptacja (rational acceptance)
        
        # Row 1: affections amplifies related emotions
        matrix[1, 0] = 0.3  # affections → radość (positive memories)
        matrix[1, 1] = 0.4  # affections → smutek (nostalgia)
        matrix[1, 4] = 0.5  # affections → miłość (deep feelings)
        
        # Row 2: wiedza provides context
        matrix[2, 2] = -0.2  # wiedza → strach (knowledge reduces fear)
        matrix[2, 7] = 0.4  # wiedza → akceptacja (understanding)
        
        # Row 3: kreacja enhances positive emotions
        matrix[3, 0] = 0.5  # kreacja → radość (joy of creation)
        matrix[3, 4] = 0.3  # kreacja → miłość (passion)
        matrix[3, 6] = 0.4  # kreacja → zaskoczenie (novelty)
        
        # Row 4: byt (stability dampens volatility)
        matrix[4, :] = -0.1
        matrix[4, 7] = 0.3  # byt → akceptacja (self-acceptance)
        
        # Row 5: przestrzen affects fear/comfort
        matrix[5, 2] = -0.3  # przestrzen → strach (comfort reduces fear)
        matrix[5, 7] = 0.3  # przestrzen → akceptacja (at home)
        
        # Row 6: etyka influences moral emotions
        matrix[6, 4] = 0.3  # etyka → miłość (compassion)
        matrix[6, 5] = 0.4  # etyka → wstręt (moral disgust)
        matrix[6, 7] = 0.4  # etyka → akceptacja (tolerance)
        
        return matrix
    
    # =========================================================================
    # MAPPING FUNCTIONS
    # =========================================================================
    
    def map_emotions_to_music(
        self,
        emotion_vector: np.ndarray,
        strength: float = 0.1
    ) -> Dict[str, float]:
        """
        Convert Language emotional state to Music ontological state.
        
        Args:
            emotion_vector: [8] array of emotion values (Language)
            strength: Mapping strength multiplier (0.0-1.0)
        
        Returns:
            dict: Updates for 9 music axes
        """
        if len(emotion_vector) != 8:
            raise ValueError(f"Expected 8 emotions, got {len(emotion_vector)}")
        
        # Calculate ephemeral updates (direct, strong)
        ephemeral_values = emotion_vector @ self.E2E_matrix
        
        # Calculate persistent updates (indirect, accumulative)
        persistent_values = emotion_vector @ self.E2P_matrix
        
        # Apply strength multiplier
        ephemeral_values *= strength
        persistent_values *= strength * 0.5  # Persistent build slower
        
        # Build result dict
        result = {}
        
        # Ephemeral axes
        result['emocje'] = float(ephemeral_values[0])
        result['czas'] = float(ephemeral_values[1])
        
        # Persistent axes
        result['logika'] = float(persistent_values[0])
        result['affections'] = float(persistent_values[1])
        result['wiedza'] = float(persistent_values[2])
        result['kreacja'] = float(persistent_values[3])
        result['byt'] = float(persistent_values[4])
        result['przestrzen'] = float(persistent_values[5])
        result['etyka'] = float(persistent_values[6])
        
        if self.verbose:
            print(f"[Map E→M] Strongest: {max(result.items(), key=lambda x: abs(x[1]))}")
        
        return result
    
    def map_music_to_emotions(
        self,
        music_state: Dict[str, float],
        strength: float = 0.1
    ) -> np.ndarray:
        """
        Convert Music ontological state to Language emotional modulation.
        
        Args:
            music_state: dict with 9 music axes
            strength: Mapping strength multiplier (0.0-1.0)
        
        Returns:
            [8] array: Emotional modulation vector
        """
        # Extract persistent values (only these affect emotions)
        persistent_array = np.array([
            music_state.get('logika', 0.0),
            music_state.get('affections', 0.0),
            music_state.get('wiedza', 0.0),
            music_state.get('kreacja', 0.0),
            music_state.get('byt', 0.0),
            music_state.get('przestrzen', 0.0),
            music_state.get('etyka', 0.0)
        ])
        
        # Calculate emotional modulation
        emotion_modulation = persistent_array @ self.P2E_matrix
        
        # Extract base emotion from 'emocje' axis
        base_emotion_level = music_state.get('emocje', 0.0)
        
        # Distribute base emotion across all emotions (diffuse influence)
        base_distribution = np.ones(8) * base_emotion_level * 0.1
        
        # Combine base + modulation
        result = base_distribution + emotion_modulation * strength
        
        if self.verbose:
            dominant_idx = np.argmax(np.abs(result))
            print(f"[Map M→E] Strongest: {self.LANG_AXES[dominant_idx]}")
        
        return result
    
    # =========================================================================
    # ANALYSIS & UTILITIES
    # =========================================================================
    
    def analyze_mapping(
        self,
        emotion_vector: np.ndarray
    ) -> Dict[str, any]:
        """
        Detailed analysis of how emotions map to music.
        
        Returns diagnostic information about the mapping.
        """
        music_updates = self.map_emotions_to_music(emotion_vector, strength=1.0)
        
        # Find dominant emotion
        emotion_idx = np.argmax(np.abs(emotion_vector))
        dominant_emotion = self.LANG_AXES[emotion_idx]
        emotion_strength = emotion_vector[emotion_idx]
        
        # Find most affected music axes
        sorted_music = sorted(
            music_updates.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        return {
            'dominant_emotion': dominant_emotion,
            'emotion_strength': float(emotion_strength),
            'top_affected_axes': sorted_music[:3],
            'ephemeral_total': abs(music_updates['emocje']) + abs(music_updates['czas']),
            'persistent_total': sum(abs(v) for k, v in music_updates.items() if k not in ['emocje', 'czas'])
        }
    
    def get_mapping_summary(self) -> str:
        """
        Human-readable summary of mapping configuration.
        """
        summary = []
        summary.append("="*70)
        summary.append("  🗺️  Axis Mapping Configuration")
        summary.append("="*70)
        
        summary.append("\n📝 Language Emotions (8):")
        for i, emotion in enumerate(self.LANG_AXES):
            summary.append(f"  {i}: {emotion}")
        
        summary.append("\n🎵 Music Ontological Axes (9):")
        summary.append("  Ephemeral (decay):")
        for axis in self.MUSIC_EPHEMERAL:
            summary.append(f"    • {axis}")
        summary.append("  Persistent (accumulate):")
        for axis in self.MUSIC_PERSISTENT:
            summary.append(f"    • {axis}")
        
        summary.append("\n🔄 Mapping Matrices:")
        summary.append(f"  E→E (Emotion→Ephemeral): {self.E2E_matrix.shape}")
        summary.append(f"  E→P (Emotion→Persistent): {self.E2P_matrix.shape}")
        summary.append(f"  P→E (Persistent→Emotion): {self.P2E_matrix.shape}")
        
        summary.append("="*70)
        
        return "\n".join(summary)


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

def test_axis_mapper():
    """Quick test of AxisMapper functionality."""
    print("\n🧪 Testing AxisMapper\n")
    
    mapper = AxisMapper(verbose=True)
    
    # Test 1: High joy (radość)
    print("\n[Test 1] High radość (joy):")
    emotions = np.array([0.9, 0, 0, 0, 0, 0, 0, 0])
    music_updates = mapper.map_emotions_to_music(emotions)
    
    print(f"  emocje: {music_updates['emocje']:.3f}")
    print(f"  czas: {music_updates['czas']:.3f}")
    print(f"  kreacja: {music_updates['kreacja']:.3f}")
    
    assert music_updates['emocje'] > 0.05, "Joy should increase emocje"
    assert music_updates['kreacja'] > 0.03, "Joy should boost kreacja"
    print("  ✅ Joy mapping correct")
    
    # Test 2: High sadness (smutek)
    print("\n[Test 2] High smutek (sadness):")
    emotions = np.array([0, 0.8, 0, 0, 0, 0, 0, 0])
    music_updates = mapper.map_emotions_to_music(emotions)
    
    print(f"  affections: {music_updates['affections']:.3f}")
    print(f"  czas: {music_updates['czas']:.3f}")
    
    assert music_updates['affections'] > 0.03, "Sadness creates deep affections"
    assert music_updates['czas'] < 0, "Sadness slows time"
    print("  ✅ Sadness mapping correct")
    
    # Test 3: Reverse mapping
    print("\n[Test 3] Music → Emotion (reverse):")
    music_state = {
        'logika': 0.0,
        'emocje': 0.5,
        'affections': 0.8,
        'wiedza': 0.0,
        'czas': 0.0,
        'kreacja': 0.6,
        'byt': 0.5,
        'przestrzen': 0.0,
        'etyka': 0.0
    }
    
    emotion_mods = mapper.map_music_to_emotions(music_state)
    print(f"  Emotions modulated: {emotion_mods}")
    
    # Should enhance positive emotions (kreacja + affections)
    assert emotion_mods[0] > 0, "Kreacja should enhance joy"
    print("  ✅ Reverse mapping works")
    
    # Test 4: Analysis
    print("\n[Test 4] Mapping analysis:")
    analysis = mapper.analyze_mapping(np.array([0.7, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.3]))
    
    print(f"  Dominant: {analysis['dominant_emotion']}")
    print(f"  Top affected: {analysis['top_affected_axes'][:2]}")
    
    print("\n✅ All AxisMapper tests passed!\n")
    
    return mapper


if __name__ == "__main__":
    mapper = test_axis_mapper()
    print(mapper.get_mapping_summary())
