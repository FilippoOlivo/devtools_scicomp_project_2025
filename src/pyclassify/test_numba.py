import numpy as np
from numba.pycc import CC

cc = CC('module')
@cc.export('distance_numba', 'f4(f4[:], f4[:])')
def distance_numba(point1, point2):
    if len(point1) != len(point2):
        raise RuntimeError("Lenght of point must be the same")
    return float(np.linalg.norm(point1 - point2))

point1 = np.random.rand(100)
point2 = np.random.rand(100)

cc.compile()
distance_numba(point1, point2)