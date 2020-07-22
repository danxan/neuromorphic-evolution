import numpy as np
import matplotlib.pyplot as plt
from quantities import nA

import pyNN.nest as pynn

from nodes import *

class Animat(object):
    def __init__(self, input_n=2, hidden_n=4, output_n=2, pop_size=1):
        pynn.setup()
        self.total_runtime = 0

        self.num_inp = input_n
        self.num_hid = hidden_n
        self.num_out = output_n

        self.inp = Input_nodes(num_pop=input_n, pop_size=pop_size, cellclass=pynn.IF_cond_exp())
        print(self.inp.populations)
        self.hid = Hidden_nodes(num_pop=hidden_n, pop_size=pop_size)
        print(self.hid.populations)
        self.out = Output_nodes(num_pop=output_n, pop_size=pop_size)
        print(self.out.populations)

        connector = pynn.AllToAllConnector()

        self.input_connections = { 'exc' : [],
                                   'inh' : [] }

        self.hidden_connections = { 'exc' : [],
                                    'inh' : [] }

        self.output_connections = { 'exc' : [],
                                    'inh' : [] }

        for i in self.inp.populations:
            for h in self.hid.populations:
                self.input_connections['exc'].append(pynn.Projection(i, h, connector, receptor_type='excitatory'))
                self.input_connections['inh'].append(pynn.Projection(i, h, connector, receptor_type='inhibitory'))

        for h in self.hid.populations:
            for h in self.hid.populations:
                self.hidden_connections['exc'].append(pynn.Projection(h, h, connector, receptor_type='excitatory'))
                self.hidden_connections['inh'].append(pynn.Projection(h, h, connector, receptor_type='inhibitory'))

        for h in self.hid.populations:
            for o in self.out.populations:
                self.output_connections['exc'].append(pynn.Projection(h, o, connector, receptor_type='excitatory'))
                self.output_connections['inh'].append(pynn.Projection(h, o, connector, receptor_type='inhibitory'))

    def setWeights(self, genome):
        for i, c in enumerate(self.input_connections['exc']):
            c.set(weight=genome[:self.num_hid*self.num_inp][i])
        for i, c in enumerate(self.input_connections['inh']):
            c.set(weight=genome[self.num_hid*self.num_inp:(self.num_hid*self.num_inp+self.num_hid*self.num_inp)][i])

        for i, c in enumerate(self.hidden_connections['exc']):
            c.set(weight=genome[(self.num_hid*self.num_inp+self.num_hid*self.num_inp):(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid)][0])
        for i, c in enumerate(self.hidden_connections['inh']):
            c.set(weight=genome[(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid):(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid+self.num_hid*self.num_hid)][i])

        for i, c in enumerate(self.output_connections['exc']):
            c.set(weight=genome[(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid+self.num_hid*self.num_hid):(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid+self.num_hid*self.num_hid+self.num_hid*self.num_out)][i])
        for i, c in enumerate(self.output_connections['inh']):
            c.set(weight=genome[(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid+self.num_hid*self.num_hid+self.num_hid*self.num_out):(self.num_hid*self.num_inp+self.num_hid*self.num_inp+self.num_hid*self.num_hid+self.num_hid*self.num_hid+self.num_hid*self.num_out+self.num_hid*self.num_out)][i])


    def plot_spiketrains(self, segment):
        for spiketrain in segment.spiketrains:
            y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
            plt.plot(spiketrain, y, '.')
            plt.ylabel(segment.name)
            plt.setp(plt.gca().get_xticklabels(), visible=False)

    def plot_signal(self, signal, index, colour='b'):
        label = "Neuron %d" % signal.annotations['source_ids'][index]
        plt.plot(signal.times, signal[:, index], colour, label=label)
        plt.ylabel("%s (%s)" % (signal.name, signal.units._dimensionality.string))
        plt.setp(plt.gca().get_xticklabels(), visible=False)
        plt.legend()

    def plot(self):
        from pyNN.utility.plotting import Figure, Panel
        # PLOT OUTPUT
        o1 = self.out.populations[0].get_data().segments[0]

        vm1 = o1.filter(name='v')[0]

        o2 = self.out.populations[1].get_data().segments[0]

        vm2 = o2.filter(name='v')[0]

        Figure(
            Panel(vm1, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
            Panel(o1.spiketrains, xlabel='Output 1', xticks=True),
            Panel(vm2, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
            Panel(o2.spiketrains, xlabel='Output 2', xticks=True)
        ).save('simulation_results_outputnodes.png')

        plt.show()


    def run(self, stimuli=[0,0], start=0, runtime=30, plot=False):
        # TODO: This code only works for animats with 2 input nodes
        for i, node in enumerate(self.inp.populations):
            if stimuli[i] == 1:
                node.initialize(v=1)
                
        stop = start+runtime
        pynn.run_until(stop)

        if plot:
            from pyNN.utility.plotting import Figure, Panel
            # PLOT OUTPUT
            o1 = self.out.populations[0].get_data().segments[0]

            vm1 = o1.filter(name='v')[0]

            o2 = self.out.populations[1].get_data().segments[0]

            vm2 = o2.filter(name='v')[0]

            Figure(
                Panel(vm1, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
                Panel(o1.spiketrains, xlabel='Output 1', xticks=True),
                Panel(vm2, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
                Panel(o2.spiketrains, xlabel='Output 2', xticks=True)
            ).save('simulation_results_outputnodes.png')

            plt.show()

        return float(pynn.get_current_time())

if __name__ == '__main__':
    import random 
    pynn.setup()
    animat = Animat(pop_size=5, input_n=2, output_n=2, hidden_n=4)
    #genome = [random.randint(0,15) for i in range(2*(2*4+4*4+4*2))]
    genome = np.random.randint(0,15, 2*(2*4+4*4+4*2))
    for i, g in enumerate(genome):
        if np.random.random() > 0.3:
            genome[i] = 0
    genome[0] = 15
    genome[1] = 15

    genome = np.array([15,15,0,8,6,0,0,14,0,0,0,12,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,8,13,0,0,13,9,0,0,0,0,0,0,3,0,0,5,6,4,7,0,0,13,0,0,0,0,0,0,13,6,13,0,0,0,0,8,5,0])
    genome = genome
    print(genome)
    animat.setWeights(genome)
    animat.run(stimuli=[0,0])

