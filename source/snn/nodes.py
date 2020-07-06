import numpy as np

import nest

class Unconnected_nodes(object):
    def __init__(self, num_pop, pop_size):
        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []

        for i in range(self.num_pop):
            p = nest.Create('iaf_cond_exp', self.pop_size)
            self.populations.append(p)
            
class Fully_connected_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_nodes.__init__(self, num_pop, pop_size)

        self.connections = []
        
        for pop_a in self.populations:
            for pop_b in self.populations:
                c = nest.Connect(pop_a, pop_b, "all_to_all")
                self.connections = []

class Input_nodes(Unconnected_nodes):
    # TODO: Write a method to accept input
    def __init__(self, num_pop=1, pop_size=1, exc_spike_times=100):
        Unconnected_nodes.__init__(self, num_pop, pop_size)

class Output_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_nodes.__init__(self, num_pop, pop_size)

def test_input_nodes():
    inp = Input_nodes(2,1)
        
def test_fully_connected_nodes():
    net = Fully_connected_nodes(4,1)

def test_output_nodes():
    out = Output_nodes(2,1)
