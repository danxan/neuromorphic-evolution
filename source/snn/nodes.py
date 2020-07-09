import numpy as np

import pyNN.nest as pynn

class Unconnected_nodes(object):
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
            self.pop = pynn.Population(pop_size, pynn.IF_cond_exp, cellparams=self.neuron_parameters)
            # self.pop.record('v', 'spikes')
            self.populations.append(self.pop)
            self.asm += self.pop

        # self.asm.record('spikes')
            
class Fully_connected_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1):
        Unconnected_nodes.__init__(self, num_pop, pop_size)

        connector = pynn.AllToAllConnector()

        self.connections = { 'exc' : [],
                             'inh' : [] } 

        for pa in self.populations:
            for pb in self.populations:
                self.connections['exc'].append(pynn.Projection(pa, pb, connector, receptor_type='excitatory'))
                self.connections['inh'].append(pynn.Projection(pa, pb, connector, receptor_type='inhibitory'))

class Input_nodes(Unconnected_nodes):
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

if __name__ == '__main__':
    inp = Input_nodes(2,2)
    print(inp.populations)
    hid = Fully_connected_nodes()
    out = Output_nodes()