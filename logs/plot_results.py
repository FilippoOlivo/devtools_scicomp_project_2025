import json
from matplotlib import pyplot as plt
# Read JSON file
with open("logs/data.json", "r") as f:
    data = json.load(f)

plt.plot(data["lengths"][1:], data["distance_numpy"][1:])
plt.plot(data["lengths"][1:], data["distance_numba"][1:])
plt.plot(data["lengths"][1:], data["distance_numba_serial"][1:])
plt.xlabel("Length of array")
plt.ylabel("Time (seconds)")
plt.legend(["Numpy", "Numba", "Numba (serial)"])
plt.savefig("logs/scalability.png")


