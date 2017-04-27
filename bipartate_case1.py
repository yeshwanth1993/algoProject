from graph import *
from req_functions import *

class Bipartate_case1(Graph):
    def __init__(self, tasks_mapping, worker_limit):
        Graph.__init__(self, [])
        for task in tasks_mapping:
            self.add_connection(['s', task, 1])
            for node in tasks_mapping[task]:
                self.add_connection([task, node, 1])
        for node in worker_limit:
            self.add_connection([node, 't', worker_limit[node]])

    def match(self, algorithm='ford-f'):
        if algorithm == 'ford-f':
            flow, paths_taken, residual_graph = self.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken, residual_graph = self.network_flow('s', 't', True)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')
        print(paths_taken)
        matched_dict = parse_paths(paths_taken, {})
        return  matched_dict

if __name__ == '__main__':
    # Testing of bipartate class which is built on Graph class
    tasks_map = {'tas1': ['w1'], 'tas2': ['w2'], 'tas3': ['w1']}
    workers = {'w1': 1, 'w2': 1, 'w3': 1}
    a = Bipartate_case1(tasks_map, workers)

    # Testing using both algorithms
    print(a.match('ford-f'))
    print(a.match('edmond-k'))

    # THis is Testing of graph class itself where graph is constructed using the conn array
    # The connection array is comprised of smaller arrays, each small array
    # represents an edge ['source_node', 'Destination_node', 'Weight_of_edge']

    conn = [['s', 'a', 15], ['s', 'c', 20], ['a', 'c', 10], ['a', 'b', 3], ['c', 'b', 12], ['c', 't', 15],
            ['b', 't', 20]]
    b = Graph(conn)
    # network flow using Ford-f
    print(b.network_flow('s', 't'))

    # flow using ed-k
    print(b.network_flow('s', 't', True))
