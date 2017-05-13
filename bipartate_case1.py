from graph import *
from req_functions import *
import time
from input_proc import *

class Bipartate_case1(Graph):
    def __init__(self, tasks_mapping, worker_limit):
        """Description: Function used to initiate the graph to the desired form, refer presentation for how the graph is formed
        from the input
        INPUT: List of tasks and list of users, tasks has which workers can work on them and workers_limit has the limit
        on the no of tasks each worker can work on"""

        # Initiate graph
        Graph.__init__(self, [])
        for task in tasks_mapping:
            # For every task add the edge from S to task
            self.add_connection(['s', task, 1])
            # Add edges to all workers who can do the task
            for node in tasks_mapping[task]:
                self.add_connection([task, node, 1])

        # Add worker to T edge with the worker limit
        for node in worker_limit:
            self.add_connection([node, 't', worker_limit[node]])

    def match(self, algo):
        """DES: A bipartite matching is done by calculating the max-flow and the paths used while caluculating the flow
        are used to find out the matches."""
        start = time.time()
        if algo == 'ff' or algo == 'ek':
            flow, paths_taken, residual_graph,tm = self.network_flow('s', 't', algo)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')

        # print(paths_taken)
        # parse_paths takes in the paths taken during the caluculation of the max flow and gives the matches b/w
        # workers and tasks
        # matched_dict = parse_paths(paths_taken, {})
        end = time.time()
        return parse_paths(paths_taken, {})

if __name__ == '__main__':
    # Testing of bipartate class which is built on Graph class
    tasks_map = {'tas1': ['w2'], 'tas2': ['w2'], 'tas3': ['w1']}
    workers = {'w1': 2, 'w2': 1}

    # In case you want to import the tasks and workers from a CSV the below line is an example of how to do it
    # tasks_map1, workers1 = parse_case1('csv/case1/tasks.txt', 'csv/case1/worker.txt')

    a = Bipartate_case1(tasks_map, workers)

    # Testing using both algorithms
    print('Mapping using Ford-fulkerson: ')
    print(a.match('ff'))

    print('Mapping using Edmond-Karp:')
    print(a.match('ek'))

   

