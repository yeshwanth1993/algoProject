import random
nrange = lambda start, end: range(start, end+1)

def create_random_DAG(no_of_vertices, threshold, max_capacity):
    edges = []
    for i in nrange(1,no_of_vertices):
        for j in nrange(1,i):
            if (random.random() < threshold and i != j):
                edges.append([str(i),str(j), int(random.uniform(1,max_capacity))])
    
    return edges

def create_graph(num_vertices):
    th = 0.7#random.random()
    return create_random_DAG(num_vertices, th, 100)

print(create_graph(20))