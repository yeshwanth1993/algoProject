import copy


class Graph (object):
    def __init__(self, connections):
        self.g = {}
        for i in connections:
            self.add_connection(i)

    def add_connection(self, connection):
        assert len(connection) == 3, 'Invalid input given'
        try:
            # Checking if same entry exists
            for i in range(len(self.g[connection[0]])):
                if self.g[connection[0]][i][0] == connection[1]:
                    self.g[connection[0]][i][1] += connection[2]
                    return

            self.g[connection[0]].append([connection[1], connection[2]])
        except KeyError:
            self.g[connection[0]] = [[connection[1], connection[2]]]

    def remove_connection(self, s, t):
        for i in range(len(self.g[s])):
            if self.g[s][i][0] == t:
                del self.g[s][i]
                return

    def remove_node(self, node):
        try:
            del self.g[node]

        finally:
            for i in self.g:
                for j in range(len(self.g[i])):
                    if self.g[i][j][0] == node:
                        del self.g[i][j]

    def find_connection(self, s, t):
        """Return weight between s and t, if no connection return 0"""
        try:
            for node in self.g[s]:
                if node[0] == t:
                    return node[1]

            return 0
        except KeyError:
            return 0

    def bfs(self, s, t, x, parent_dict):
        x.append(s)
        while True:
            try:
                parent = x.pop(0)
                if parent == t:
                    return True
                for i in range(len(self.g[parent])):
                    if self.g[parent][i][0] in parent_dict:
                        continue
                    x.append(self.g[parent][i][0])
                    parent_dict[x[-1]] = parent

            except KeyError:
                continue
            except IndexError:
                break

    def dfs(self, s, t, x):
        x.append(s)
        try:
            for i in range(len(self.g[s])):
                if self.g[s][i][0] in x:
                    continue
                if self.g[s][i][0] == t:
                    x.append(t)
                    return True
                status = self.dfs(self.g[s][i][0], t, x)
                if status:
                    return True
                x.pop()

        except:
            return False

        return False

    def find_shortest_path(self, s, t):
        visited = []
        parent_dict = {}
        path = []
        status = self.bfs(s, t, visited, parent_dict)
        if status:
            path.append(t)
            while True:
                if parent_dict[t] == s:
                    path.append(s)
                    path.reverse()
                    return path
                else:
                    t = parent_dict[t]
                    path.append(t)
        return []

    def find_a_path(self, s, t):
        visited = []
        status = self.dfs(s, t, visited)
        if status:
            return visited
        return []

    def network_flow(self, s, t, ek=False):
        # Flow of graph
        flow = 0
        paths_taken = []

        # Make a copy of dict
        copy_of_self = copy.deepcopy(self)
        while True:
            if ek:
                path = copy_of_self.find_shortest_path(s, t)
            else:
                path = copy_of_self.find_a_path(s, t)

            if len(path) == 0:
                return flow, paths_taken, residual_graph

            curr_flow, residual_graph = copy_of_self.calc_flow(path)
            paths_taken.append((path, curr_flow))
            flow += curr_flow

    def calc_flow(self, path):
        # calculate lowest flow in path
        flow_of_path = []
        try:
            for i in range(len(path)):
                for j in range(len(self.g[path[i]])):
                    if self.g[path[i]][j][0] == path[i+1]:
                        # Flow from i--> i+1 in path array
                        flow_of_path.append(self.g[path[i]][j][1])

        except (IndexError, KeyError):
            pass
        flow = min(flow_of_path)
        residual_graph = self.update_residual_graph(path, flow)
        return flow, residual_graph

    def update_residual_graph(self, path, flow):
        # Calculating residual graph
        try:
            for i in range(len(path) - 1):
                for j in range(len(self.g[path[i]])):
                    try:

                        if self.g[path[i]][j][0] == path[i + 1]:
                            self.g[path[i]][j][1] = self.g[path[i]][j][1] - flow

                            if self.g[path[i]][j][1] == 0:
                                self.remove_connection(path[i], path[i+1])

                            self.add_connection([path[i+1], path[i], flow])
                    except IndexError:
                        continue

        except KeyError:
            pass
        return self


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
        matched_dict = {}
        if algorithm == 'ford-f':
            flow, paths_taken, residual_graph = self.network_flow('s', 't')
        elif algorithm == 'edmond-k':
            flow, paths_taken, residual_graph = self.network_flow('s', 't', True)
        else:
            raise ValueError('Algorithm parameter should either be "ford-f" or "edmond-k".')
        # print(flow, paths_taken)

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

        for path in paths_taken:
            if len(path[0]) == 4:
                for node in path[0]:
                    if node[0] == 'w':
                        try:
                            matched_dict[path[0][path[0].index(node) - 1]].append(node)
                        except KeyError:
                            matched_dict[path[0][path[0].index(node) - 1]] = [node]
            elif len(path[0]) == 6:
                first_path = True
                for node in path[0]:
                    index_of_node = path[0].index(node)
                    previous_node_in_path = path[0][index_of_node - 1]

                    if node[0] == 'w' and first_path:
                        try:
                            matched_dict[previous_node_in_path].append(node)
                            first_path = False
                        except KeyError:
                            matched_dict[previous_node_in_path] = [node]
                            first_path = False
                    elif node[0] == 'w':
                        try:
                            matched_dict[previous_node_in_path].remove(path[0][index_of_node - 2])
                            matched_dict[previous_node_in_path].append(node)
                        except KeyError:
                            matched_dict[previous_node_in_path].remove(path[0][path[0].index(node) - 2])
                            matched_dict[previous_node_in_path] = [node]
            else:
                raise TypeError('Returned type of path is not acceptable.')

        return matched_dict

if __name__ == '__main__':
    # Testing of bipartate class which is built on Graph class
    tasks_map = {'tas1': (['w1', 'w2', 'w3'], [2, 3]), 'tas2': (['w1', 'w2', 'w3'], [1, 3]),
                 'tas3': (['w2', 'w3', 'w4'], [2, 3])}

    workers = {'w1': [1, 3], 'w2': [2, 3], 'w3': [2, 5], 'w4': [1, 1]}
    a = Bipartate_case2(tasks_map, workers)

    # Testing using both algorithms
    # print(a.match('ford-f'))
    # print(a.match('edmond-k'))
    print('Mapping:')
    print(a.match())

