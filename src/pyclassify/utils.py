import os
import yaml
import numpy as np
from numba.pycc import CC
from numba import njit, prange
from line_profiler import profile
cc = CC('utilsnumba')

@profile
def distance(point1, point2):
    if len(point1) != len(point2):
        raise RuntimeError("Lenght of point must be the same")
    distance = 0
    for x1, x2 in zip(point1, point2):
        distance += (x1-x2)**2
    return distance

@profile
def distance_numpy(point1, point2):
    if len(point1) != len(point2):
        raise RuntimeError("Lenght of point must be the same")
    return float(np.sum((point1 - point2)**2))

@profile
@cc.export('distance_numba', 'f8(f8[:], f8[:])')
@njit(parallel=True)
def distance_numba(point1, point2):
    distance = 0
    n = point1.shape[0]
    for ix in prange(n):
        distance += (point1[ix] - point2[ix])**2
    return distance

@profile
@cc.export('distance_numba_serial', 'f8(f8[:], f8[:])')
@njit(parallel=True)
def distance_numba_serial(point1, point2):
    diff = (point1 - point2) ** 2
    distance = np.sum(diff)
    return distance
 
@profile
def majority_vote(neighbors):
    total_sum = sum(neighbors)
    return 1 if total_sum >= len(neighbors)/2 else 0

def read_config(file):
   filepath = os.path.abspath(f'{file}.yaml')
   with open(filepath, 'r') as stream:
      kwargs = yaml.safe_load(stream)
   return kwargs

def read_file(filename):
    X = []
    y = []
    with open(filename) as f:
        for line in f:
            values = line.split(',')
            y_temp = values[-1]
            if y_temp.isdigit() and int(y_temp) in [0, 1]:
                y.append(int(y_temp))
            else:
                y.append(0 if y_temp[0] == 'b' else 1)
            X.append([float(i) for i in values[:-1]])
    return X, y

if __name__ == "__main__":
    cc.compile()