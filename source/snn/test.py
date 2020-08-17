from nest import *
from nestAnimat import Animat
from nestGenome import Genome

import numpy as np

'''
class Population(object):
    def __init__(self, num_ind, num_trials, genomes):
        self.num_ind = num_ind
        self.num_trials = num_trials
        self.genomes = genomes

        self.trial_a = []
        for i in range(self.num_ind):
            for j in range(self.num_trials):
                self.trial_a.append(
'''






sg = []
sd = []
for i in range(2):
    sg.append(Create('spike_generator'))
    sd.append(Create('spike_detector'))
    SetStatus(sg[i], {'spike_times': [1.0]})
    SetStatus(sd[i], {'n_events': 0})

g = Genome(id=0, low=1000, high=10000)
print("GENOME weights \n")
print("iw\n{}\nhw\n{}\now\n{}".format(g.iw, g.hw, g.ow))

#print("Setting weights")
#a.set_weights(g)
#for i in range(2):
trial_a = []

trials = 10

for t in range(trials):
    a = Animat(g)
    for i in range(2):
        SetStatus(a.sgs[i], {'spike_times': [21.0]})
    trial_a.append(a)


Simulate(40)
for a in trial_a:
    print("n_events: {}".format(GetStatus(a.sds[i])[0]['n_events']))
    print(GetStatus(a.sds[i]))
    SetStatus(a.sds[i], {'n_events': 0})
Simulate(20)

'''
for s in sg:
    print("SPIKE GENERATOR")
    print(GetStatus(s))
for s in sd:
    print("n_events: {}".format(GetStatus(s)[0]['n_events']))
for s in sd:
    print(GetStatus(s))

#Cleanup()

'''


ResetKernel()


