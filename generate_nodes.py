import random_generation
from bipartate_case1 import *
from bipartate_case2 import *
from bipartate_case3 import *
import matplotlib.pyplot as plt

def test_case1(no_of_nodes, increment):
    iterations = []
    ford_time_arr = []
    edmond_time_arr = []
    flow_arr = []

    for i in range(increment, no_of_nodes, increment):
        # print('***')
        # Case where both tasks and workers increase
        tasks, workers = random_generation.generate_inputs_task1(no_of_workers=i, no_of_tasks=i)

        case1_graph = Bipartate_case1(tasks_mapping=tasks, worker_limit=workers)

        matches, ford_time, flow1 = case1_graph.match(algo='ff')
        matches, edmond_time, flow2 = case1_graph.match(algo='ek')

        #if flow1 != flow2:
         #   raise ValueError('Algo is wrong')

        iterations.append(i)
        ford_time_arr.append(ford_time)
        edmond_time_arr.append(edmond_time)
        flow_arr.append(flow1/100)



    # plt.plot(iterations, flow_arr, c='R', marker='.',label='Ford Fulkerson')

    fig = plt.figure()
    plt.plot(iterations, edmond_time_arr, c='G', marker='8',label='Edmond Karp')
    plt.plot(iterations, ford_time_arr, c='B', marker='o', label='Ford Fulkerson')
    fig.suptitle('FORD FULKERSON V/S EDMOND KARP PERFORMANCE')
    legend = plt.legend(loc='upper center', shadow=True)
    plt.xlabel('Iterations')
    plt.ylabel('Time Taken')
    plt.show()
    print(iterations, ford_time_arr)

    # print('mac - ek:' + str(max(edmond_time_arr)))
    # print('mac - ff:' + str(max(ford_time_arr)))

    return

def test_case3(no_of_nodes, increment):
    iterations = []
    ford_time_arr = []
    edmond_time_arr = []

    for i in range(increment, no_of_nodes, increment):
        # print('***')
        # Case where both tasks and workers increase
        tasks = random_generation.get_input_cases_task3(num_tasks=i)

        case3_graph = Bipartate_case3(tasks_list=tasks)


        matches, ford_time = case3_graph.match(algo='ff')
        matches, edmond_time = case3_graph.match(algo='ek')

        #if flow1 != flow2:
         #   raise ValueError('Algo is wrong')

        iterations.append(i)
        ford_time_arr.append(ford_time)
        edmond_time_arr.append(edmond_time)



    # plt.plot(iterations, flow_arr, c='R', marker='.',label='Ford Fulkerson')

    fig = plt.figure()
    plt.plot(iterations, edmond_time_arr, c='G', marker='8',label='Edmond Karp')
    plt.plot(iterations, ford_time_arr, c='B', marker='o', label='Ford Fulkerson')
    fig.suptitle('FORD FULKERSON V/S EDMOND KARP PERFORMANCE')
    legend = plt.legend(loc='upper center', shadow=True)
    plt.xlabel('Iterations')
    plt.ylabel('Time Taken')
    plt.show()
    print(iterations, ford_time_arr)

    # print('mac - ek:' + str(max(edmond_time_arr)))
    # print('mac - ff:' + str(max(ford_time_arr)))

    return


if __name__ == "__main__":

    test_case3(200, 10)
