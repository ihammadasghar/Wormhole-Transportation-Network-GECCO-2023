from pyeasyga import pyeasyga as pyga
import numpy as np
from Evaluation import udp
import random
from BlackholeNetworkTree import BlackholeNetworkTree

data = np.load('database.npz')
origins = data['origins']
NUM_OF_SHIPS = 12
JUMP_LIMIT = data['jump_limit']
DESTINATION = data['destination']
means = list(data['meanvar'][:,0])
variances = list(data['meanvar'][:,1])
edges = list(data['edges'])
networkTree = BlackholeNetworkTree(edges, means, variances, 10000)


def get_blackholes_with_destination(destination):
    sources = {x[0] for x in data['edges'] if x[1] == destination}
    return sources


penultimate_blackholes = get_blackholes_with_destination(DESTINATION)


def find_solution_for_ship(ship, mean_time):
    attempt = 0
    while(True):
        attempt += 1
        origin_blackhole = random.choice(origins[ship])
        current_blackhole = networkTree.blackholes[origin_blackhole]
        traveresed_blackholes = [networkTree.blackholes[origin_blackhole]]
        jumps = 1
        time = data['delays'][ship]
        uncertainity = 0
        is_current_blackhole_penultimate = False
        
        while(jumps < JUMP_LIMIT):
            chosen_wormhole = None
            next_blackhole = None

            if is_current_blackhole_penultimate:
                for w in current_blackhole.wormholes:
                  if w.destination.id == DESTINATION:
                    chosen_wormhole = w
                    break

                if abs(time+chosen_wormhole.time_offset-mean_time) <= 0.5:
                    time += chosen_wormhole.time_offset
                    uncertainity += chosen_wormhole.uncertainity

                    traveresed_blackholes.append(DESTINATION)
                    print(f"Solution found: Ship {ship} | Jumps: {jumps} | Attempts: {attempt} | Time Offset: {time} | Uncertainity: {uncertainity}")
                    return traveresed_blackholes
            
            # Try to end journey if mean time in reach
            if abs(time-mean_time) <= 0.5:
                for w in current_blackhole.wormholes:
                    if w.destination.id in penultimate_blackholes:
                        if abs(time+w.time_offset-mean_time) <= 0.5:
                            chosen_wormhole = w
                            next_blackhole = w.destination
                            is_current_blackhole_penultimate = True
                            break

            if not next_blackhole:
                if time < mean_time:
                    chosen_wormhole = random.choice(current_blackhole.wormholes)
                    while chosen_wormhole.time_offset < 0:
                        chosen_wormhole = random.choice(current_blackhole.wormholes)
                    
                else:
                    chosen_wormhole = random.choice(current_blackhole.wormholes)
                    while chosen_wormhole.time_offset > 0:
                        chosen_wormhole = random.choice(current_blackhole.wormholes)

                next_blackhole = chosen_wormhole.destination

            time += chosen_wormhole.time_offset
            uncertainity += chosen_wormhole.uncertainity

            traveresed_blackholes.append(next_blackhole.id)
            current_blackhole = next_blackhole

            jumps += 1


def generate_gen_zero():
    mean_delay_time = sum(data['delays'])/len(data['delays'])
    solutions = [find_solution_for_ship(i, mean_delay_time) for i in range(NUM_OF_SHIPS)]

    np.save('genzero', solutions)



def fitness():
    raise NotImplementedError

def cross_over(parent1, parent2):
    raise NotImplementedError

def selection(population):
    raise NotImplementedError

generate_gen_zero()