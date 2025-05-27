import os
import yaml

def distance(point1, point2):
    if len(point1) != len(point2):
        raise RuntimeError("Lenght of point must be the same")
    distance = 0
    for x1, x2 in zip(point1, point2):
        distance += (x1-x2)**2
    return distance

def majority_vote(neighbors):
    total_sum = sum(neighbors)
    return 1 if total_sum >= len(neighbors)/2 else 0

def read_config(file):
   filepath = os.path.abspath(f'{file}.yaml')
   with open(filepath, 'r') as stream:
      kwargs = yaml.safe_load(stream)
   return kwargs

    