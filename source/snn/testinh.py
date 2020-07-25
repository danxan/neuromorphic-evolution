import pyNN.nest as pynn
from pyNN.utility.plotting import Figure, Panel
from pyNN.random import RandomDistribution

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

pe.set(weight=0.1)
pi.set(weight=6)

o.record('spikes')

#e.set(spike_times=[1])
e.initialize(v=1)
pynn.run_until(20)
time = pynn.get_current_time()+1
#e.set(spike_times=[time])
e.initialize(v=1)
#i.initialize(v=0)


pynn.run(100)

spikes = o.get_data().segments[0].spiketrains
Figure(
    Panel(spikes)
)

plt.plot(o)
plt.show()
print(RandomDistribution('uniform', (-5,5)).next(10))