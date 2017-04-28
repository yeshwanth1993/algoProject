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

    def dfs_wo_pop(self, s, t, x):
        print(s)
        x.append(s)
        try:
            for i in range(len(self.g[s])):
                edge_to = self.g[s][i][0]
                if edge_to in x:
                    continue
                if edge_to == t:
                    x.append(t)
                    return True
                status = self.dfs_wo_pop(edge_to, t, x)
                if status:
                    return True

        except Exception as e:
            print(str(e))
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
        residual_graph = copy.deepcopy(self)
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

