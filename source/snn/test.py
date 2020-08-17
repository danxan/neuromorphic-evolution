from nest import *
from nestAnimat import Animat
from nestGenome import Genome

import numpy as np


g = Genome(5,4, 0, low=0, high=10000)

sds = []
for i in range(2):
    sds.append(Create('spike_detector'))


a = Animat(g, sds)
SetStatus(a.sgs[0], {'spike_times': [1.0]})
SetStatus(a.sgs[1], {'spike_times': [10.0]})
Simulate(20)
print(GetStatus(a.sgs[0]))
print(GetStatus(a.sgs[1]))



print(GetStatus(sds[0]))
print(GetStatus(sds[1]))

ResetKernel()


