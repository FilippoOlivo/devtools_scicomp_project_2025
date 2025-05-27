from .utils import distance, majority_vote

class kNN:
    def __init__(self, k):
        if k < 1:
            raise RuntimeError("k must be positive!")
        if not isinstance(k, int):
            raise RuntimeError("k must be an int")
        self.k  = k

        self.predicted = None
    
    def _get_k_nearest_neighbors(self, X, y, x):
        distances = [distance(a, x) for a in X]
        sorted_idx = sorted(range(len(distances)), key=distances.__getitem__)
        sorted_idx = sorted_idx[:self.k]
        return [y[i] for i in sorted_idx]

    def __call__(self, data, new_points):
        X,y = data[0], data[1]
        nn = [self._get_k_nearest_neighbors(X,y,x) for x in new_points]
        self.predicted = [majority_vote(i) for i in nn]