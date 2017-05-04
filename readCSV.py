import random
import numpy.random as random
def read_csv(filename):
    file = open(filename,'r')
    file_contents = file.read()
    file_contents = file_contents.split('\n')
    details = [list(map(int, x.split(','))) for x in file_contents ]
    return details
def generate_inputs_task1(no_of_workers,no_of_tasks):
    worker_settings,task_settings = {},{}
    for i in range(1,no_of_workers+1):
        max_tasks = random.randint(1,no_of_tasks+1)
        worker_settings['w'+str(i)] = max_tasks
    for i in range(1,no_of_tasks+1):    
        suitable_workers = random.randint(1, no_of_workers+1, size=random.randint(1,no_of_workers+1))
        suitable_workers = map(str,list(set(suitable_workers)))
        suitable_workers = ['w'+s for s in suitable_workers]
        task_settings['task'+str(i)] = suitable_workers 
    return worker_settings,task_settings    

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
    cases = sample_parameters()
    print(cases[3])