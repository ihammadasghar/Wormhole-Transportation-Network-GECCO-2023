from pyeasyga import pyeasyga as pyga
import numpy as np
from Evaluation import udp
import random

data = np.load('database.npz')
origins = data['origins']
NUM_OF_SHIPS = 12
JUMP_LIMIT = data['jump_limit']
DESTINATION = data['destination']


def get_blackholes_with_destination(destination):
    sources = []
    for x in data['edges']:
        if x[1] == destination:
            sources.append(x[0]) 
    return sources

penultimate_blackholes = get_blackholes_with_destination(DESTINATION)

def get_blackholes_with_source(source):
    destinations = []
    for x in data['edges']:
        if x[0] == source:
            destinations.append(x[1]) 
    return destinations


def find_solution_for_ship(ship, mean_time):
    while(True):
        print(f"Started Attempt 1 for ship {ship}")
        origin_blackhole = random.choice(origins[ship])
        current_blackhole = origin_blackhole
        traveresed_blackholes = [origin_blackhole]
        jumps = 1
        is_in_time_window = True
        
        while(jumps < JUMP_LIMIT):
            next_blackhole_options = get_blackholes_with_source(current_blackhole)

            # If it is in time window try to get to destination ASAP
            if is_in_time_window:
                if DESTINATION in next_blackhole_options:
                    next_blackhole = DESTINATION
                else:
                    penultimate_found = False
                    for b in next_blackhole_options:
                        if b in penultimate_blackholes:
                            next_blackhole = b
                            penultimate_found = True
                            break
                    
                    if(not penultimate_found):
                        next_blackhole = (random.choice(next_blackhole_options))
            else:
                # Choose blackholes that help get closer to time window
                next_blackhole = (random.choice(next_blackhole_options))

            traveresed_blackholes.append(next_blackhole)
            current_blackhole = next_blackhole
            jumps += 1
            if(current_blackhole == data['destination']):
                print(f"Solution found for ship {ship} with {len(traveresed_blackholes)} jumps")
                return traveresed_blackholes
            
        print(f"Jumps Exceeded.")


def generate_gen_zero():
    solutions = [find_solution_for_ship(i) for i in range(NUM_OF_SHIPS)]
    gen_zero = udp.convert_to_chromosome(solutions)
    print(gen_zero)



def fitness():
    raise NotImplementedError

def cross_over(parent1, parent2):
    raise NotImplementedError

def selection(population):
    raise NotImplementedError

generate_gen_zero()