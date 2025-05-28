from .utils import distance, majority_vote, distance_numpy
from .utilsnumba import distance_numba
import numpy as np
from line_profiler import profile

class kNN:
    def __init__(self, k, backhand='plain'):
        if k < 1:
            raise RuntimeError("k must be positive!")
        if not isinstance(k, int):
            raise RuntimeError("k must be an int")
    
        if backhand not in ['plain', 'numpy', 'numba']:
            raise ValueError(f"backhand='{backhand}' is not supported")
        if backhand == 'plain':
            self.distance = distance
        elif backhand == 'numpy':
            self.distance = distance_numpy
        elif backhand == 'numba':
            self.distance = distance_numba
        self.k  = k

        self.predicted = None
    
    @profile
    def _get_k_nearest_neighbors(self, X, y, x):
        distances = [self.distance(a, x) for a in X]
        sorted_idx = sorted(range(len(distances)), key=distances.__getitem__)
        sorted_idx = sorted_idx[:self.k]
        return [y[i] for i in sorted_idx]
    
    @profile
    def __call__(self, data, new_points):
        X,y = data[0], data[1]
        if self.distance != distance:
            X = np.array(X)
            new_points = np.array(new_points)
        nn = [self._get_k_nearest_neighbors(X,y,x) for x in new_points]
        self.predicted = [majority_vote(i) for i in nn]