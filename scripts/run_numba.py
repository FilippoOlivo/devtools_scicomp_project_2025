from pyclassify.utils import distance_numpy
from pyclassify.utilsnumba import distance_numba, distance_numba_serial
import numpy as np
from time import time
import json


times = {
    'distance_numpy': [],
    'distance_numba': [],
    'distance_numba_serial': [],
    'lengths': []
}
for i in range(5):
    length = 1024 * 2**i
    print(length)
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
    times['lengths'].append(length)
    with open("data.json", "w") as f:
        json.dump(times, f, indent=4) 
    

