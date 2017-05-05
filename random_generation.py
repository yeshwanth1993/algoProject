import random
import numpy.random as random


def generate_inputs_task1(no_of_workers, no_of_tasks):
    worker_settings,task_settings = {}, {}
    for i in range(1, no_of_workers+1):
        max_tasks = random.randint(1,no_of_tasks+1)
        worker_settings['w'+str(i)] = max_tasks
    for i in range(1,no_of_tasks+1):    
        suitable_workers = random.randint(1, no_of_workers+1, size=random.randint(1,no_of_workers+1))
        suitable_workers = map(str,list(set(suitable_workers)))
        suitable_workers = ['w'+s for s in suitable_workers]
        task_settings['task'+str(i)] = suitable_workers 
    return task_settings, worker_settings


def generate_input_task3(no_of_tasks,max_profit=100):
    tasks = range(1,no_of_tasks+1)
    dependent_tasks = set(random.choice(tasks,size = random.randint(1,int(2 * no_of_tasks/3.0))))
    independent_tasks = list(set(tasks) - dependent_tasks)
    dependent_tasks = list(dependent_tasks)
    task_config = {}
    for i in range(0,len(dependent_tasks)):
        pre_reqs = list(map(str,set(random.choice(independent_tasks,size = len(independent_tasks)+1))))
        profit = random.randint(1,max_profit+1)
        task_config[str(dependent_tasks[i])] =[profit , pre_reqs]
    for i in range(0,len(independent_tasks)):
        profit = random.randint(1,max_profit+1)
        task_config[str(independent_tasks[i])] =[-profit , []]
    return task_config


def get_input_cases_task3(num_tasks = 1000):
    graphs = []
    for num in range(50,num_tasks+1,50):
         graphs.append((num,generate_input_task3(num)))
    return graphs


def generate_inputs_task2(no_of_workers,no_of_tasks):
    worker_settings,task_settings = [],[]
    for i in range(1,no_of_workers+1):
        min_tasks = random.randint(1,no_of_tasks)
        max_tasks = random.randint(min_tasks,no_of_tasks+1)
        worker_settings += [(i,(min_tasks,max_tasks))]
    for i in range(1,no_of_tasks+1):    
        suitable_workers = random.randint(1, no_of_workers+1, size=random.randint(1,no_of_workers+1))
        suitable_workers = list(set(suitable_workers))
        min_workers = random.randint(1, len(suitable_workers))
        max_workers = random.randint(min_workers+1, no_of_workers+1)
        task_settings += [(i,(min_workers,max_workers),suitable_tasks)]

    return worker_settings,task_settings


def sample_parameters():
    num_tasks= 100
    cases = []
    for t in range(10,num_tasks+1):
        num_workers = random.randint(int(t/2.0),t+1)
        worker_settings,task_settings = generate_inputs_task1(num_workers,t)
        cases += [(t,num_workers,worker_settings,task_settings)] # (num_tasks, num_workers, worker_compatibility)
    return cases

if __name__ == '__main__':
    #file_contents = read_csv('task_details.csv')
    #print(file_contents)
    print(generate_inputs_task1(10, 10))