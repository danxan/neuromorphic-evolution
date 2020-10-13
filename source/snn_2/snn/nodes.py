import numpy as np

import pyNN.nest as pynn



class Unconnected_nodes(object):
    '''
    It's important to use labeling correctly. Input neurons need to be labeled as 'input'
    '''
    def __init__(self, num_pop=1, pop_size=1, cellclass=pynn.IF_cond_exp(), label='default'):
        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []
        self.asm = pynn.Assembly()
        
        for i in range(int(num_pop)):
            self.pop = pynn.Population(pop_size, cellclass, label=label)
            self.pop.record('spikes')
            self.populations.append(self.pop)
            self.asm += self.pop

        self.asm.record('spikes')

    def set_params(self, cellparams, debug=False):
        if type(cellparams) != type({}):
            print("Cellparams must be a dictionary.")
        else:
            keys = cellparams.keys()
            if len(keys) == 0:
                print("Cellparams is empty. Using default parametervalues.")
            elif self.populations[0].label != 'input':
                # TODO: Check celltype
                '''
                c = self.populations[0].celltype
                x = pynn.Population(1, pynn.IF_cond_exp()).celltype
                print(type(c))
                print(type(x))
                if type(c) == type(x):
                '''
                for p in self.populations:

                    if 'e_rev_E' in keys:
                        p.set(e_rev_E=cellparams['e_rev_E'])
                        if debug:
                            print('setting params')

                    if 'i_offset' in keys:
                        p.set(i_offset=cellparams['i_offset'])
                        if debug:
                            print('setting params')

                    if 'tau_syn_I' in keys:
                        p.set(tau_syn_I=cellparams['tau_syn_I'])
                        if debug:
                            print('setting params')

                    if 'v_reset' in keys:
                        p.set(v_reset=cellparams['v_reset'])
                        if debug:
                            print('setting params')

                    if 'e_rev_I' in keys:
                        p.set(e_rev_I=cellparams['e_rev_I'])
                        if debug:
                            print('setting params')

                    if 'tau_m' in keys:
                        p.set(tau_m=cellparams['tau_m'])
                        if debug:
                            print('setting params')

                    if 'cm' in keys:
                        p.set(cm=cellparams['cm'])
                        if debug:
                            print('setting params')

                    if 'v_tresh' in keys:
                        p.set(v_tresh=cellparams['v_tresh'])
                        if debug:
                            print('setting params')

                    if 'v_rest' in keys:
                        p.set(v_rest=cellparams['v_rest'])
                        if debug:
                            print('setting params')

                    if 'tau_syn_E' in keys:
                        p.set(tau_syn_E=cellparams['tau_syn_E'])
                        if debug:
                            print('setting params')

                    if 'tau_refrac' in keys:
                        p.set(tau_refrac=cellparams['tau_refrac'])
                        if debug:
                            print('setting params')
                            
                    '''
                    # if celltype is not IF_cond_exp
                    else: 
                        print('Using the cellparams parameter to set cellvalues only works of pynn.IF_cond_exp')
                        print('Will use the default parameters for the cell.')
                    '''
            
class Hidden_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1, label='hidden', cellparams={}):
        Unconnected_nodes.__init__(self, num_pop=num_pop, pop_size=pop_size)
        
        for p in self.populations:
            p.record('v')

class Fully_connected_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1, label='hidden'):
        Unconnected_nodes.__init__(self, num_pop=num_pop, pop_size=pop_size)

        connector = pynn.AllToAllConnector()

        self.connections = { 'exc' : [],
                             'inh' : [] } 

        for pa in self.populations:
            pa.record('v')
            pa.record('spikes')
            for pb in self.populations:
                self.connections['exc'].append(pynn.Projection(pa, pb, connector, receptor_type='excitatory'))
                self.connections['inh'].append(pynn.Projection(pa, pb, connector, receptor_type='inhibitory'))

class Input_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1, cellclass=pynn.SpikeSourceArray(), label='input'):
        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []
        self.asm = pynn.Assembly()
        
        for i in range(int(num_pop)):
            self.pop = pynn.Population(pop_size, cellclass=cellclass, label=label)
            self.pop.record('spikes')
            self.populations.append(self.pop)
            self.asm += self.pop

        self.asm.record('spikes')

class Output_nodes(Unconnected_nodes):
    def __init__(self, num_pop=1, pop_size=1, label='output'):
        Unconnected_nodes.__init__(self, num_pop=num_pop, pop_size=pop_size)
        for p in self.populations:
            p.record('v')

def test_input_nodes():
    inp = Input_nodes(2,1)
        
def test_fully_connected_nodes():
    net = Fully_connected_nodes(4,1)

def test_output_nodes():
    out = Output_nodes(2,1)

if __name__ == '__main__':
    inp = Input_nodes(num_pop=2, pop_size=2)
    print(inp.populations)
    hid = Fully_connected_nodes()
    out = Output_nodes()
    