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
networkTree = BlackholeNetworkTree(data, 10000)


def get_blackholes_with_destination(destination):
    sources = {x[0] for x in data['edges'] if x[1] == destination}
    return sources


penultimate_blackholes = get_blackholes_with_destination(DESTINATION)


def get_wormholes_with_source(source):
    wormhole_indexes = [i for i, (s, d) in enumerate(edges) if s == source]
    destination_blackholes = [d for s, d in edges if s == source]
    wormhole_means = [means[i] for i in wormhole_indexes]
    return wormhole_indexes, wormhole_means, destination_blackholes


def get_means_by_wormholes(wormholes):
    return [means[w] for w in wormholes]


def find_solution_for_ship(ship, mean_time):
    attempt = 0
    while(True):
        attempt += 1
        origin_blackhole = random.choice(origins[ship])
        current_blackhole = origin_blackhole
        traveresed_blackholes = [origin_blackhole]
        jumps = 1
        time = data['delays'][ship]
        uncertainity = 0
        is_current_blackhole_penultimate = False
        
        while(jumps < JUMP_LIMIT):
            wormhole_option, wormhole_means, next_blackhole_options = get_wormholes_with_source(current_blackhole)
            chosen_wormhole = None
            next_blackhole = None

            if is_current_blackhole_penultimate:
                chosen_wormhole = wormhole_option[next_blackhole_options.index(DESTINATION)]
                chosen_wormhole_mean = means[chosen_wormhole]

                if abs(time+chosen_wormhole_mean-mean_time) <= 0.5:
                    next_blackhole = DESTINATION
                    time += means[chosen_wormhole]
                    uncertainity += variances[chosen_wormhole]

                    traveresed_blackholes.append(next_blackhole)
                    current_blackhole = next_blackhole
                    print(f"Solution found for ship {ship} with {jumps} jumps")
                    if not mean_time:
                        return traveresed_blackholes, time
                    return traveresed_blackholes
                    print("Destination reached")
            
            # Try to end journey if mean time in reach
            if abs(time-mean_time) <= 0.5:
                for b in next_blackhole_options:
                    if b in penultimate_blackholes:
                        chosen_wormhole = wormhole_option[next_blackhole_options.index(b)]
                        chosen_wormhole_mean = means[chosen_wormhole]

                        if abs(time+chosen_wormhole_mean-mean_time) <= 0.5:
                            next_blackhole = b
                            is_current_blackhole_penultimate = True
                            break

            if not next_blackhole:
                if time < mean_time:
                    chosen_mean_index = random.randrange(len(wormhole_means))
                    while wormhole_means[chosen_mean_index] < 0:
                        chosen_mean_index = random.randrange(len(wormhole_means))

                    next_blackhole = next_blackhole_options[chosen_mean_index]
                    
                else:
                    chosen_mean_index = random.randrange(len(wormhole_means))
                    while wormhole_means[chosen_mean_index] > 0:
                        chosen_mean_index = random.randrange(len(wormhole_means))

                    next_blackhole = next_blackhole_options[chosen_mean_index]
                
                chosen_wormhole = wormhole_option[chosen_mean_index]

            time += means[chosen_wormhole]
            uncertainity += variances[chosen_wormhole]

            traveresed_blackholes.append(next_blackhole)
            current_blackhole = next_blackhole

            print("Jump ", jumps, "| current blackhole: ", next_blackhole, "| time: ", time, "| Uncertainity: ", uncertainity, f"Attempt {attempt} for ship {ship} with goal time {mean_time}")

            jumps += 1
            
        print(f"Jumps Exceeded.")


def generate_gen_zero():
    mean_delay_time = sum(data['delays'])/len(data['delays'])
    solutions = [find_solution_for_ship(i, mean_delay_time) for i in range(NUM_OF_SHIPS)]

    gen_zero = udp.convert_to_chromosome(solutions)
    np.save('genzero', gen_zero)
    print(gen_zero)



def fitness():
    raise NotImplementedError

def cross_over(parent1, parent2):
    raise NotImplementedError

def selection(population):
    raise NotImplementedError

generate_gen_zero()