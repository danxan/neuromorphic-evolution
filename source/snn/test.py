from nest import *
from nestAnimat import Animat
from nestGenome import Genome

import numpy as np


g = Genome(5,4, 0)
sg = []
sd = []
for i in range(2):
    sg.append(Create('spike_generator'))
    sd.append(Create('spike_detector'))
    SetStatus(sg[i], {'spike_times': [1.0]})

a = Animat(sg, sd, g)
conn = GetConnections(a.hid[0], a.out[0])
Prepare()
print(conn)
Run(10)

for s in sd:
    print(GetStatus(s))

ResetNetwork()

g.ow = np.zeros((g.nh,g.no))

a.set_weights(g)

for i in range(2):
    SetStatus(sg[i], {'spike_times': [11.0]})

Run(10)

for s in sd:
    print(GetStatus(s))

Cleanup()

print(1)





