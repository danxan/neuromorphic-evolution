import numpy as np

import nest

class Unconnected_neurons(object):
    """
    A neuronal population consist of several objects of pynn.Population, collected in a pynn.assembly.
    The idea is that by representing each neuron with a cluster of neurons, spikes are ensured.
    """
    def __init__(self, num_pop, pop_size):

        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []

        for i in range(self.num_pop):
            p = nest.Create('iaf_cond_exp', self.pop_size)
            self.populations.append(p)
            
class Fully_connected_neurons(Unconnected_neurons):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_neurons.__init__(self, num_pop, pop_size)

        self.connections = []
        
        for pop_a in self.populations:
            for pop_b in self.populations:
                c = nest.Connect(pop_a, pop_b, "all_to_all")
                self.connections = []

class Input_neurons(Unconnected_neurons):
    # TODO: Write a method to accept input
    def __init__(self, num_pop=1, pop_size=1, exc_spike_times=100):
        Unconnected_neurons.__init__(self, num_pop, pop_size)

class Output_neurons(Unconnected_neurons):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_neurons.__init__(self, num_pop, pop_size)

def test_input_neurons():
    inp = Input_neurons(2,1)
        
def test_fully_connected_neurons():
    net = Fully_connected_neurons(4,1)

def test_output_neurons():
    out = Output_neurons(2,1)
