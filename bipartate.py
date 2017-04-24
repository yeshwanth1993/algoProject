from graph import *

conn = [['s', 'a', 15], ['s', 'c', 20], ['a', 'c', 10], ['a', 'b', 3], ['c', 'b', 12], ['c', 't', 15], ['b', 't', 20]]
a = Graph(conn)
print(a.network_flow('s', 't'))
print(a.g)