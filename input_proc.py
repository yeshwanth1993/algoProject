import ast

def parse_case1(taskfile, workerfile):
    f_worker = open(workerfile,'r')
    f_task = open(taskfile,'r')

    workers = {}
    worker_no = int(f_worker.readline())

    for line in f_worker.readlines():
        wid,mint,maxt=line.split(' ')
        workers[wid]=int(mint)
    tasks = {}
    task_no = int(f_task.readline())
    for line in f_task.readlines():
        tid, mint, maxt, wlist = line.split(' ')
        tasks[tid] = ast.literal_eval(wlist.strip())


    return tasks,workers


def parse_case2(taskfile,workerfile):
	f_worker=open(workerfile,'r')
	f_task=open(taskfile,'r')
	
	
	workers={}
	worker_no=int(f_worker.readline())
	
	for line in f_worker.readlines():
		wid,mint,maxt=line.split()
		workers[wid]=[int(mint),int(maxt)]
	tasks={}
	task_no=int(f_task.readline())
	for line in f_task.readlines():
		
		tid,mint,maxt,wlist=line.split()

		tasks[tid]=(ast.literal_eval(wlist.strip()),[int(mint),int(maxt)])
	return tasks,workers

def parse_case3(taskfile):
	f_task=open(taskfile,'r')
	task_no = int(f_task.readline())
	tasks={}

	for line in f_task.readlines():
		tid, profit, wlist = line.split(' ')
		if not wlist:
			wlist=[]
		tasks[tid] = [int(profit),ast.literal_eval(wlist.strip())]

	return tasks


