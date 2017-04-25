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

    def remove_node(self, node):
        try:
            del self.g[node]

        finally:
            for i in self.g:
                for j in range(len(self.g[i])):
                    if self.g[i][j][0] == node:
                        del self.g[i][j]

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

    def bfs(self, s, t, x, parent_dict):
        x.append(s)
        while True:
            try:
                parent = x.pop(0)
                if parent == t:
                    return True
                for i in range(len(self.g[parent])):
                    x.append(self.g[parent][i][0])
                    parent_dict[x[-1]] = parent

            except KeyError:
                continue

    def find_a_path(self, s, t):
        visited = []
        status = self.dfs(s, t, visited)
        if status:
            return visited
        return []

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
                    return path
                else:
                    t = parent_dict[t]
                    path.append(t)
        return []

    def network_flow(self, s, t):
        # Flow of graph
        flow = 0
        residual_net = None

        # Make a copy of dict
        copy_of_self = copy.deepcopy(self)
        while True:
            path = copy_of_self.find_a_path(s, t)

            if len(path) == 0:
                return flow, residual_net
            curr_flow, residual_net = copy_of_self.calc_flow(path)
            flow += curr_flow

    def remove_connection(self, s, t):
        for i in range(len(self.g[s])):
            if self.g[s][i][0] == t:
                del self.g[s][i]
                return

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
        residual_net = self.update_residual_graph(path, flow)
        return flow, residual_net

    def change_weight(self, s, t, weight):
        for i in range(len(self.g[s])):
            if self.g[s][i][0] == t:
                if self.g[s][i][1] - weight == 0:
                    self.remove_connection(s, t)
                    return
                self.g[s][i][1] -= weight
        return

class Bipartate(Graph):
    def __init__(self, tasks_mapping, worker_limit):
        Graph.__init__(self, [])
        for task in tasks_mapping:
            self.add_connection(['s', task, 1])
            for node in tasks_mapping[task]:
                self.add_connection([task, node, 1])
        for node in worker_limit:
            self.add_connection([node, 't', worker_limit[node]])

    def match(self):
        matched_dict = {}
        paths_array = []
        flow, residual_net = self.network_flow('s', 't')

        while True:
            path = residual_net.find_shortest_path('t', 's')
            print(path)
            if len(path) == 0:
                break
            paths_array.append(path)
            residual_net.change_weight('t', path[1], 1)

        print(paths_array)
        for path in paths_array:
            try:
                matched_dict[path[2]].append(path[1])
            except KeyError:
                matched_dict[path[2]] = [path[1]]

        return matched_dict

if __name__ == '__main__':
    tasks_map = {'tas1': ['w1', 'w2', 'w3'], 'tas2': ['w1', 'w2', 'w3'], 'tas3': ['w1']}
    workers = {'w1': 1, 'w2': 5, 'w3': 7}
    a = Bipartate(tasks_map, workers)

    print(a.match())














