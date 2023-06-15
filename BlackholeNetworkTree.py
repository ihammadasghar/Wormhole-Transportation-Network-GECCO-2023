class Blackhole:
    def __init__(self):
        self.wormholes = []
        self.visited = False


class Wormhole:
    def __init__(self, time_offset, uncertainity, destination):
        self.time_offset = time_offset
        self.uncertainity = uncertainity
        self.destination = destination


class BlackholeNetworkTree:
    def __init__(self, data, num_of_blackholes):
        self.blackholes = {(i+1): Blackhole() for i in range(num_of_blackholes)}
        self.wormholes = {i: Wormhole(data['meanvar'][i][0], data['meanvar'][i][1], d) for i, (_, d) in enumerate(data['edges'])}

        for i, (source, destination) in enumerate(data['edges']):
            wormhole = Wormhole(data['meanvar'][i][0], data['meanvar'][i][1], self.blackholes[destination])
            self.wormholes[i] = Wormhole(data['meanvar'][i][0], data['meanvar'][i][1], destination)
            self.blackholes[source].wormholes.append(wormhole)
