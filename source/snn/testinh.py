import pyNN.nest as pynn
from pyNN.utility.plotting import Figure, Panel

import matplotlib.pyplot as plt

pynn.setup()

#e = pynn.Population(1, pynn.SpikeSourceArray(spike_times=[1,2,3,4,5,6,7,8,9,21,22,23,24,25,26,27,28,29]))
#i = pynn.Population(1, pynn.SpikeSourceArray(spike_times=[22,23,24,25,26,27,28,29]))
e = pynn.Population(1, pynn.IF_cond_exp())#pynn.SpikeSourceArray(spike_times=[1,2,3,4,5,6,7,8,9,21,22,23,24,25,26,27,28,29]))
i = pynn.Population(1, pynn.IF_cond_exp())#pynn.SpikeSourceArray(spike_times=[22,23,24,25,26,27,28,29]))


o = pynn.Population(1, pynn.IF_cond_exp())

connector = pynn.AllToAllConnector()
pe = pynn.Projection(e,o, connector)
pi = pynn.Projection(i,o, connector,receptor_type='inhibitory')

pe.set(weight=2)
pi.set(weight=6)

o.record('spikes')

e.initialize(v=1)
pynn.run(20)
e.initialize(v=1)
i.initialize(v=1)


pynn.run(50)

spikes = o.get_data().segments[0].spiketrains
Figure(
    Panel(spikes)
)

plt.plot(o)
plt.show()