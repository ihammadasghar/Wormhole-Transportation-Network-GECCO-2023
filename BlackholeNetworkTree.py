class Blackhole:
    def __init__(self, id):
        self.id = id
        self.wormholes = []
        self.visited = False


class Wormhole:
    def __init__(self, time_offset, uncertainity, destination):
        self.time_offset = time_offset
        self.uncertainity = uncertainity
        self.destination = destination


class BlackholeNetworkTree:
    def __init__(self, edges, means, variances, num_of_blackholes):
        self.blackholes = {(i+1): Blackhole(i+1) for i in range(num_of_blackholes)}
        
        for i, (source, destination) in enumerate(edges):
            wormhole = Wormhole(means[i], variances[i], self.blackholes[destination])
            self.blackholes[source].wormholes.append(wormhole)
