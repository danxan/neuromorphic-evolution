import pyNN.nest as pynn

from pyNN.utility.plotting import Figure, Panel

import matplotlib.pyplot as plt

pynn.setup()

a = pynn.Population(1, pynn.SpikeSourceArray())

si = 1.0

pynn.reset()
#pynn.record(['spikes'], a, filename='output_testreset1.pk1', sampling_interval=si)
a.record('spikes')
a.set(spike_times=[1])
#a.initialize(v=1)
pynn.run_until(1)

Figure(
    Panel(a.get_data().segments[-1].spiketrains)
)

plt.show()


pynn.reset()
#pynn.record(['spikes'], a, filename='output_testreset2.pk1', sampling_interval=si)
#a.initialize(v=1)
a.set(spike_times=[1])
pynn.run(30)
a.set(spike_times=[31])
pynn.run(30)
#a.initialize(v=1)
#pynn.run_until(10)
#a.initialize(v=1)
#pynn.run_until(10)

Figure(
    Panel(a.get_data().segments[-1].spiketrains)
)

plt.show()