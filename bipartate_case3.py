from graph import *
import sys
import time

class Bipartate_case3(Graph):
    def __init__(self, tasks_list):
        """Des: Function used to initiate the graph to the desired form, refer presentation for how the graph is formed
        from the input
        INPUT: List of tasks, which has a profit constraint and another list of taks it is dependent on"""

        # Initialize the graph object
        Graph.__init__(self, [])

        for task in tasks_list:
            # profit constraint of every task
            profit_of_task = tasks_list[task][0]

            # If positive profit add edge from S to task
            if profit_of_task > 0:
                self.add_connection(['s', task, profit_of_task])

            # if -ve constraint add edge from task to T
            else:
                self.add_connection([task, 't', -profit_of_task])

            # add edges for prereq with infinity weight
            for prereq in tasks_list[task][1]:
                self.add_connection([task, prereq, sys.maxsize])

        #print('init-graph')
        #print(self.g)

    def match(self, algo):
        """DES: A bipartite matching is done by calculating the max-flow and the paths used while caluculating the flow
        are used to find out the matches."""
        start = time.time()
        # Calculating the required flow and residual graph
        if algo == 'ff' or algo == 'ek':
            flow, paths_taken, residual_graph, tm = self.network_flow('s', 't', algo)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')

        # finding min cut in residual graph
        #print('Residual-graph')
        #print(residual_graph.g)
        # DFS without pop will give all the taks which can be reached by S which actually resembles the
        # Min cut in a graph
        visited_nodes = []
        residual_graph.dfs_wo_pop('s', 't', visited_nodes)
        del visited_nodes[visited_nodes.index('s')]

        # returns the visited nodes in the residual graph from S
        return visited_nodes


if __name__ == "__main__":
    tasks = {'1': [10, ['3', '2']], '2': [-10, []], '3': [5, ['2']], '4': [-4, ['1']]}
    tasks1 = {'1': [7, ['5']], '2': [3, ['6']], '3': [2, []], '4': [2, []],'5':[-7,[]],'6':[-2,[]],'7':[-4,['3']]}
    a = Bipartate_case3(tasks1)

    start = time.time()
    print(sorted([int(i) for i in a.match(algo='ff')]))
    print(sorted([int(i) for i in a.match(algo='ek')]))
    #time = time.time() - start

    #print('Time:' + str(time))
