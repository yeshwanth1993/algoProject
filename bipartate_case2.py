from graph import *
from req_functions import *

class Bipartate_case2(Graph):
    def __init__(self, tasks_mapping, worker_limit):
        Graph.__init__(self, [])
        self.tasks_mapping = tasks_mapping
        self.worker_limit = worker_limit

        for task in tasks_mapping:
            self.add_connection(['s', task, tasks_mapping[task][1][1]])
            for node in tasks_mapping[task][0]:
                self.add_connection([task, node, 1])
        for node in worker_limit:
            self.add_connection([node, 't', worker_limit[node][0]])


    def match(self, algorithm='ford-f'):
        if algorithm == 'ford-f':
            flow, paths_taken, residual_graph = self.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken, residual_graph = self.network_flow('s', 't', True)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')
        print('Step-1')
        print(parse_paths(paths_taken, {}))

        # adding forward edges from workers to t, after min calculation is over
        for node in self.worker_limit:
            residual_graph.add_connection([node, 't', self.worker_limit[node][1] - self.worker_limit[node][0]])

        for task in self.tasks_mapping:
            min_val_of_task = self.tasks_mapping[task][1][0]
            weight_to_src = residual_graph.find_connection(task, 's')
            if weight_to_src >= min_val_of_task:
                residual_graph.remove_connection('s', task)
            else:
                residual_graph.remove_connection('s', task)
                residual_graph.add_connection(['s', task, min_val_of_task-weight_to_src])

        if algorithm == 'ford-f':
            flow, paths_taken2, residual_graph = residual_graph.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken2, residual_graph = residual_graph.network_flow('s', 't', True)

        paths_taken += paths_taken2

        print('Step-2')
        print(parse_paths(paths_taken, {}))

        # Finally adding all cases

        for task in self.tasks_mapping:
            max_val_of_task = self.tasks_mapping[task][1][1]
            weight_to_src = residual_graph.find_connection(task, 's')

            if weight_to_src < max_val_of_task:
                residual_graph.add_connection(['s', task, max_val_of_task - weight_to_src])

        if algorithm == 'ford-f':
            flow, paths_taken3, residual_graph = residual_graph.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken3, residual_graph = residual_graph.network_flow('s', 't', True)

        paths_taken += paths_taken3

        matched_dict = parse_paths(paths_taken, {})
        print('Step-3')
        return matched_dict


if __name__ == '__main__':
    # Testing of bipartate class which is built on Graph class
    tasks_map = {'tas1': (['w1', 'w2', 'w5'], [2, 5]), 'tas2': (['w1', 'w2', 'w4', 'w5'], [3, 6]),
                 'tas3': (['w2', 'w3', 'w4', 'w5'], [3, 4])}

    workers = {'w1': [1, 4], 'w2': [2, 5], 'w3': [1, 3], 'w4': [1, 2], 'w5': [2, 3]}
    a = Bipartate_case2(tasks_map, workers)

    # Testing using both algorithms
    # print(a.match('ford-f'))
    # print(a.match('edmond-k'))
    print('Mapping:')
    print(a.match())

