import numpy as np
from GeneticAlgorithm import get_wormholes

def showData(data):
    print("Jump Limit: ", data["jump_limit"])
    print("Destination Blackhole: ", data["destination"])
    for k in data.keys():
        print("key: ", k, " | Type: ", type(data[k]), " | Length: ", data[k].size)

data = np.load('database.npz')

showData(data)

print("number of connections to destination: ", len(get_wormholes(105)))