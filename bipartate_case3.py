from graph import *
import sys

class Bipartate_case3(Graph):
    def __init__(self, tasks_list):
        Graph.__init__(self, [])
        for task in tasks_list:
            weight_of_task = tasks_list[task][0]
            if weight_of_task > 0:
                self.add_connection(['s', task, weight_of_task])
            else:
                self.add_connection([task, 't', -weight_of_task])

            for prereq in tasks_list[task][1]:
                self.add_connection([task, prereq, sys.maxsize])

        print('init-graph')
        print(self.g)

    def match(self, algorithm='ford-f'):
        if algorithm == 'ford-f':
            flow, paths_taken, residual_graph = self.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken, residual_graph = self.network_flow('s', 't', True)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')

        # finding min cut in residual graph
        print(residual_graph.g)
        visited_paths = []
        residual_graph.dfs_wo_pop('s', 't', visited_paths)
        print(visited_paths)




if __name__ == "__main__":
    tasks = {'1': [10, ['3', '2']], '2': [-10, []], '3': [5, ['2']], '4': [-4, ['1']]}

    a = Bipartate_case3(tasks)
    print(a.match())
