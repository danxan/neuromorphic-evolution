import multiprocessing as mp
import queue
import numpy as np


from genome import SgaGenome
from pynnAnimat import Animat
from evaltest import Eval

taskstobedone = mp.Queue()
tasksthataredone = mp.Queue()
tasks = []
completedtaskslist = []

def do_job(taskstobedone, completedtaskslist):
    while True:
        doneg = []
        try:
            task = taskstobedone.get_nowait()
            for g in task:
                a = Animat()
                e = Eval()
                doneg += e.eval_genome(g, a)
        except queue.Empty:
            break
        else:
            tasksthataredone.put(doneg)

    return True

genomes = []
#animats = []
for i in range(1,11):
    genomes.append(SgaGenome(id=i))
    #animats.append(Animat())


numprocs = 1
processes = []

b = []
chunk = int(len(genomes)/numprocs)
for i in range(1, chunk+1):
    taskstobedone.put(genomes[chunk*(i-1):chunk*(i)])#, animats[chunk*(i-1):chunk*(i)]))

    for w in range(numprocs):
        p = mp.Process(target=do_job, args=(taskstobedone, completedtaskslist))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    b += tasksthataredone.get()

print(b)


