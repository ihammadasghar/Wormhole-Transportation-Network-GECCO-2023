from pyeasyga import pyeasyga as pyga
import numpy as np
from Evaluation import udp
import random
import csv

data = np.load('database.npz')
origins = data['origins']
NUM_OF_SHIPS = 12
JUMP_LIMIT = data['jump_limit']
DESTINATION = data['destination']
means = list(data['meanvar'][:,0])
variances = list(data['meanvar'][:,1])


def get_blackholes_with_destination(destination):
    sources = []
    for x in data['edges']:
        if x[1] == destination:
            sources.append(x[0]) 
    return sources

penultimate_blackholes = get_blackholes_with_destination(DESTINATION)

def get_wormholes_with_source(source):
    wormholes = []
    i = 0
    for edge in data['edges']:
        if edge[0] == source:
            wormholes.append((i, edge[1]))
        i +=1
    return np.array(wormholes)


def get_means_by_wormholes(wormholes):
    return [means[w] for w in wormholes]


def find_solution_for_ship(ship, mean_time=None):
    while(True):
        print(f"\nStarted Attempt 1 for ship {ship} for goal mean time {mean_time}")
        origin_blackhole = random.choice(origins[ship])
        current_blackhole = origin_blackhole
        traveresed_blackholes = [origin_blackhole]
        jumps = 1
        time = data['delays'][ship]
        uncertainity = 0
        ended = False
        
        while(jumps < JUMP_LIMIT and not ended):
            wormhole_option = get_wormholes_with_source(current_blackhole)
            next_blackhole_options = list(wormhole_option[:,1])
            wormhole_option = wormhole_option[:,0]
            chosen_wormhole = None
            next_blackhole = None

            if DESTINATION in next_blackhole_options:
                chosen_wormhole = wormhole_option[next_blackhole_options.index(DESTINATION)]
                chosen_wormhole_mean = means[chosen_wormhole]

                if (not mean_time) or (mean_time and abs(time+chosen_wormhole_mean-mean_time) <= 0.5):
                    next_blackhole = DESTINATION
                    ended = True
                    print("Destination reached")
                
            
            if not ended:
                for b in next_blackhole_options.copy():
                    if b in penultimate_blackholes:
                        chosen_wormhole = wormhole_option[next_blackhole_options.index(b)]
                        chosen_wormhole_mean = means[chosen_wormhole]

                        if (not mean_time) or (mean_time and abs(time+chosen_wormhole_mean-mean_time) <= 0.5):
                            next_blackhole = b
                            print("Penultimate node found")
                            break
                    

                if not next_blackhole:
                    wormhole_means = get_means_by_wormholes(wormhole_option)
                    
                    if time < mean_time:
                        index_max = np.argmax(wormhole_means)
                        next_blackhole = next_blackhole_options[index_max]
                        chosen_wormhole = wormhole_option[next_blackhole_options.index(next_blackhole)]
                        print("random node chosen to adjust time")
                             
                    else:
                        index_min = np.argmin(wormhole_means)
                        next_blackhole = next_blackhole_options[index_min]
                        chosen_wormhole = wormhole_option[next_blackhole_options.index(next_blackhole)]
                        print("random node chosen to adjust time")

            time += means[chosen_wormhole]
            uncertainity += variances[chosen_wormhole]

            traveresed_blackholes.append(next_blackhole)
            current_blackhole = next_blackhole

            print("Jump ", jumps, "| next black hole: ", next_blackhole, "| time: ", time, "| Uncertainity: ", uncertainity)
            
            if(current_blackhole == data['destination']):
                print(f"Solution found for ship {ship} with {len(traveresed_blackholes)} jumps")
                if not mean_time:
                    return traveresed_blackholes, time
                return traveresed_blackholes

            jumps += 1
            
        print(f"Jumps Exceeded.")


def generate_gen_zero():
    solution6, mean_time = find_solution_for_ship(6)
    solutions = []

    for i in range(NUM_OF_SHIPS):
        solutions.append(find_solution_for_ship(i, mean_time))

    gen_zero = udp.convert_to_chromosome(solutions)
    with open('genzero', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(gen_zero)
    print(gen_zero)



def fitness():
    raise NotImplementedError

def cross_over(parent1, parent2):
    raise NotImplementedError

def selection(population):
    raise NotImplementedError

generate_gen_zero()