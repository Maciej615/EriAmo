# v17/cortex.py
import numpy as np
from numba import njit

@njit
def cos(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

class CortexFilter:
    def __init__(self, soul):
        self.soul = soul.copy()

    def filter(self, vec, t=0.98):
        s = cos(vec, self.soul)
        if s > t:
            self.soul += vec * 0.1
            return False, f"[KOMPRESJA] {s:.3f}"
        return True, f"[ARCHIWIZACJA] {s:.3f}"
