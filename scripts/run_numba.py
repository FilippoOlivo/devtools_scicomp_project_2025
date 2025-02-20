from pyclassify.utils import distance_numpy
from pyclassify.utilsnumba import distance_numba, distance_numba_serial
import numpy as np
from time import time


times = {
    'distance_numpy': [],
    'distance_numba': [],
    'distance_numba_serial': []
}
lengths = [] 
for i in range(20):
    length = 1024 * 2**i
    point1 = np.random.rand(length)
    point2 = np.random.rand(length)
    start = time()
    distance_numba(point1, point2)
    times['distance_numba'].append(time() - start)
    start = time()
    distance_numba_serial(point1, point2)
    times['distance_numba_serial'].append(time() - start)
    start = time()
    distance_numpy(point1, point2)
    times['distance_numpy'].append(time() - start)
    lengths.append(length)
    
print(lengths)
print(times)