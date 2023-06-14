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

def get_wormholes_with_source(source):
    wormholes = []
    
    for i in range(len(data['edges'])):
        print(i+1,"/",len(data['edges']))
        if data['edges'][i][0] == source:
            wormholes.append(i) 
    return wormholes


def find_solution_for_ship(ship, mean_time=None):
    while(True):
        print(f"Started Attempt 1 for ship {ship} for goal mean time {mean_time}")
        origin_blackhole = random.choice(origins[ship])
        current_blackhole = origin_blackhole
        traveresed_blackholes = [origin_blackhole]
        jumps = 1
        time = data['delays'][ship]
        uncertainity = 0
        ended = False
        
        while(jumps < JUMP_LIMIT and not ended):
            print("searching wormholes...")
            wormhole_option = get_wormholes_with_source(current_blackhole)
            print("Found worm hole options\nSearching Black holes")
            next_blackhole_options = [data['edges'][i][1] for i in wormhole_option]
            chosen_wormhole = None
            next_blackhole = None

            print("Found blackhole options")

            if DESTINATION in next_blackhole_options:
                chosen_wormhole = wormhole_option[next_blackhole_options.index(DESTINATION)]
                chosen_wormhole_mean = data['meanvar'][chosen_wormhole][0]

                if (not mean_time) or (mean_time and abs(time+chosen_wormhole_mean-mean_time) <= 0.5):
                    next_blackhole = DESTINATION
                    ended = True
                
                print("Checked if going to destination available")
            
            if not ended:
                penultimate_found = False
                for b in next_blackhole_options.copy():
                    if b in penultimate_blackholes:
                        chosen_wormhole = wormhole_option[next_blackhole_options.index(b)]
                        chosen_wormhole_mean = data['meanvar'][chosen_wormhole][0]

                        if (not mean_time) or (mean_time and abs(time+chosen_wormhole_mean-mean_time) <= 0.5):
                            next_blackhole = b
                            penultimate_found = True
                            break

                    next_blackhole_options.remove(b)
                
                print("Checked if going to penultimate node available")

                if(not penultimate_found):
                    for b in next_blackhole_options:
                        if b in penultimate_blackholes:
                            chosen_wormhole = wormhole_option[next_blackhole_options.index(b)]
                            chosen_wormhole_mean = data['meanvar'][chosen_wormhole][0]

                            if (not mean_time) or (mean_time and abs(time+chosen_wormhole_mean-mean_time) <= 0.5):
                                next_blackhole = b
                                break
                    
                    print("Checked if going to rest nodes in time limit available")

                if not next_blackhole:
                    next_blackhole = random.choice(next_blackhole_options)            

            time += data['meanvar'][chosen_wormhole][0]
            uncertainity += data['meanvar'][chosen_wormhole][1]

            traveresed_blackholes.append(next_blackhole)
            current_blackhole = next_blackhole

            print("Jump ", jumps, "| next black hole: ", next_blackhole, "| time: ", time, "| Uncertainity: ", uncertainity)
            jumps += 1
            if(current_blackhole == data['destination']):
                print(f"Solution found for ship {ship} with {len(traveresed_blackholes)} jumps")
                if not mean_time:
                    return traveresed_blackholes, time
                return traveresed_blackholes
            
        print(f"Jumps Exceeded.")


def generate_gen_zero():
    solution1, mean_time = find_solution_for_ship(0)
    solutions = [solution1] + [find_solution_for_ship(i, mean_time) for i in range(1, NUM_OF_SHIPS)]
    gen_zero = udp.convert_to_chromosome(solutions)
    print(gen_zero)



def fitness():
    raise NotImplementedError

def cross_over(parent1, parent2):
    raise NotImplementedError

def selection(population):
    raise NotImplementedError

generate_gen_zero()