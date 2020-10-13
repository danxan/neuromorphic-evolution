import numpy as np

import pyNN.nest as pynn

class Unconnected_neurons(object):
    """
    A neuronal population consist of several objects of pynn.Population, collected in a pynn.assembly.
    The idea is that by representing each neuron with a cluster of neurons, spikes are ensured.
    """
    def __init__(self, num_pop, pop_size):
        self.neuron_parameters = {
        'cm': 0.2,
        'v_reset': -70.,
        'v_rest': -20.,
        'v_thresh': -15.,
        'e_rev_I': -100.,
        'e_rev_E': 60.,
        'tau_m': 7.,
        'tau_refrac': 4.,
        'tau_syn_E': 5.,
        'tau_syn_I': 5.,
        }

        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []
        self.asm = pynn.Assembly()
        for i in range(int(num_pop)):
            self.pop = pynn.Population(pop_size, pynn.IF_cond_exp, self.neuron_parameters)
            self.populations.append(self.pop)
            self.asm += self.pop
            self.pop.record('v')

        self.outgoing_connections = {   'exc' : [],
                                        'inh' : [] }


        self.incoming_connections = {   'exc' : [],
                                        'inh' : [] }


class Fully_connected_neurons(Unconnected_neurons):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_neurons.__init__(self, num_pop, pop_size)

        connector = pynn.AllToAllConnector()

        self.connections = []
        
        for pop_a, pop_b in zip(self.populations, self.populations[1:]):
            p = pynn.Projection(pop_a, pop_b, connector)
            self.incoming_connections['exc'].append(p)
            p = pynn.Projection(pop_b, pop_a, connector)
            self.incoming_connections['exc'].append(p)

class Input_neurons(Unconnected_neurons):
    # TODO: Write a method to accept input
    def __init__(self, num_pop=1, pop_size=1, exc_spike_times=100):
        Unconnected_neurons.__init__(self, num_pop, pop_size)

        connector = pynn.AllToAllConnector()

        self.connections = []

        # exc_spike_times is an int
        exc_spike_times = [
            exc_spike_times
        ]

        inh_spike_times = [
        ]

        self.input = []
        for i in range(num_pop):
            stim_exc = pynn.Population(self.pop_size, pynn.SpikeSourceArray, {
                'spike_times': exc_spike_times
            })
            self.input.append(stim_exc)

        for p_stim, p_in in zip(self.input, self.populations):
            p = pynn.Projection(p_stim, p_in, connector, receptor_type='excitatory')
            self.incoming_connections['exc'].append(p)
        

class Output_neurons(Unconnected_neurons):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_neurons.__init__(self, num_pop, pop_size)


def test_input_neurons():
    inp = Input_neurons(2,1)
        
def test_fully_connected_neurons():
    net = Fully_connected_neurons(4,1)

def test_output_neurons():
    out = Output_neurons(2,1)
