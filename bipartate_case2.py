from graph import *
from req_functions import *

class Bipartate_case2(Graph):
    def __init__(self, tasks_mapping, worker_limit):
        """Description: Function used to initiate the graph to the desired form, refer presentation for how the graph is formed
        from the input
        INPUT: List of tasks and list of users, tasks has which workers can work on them and workers_limit has the limit
        on the no of tasks each worker can work on"""

        # Initiate graph
        Graph.__init__(self, [])

        # saving the tasks map and the worker_limit
        self.tasks_mapping = tasks_mapping
        self.worker_limit = worker_limit

        # adding connection from S to each task with he weight of max ppl needed ot do task
        for task in tasks_mapping:
            self.add_connection(['s', task, tasks_mapping[task][1][1]])

            # adding all the dependencies of workers
            for node in tasks_mapping[task][0]:
                self.add_connection([task, node, 1])
        # adding edges from workers to T with  weight as min no of tasks each should work on
        for node in worker_limit:
            self.add_connection([node, 't', worker_limit[node][0]])


    def match(self, algorithm='ford-f'):
        """DES: A bipartite matching is done by calculating the max-flow and the paths used while caluculating the flow
        are used to find out the matches."""

        # calculating flow, this will make sure all the minimum constraint of s=workers are satisfied
        if algorithm == 'ford-f':
            flow, paths_taken, residual_graph = self.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken, residual_graph = self.network_flow('s', 't', True)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')
        print('Step-1')
        print(parse_paths(paths_taken, {}))

        # adding forward edges from workers to t, after min calculation is over with the remaining weight which will be
        # equal to max- min constraints for each worker
        for node in self.worker_limit:
            residual_graph.add_connection([node, 't', self.worker_limit[node][1] - self.worker_limit[node][0]])

        # removing the edges from tasks to S and adding edges with min constraint as the weight, if there are previously
        # any other back edges then also taking that into consideration
        for task in self.tasks_mapping:
            min_val_of_task = self.tasks_mapping[task][1][0]
            weight_to_src = residual_graph.find_connection(task, 's')
            if weight_to_src >= min_val_of_task:
                residual_graph.remove_connection('s', task)
            else:
                residual_graph.remove_connection('s', task)
                residual_graph.add_connection(['s', task, min_val_of_task-weight_to_src])

        # running maz flow again, now min constraints of tasks is satisfied
        if algorithm == 'ford-f':
            flow, paths_taken2, residual_graph = residual_graph.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken2, residual_graph = residual_graph.network_flow('s', 't', True)

        paths_taken += paths_taken2

        print('Step-2')
        print(parse_paths(paths_taken, {}))

        # Finally adding all cases, so adding all the remaining edges to the graph and then calculating flow

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

        # Parsing all the paths taken to find suitable matches
        matched_dict = parse_paths(paths_taken, {})
        print('Step-3')

        # Returning the matches
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

