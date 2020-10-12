import pyNN.nest as pynn

from pynnGame import Game
from genome import SgaGenome

from nest import NumProcesses, Rank
import nest

T = NumProcesses()
id = Rank()

pynn.setup() 
a = pynn.Population(1, pynn.SpikeSourceArray(spike_times=[1]))
a.record('spikes')

pynn.run(10)

a.get_data(gather=False).segments[0].spiketrains

pynn.end()