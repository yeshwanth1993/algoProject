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

    def find_a_path(self, s, t):
        visited = []
        status = self.dfs(s, t, visited)
        if status:
            return visited
        return []

    def network_flow(self, s, t):
        # Flow of graph
        flow = 0

        # Make a copy of dict
        copy_of_self = copy.deepcopy(self)
        while True:
            path = copy_of_self.find_a_path(s, t)
            if len(path) == 0:
                return flow

            curr_flow = copy_of_self.calc_flow(path)
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
        self.update_residual_graph(path, flow)
        return flow

