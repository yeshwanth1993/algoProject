# import required libraries
import copy

class Graph (object):
    def __init__(self, connections):
        """Description: Initiates the graph with connections array, which is an array of connections each connection is
        of the form [nodeA, nodeB, weight of edge]"""

        # Represents the data structure to store graph connections
        self.g = {}

        # Adds the connections one by one to the graph
        for i in connections:
            self.add_connection(i)

    def add_connection(self, connection):
        """Description: adds the connection to the graph, which is represented by the adjacency list,
        INPUT: an array of len three, representation - > [nodeA, nodeB, weight of edge]"""
        assert len(connection) == 3, 'Invalid input given'

        try:
            for i in range(len(self.g[connection[0]])):
                # If the same edge exists then the weight of that edge is increased
                if self.g[connection[0]][i][0] == connection[1]:
                    self.g[connection[0]][i][1] += connection[2]
                    return

            # Else a new connection is added to the adjacency list.
            self.g[connection[0]].append([connection[1], connection[2]])
        except KeyError:
            # If node A also doesn't exist in the adjacency list
            self.g[connection[0]] = [[connection[1], connection[2]]]

    def remove_connection(self, s, t):
        """Description: removes a connection from the graph by manipulating the ADJ list.
        INPUT: the edge s->t is given and the edge is removed if there is no such edge nothing is done."""

        # Iterating over the ADJ list to find the node S and removing T from its connections
        for i in range(len(self.g[s])):
            if self.g[s][i][0] == t:
                del self.g[s][i]
                return

    def remove_node(self, node):
        """Description: Removes the entire node from the graph along with all the edges connected to it.
        INPUT: the node to be removed"""

        # Deletes the node
        try:
            del self.g[node]

        # Finally removes all the other places where the node has been referenced. E.g: if there was another connection
        # A -> C iterates over A and removes that edge.
        finally:
            for i in self.g:
                for j in range(len(self.g[i])):
                    if self.g[i][j][0] == node:
                        del self.g[i][j]

    def find_connection(self, s, t):
        """DES: Return weight between s and t, if no connection return 0
        INPUT: the nodes between which the weight has to be returened for"""
        try:
            # Iterate over ADJ list to find T and return weight
            for node in self.g[s]:
                if node[0] == t:
                    return node[1]

            return 0

        # If no such node as S return 0
        except KeyError:
            return 0

    def bfs(self, s, t, x, parent_dict):
        """Des: A BFS function with S as the source to start from and T as the destination. X is used as the queue
        required for BFS to work and parent_dict to store the parent of each node explored to calculate the final
        path from S to T later on"""

        # Adds S to the queue
        x.append(s)

        # Entire while loop where bFS in implemented, keeps exploring the graph until T is found
        while True:
            try:
                # Dequeue this node to find its children and to see if it is T
                parent = x.pop(0)
                # Return True when destination is found
                if parent == t:
                    return True

                # Else explore its child(Edges going into)
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
        """Des: A DFS function with S as the source to start from and T as the destination. X is used as the stack
        required for DFS."""

        # Push S to the stack
        x.append(s)
        try:
            # Exploring every child of S
            for i in range(len(self.g[s])):
                # If child has already been explored then continue
                if self.g[s][i][0] in x:
                    continue
                # If T is found return Ture
                if self.g[s][i][0] == t:
                    x.append(t)
                    return True
                status = self.dfs(self.g[s][i][0], t, x)
                if status:
                    return True

                x.pop()
        # T is not found therefore return False
        except:
            return False

        return False

    def dfs_wo_pop(self, s, t, x):
        """Des: A DFS function with S as the source to start from and T as the destination. X is used as the stack
                required for DFS. This version of the DFS is with poping the stack, therefore using the stack returned
                we can find all the nodes that are either directly or indirectly connected to the node S if we give an
                unreachable input T"""

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
        """Des: Using BFS finds the shortest path b/w S and T.
        INPUT S and T"""

        # Visited Array
        visited = []

        # Dictionary to keep track of each explored node's parent
        parent_dict = {}
        path = []

        # Stating BFS
        status = self.bfs(s, t, visited, parent_dict)

        # If there exists a path
        if status:
            path.append(t)
            while True:
                # Forming a path by backtracking on the parent dictionary
                if parent_dict[t] == s:
                    path.append(s)
                    path.reverse()
                    return path
                else:
                    t = parent_dict[t]
                    path.append(t)
        # If status is False means there is no path from S to T, therefore returning empty array
        return []

    def find_a_path(self, s, t):
        """Des: uses DFS to return a path"""
        visited = []
        path = []
        status = self.dfs(s, t, visited)

        if status:
            for i in visited:
                path.append(i)
            path = []
            for i in visited:
                path.append(i)
            path = []
            for i in visited:
                path.append(i)

            path.reverse()
            path.reverse()
            return path
        return path

    def network_flow(self, s, t, algo):
        """DES: Calculates flow from S to T, first copies graph so that which flow calculations the graph is not affected
        due to formations of residual graphs. THe same algorithm can be used to calculate flow using both Edmon-Karp
        and Ford fulkerson.
        INPUT: S and T, EK set to true uses Edmond Karp and False uses Ford-Fulkerson"""
        # Flow of graph
        flow = 0
        paths_taken = []

        # Make a copy of dict
        copy_of_self = copy.deepcopy(self)
        residual_graph = copy.deepcopy(self)
        while True:
            # Finding a path
            if algo == 'ek':
                path = copy_of_self.find_shortest_path(s, t)
            elif algo == 'ff':
                path = copy_of_self.find_a_path(s, t)
            else:
                raise ValueError('Wrong algorithm specified')

            # Once the length of the path is zero, return the flow
            if len(path) == 0:
                return flow, paths_taken, residual_graph

            # Calculate the flow for that augmenting path and append it to the paths_taken array which ll later help us
            # find the matches in the bipartite graph
            curr_flow, residual_graph = copy_of_self.calc_flow(path)
            paths_taken.append((path, curr_flow))

            # Increase the Flow by the flow for this path
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

        # Once the flow is calculated, the residual graph is updated
        residual_graph = self.update_residual_graph(path, flow)
        return flow, residual_graph

    def update_residual_graph(self, path, flow):
        """Des: Updates the residual graph once the flow is calculated for one particular path
        INPUT path and flow of that path."""
        try:
            # for every node in the path, removing and adding reverse edges.
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

if __name__ == "__main__":
    connections = [['a', 'b', 1], ['c', 'd', 2]]
