import numpy as np

import pyNN.nest as pynn

from neurons import *

class Animat(object):
    def __init__(self, input_n=1, hidden_n=3, output_n=1):
        inp = Input_neurons(num_pop=input_n)
        hid = Fully_connected_neurons(num_pop=hidden_n)
        out = Output_neurons(num_pop=output_n)

        connector = pynn.AllToAllConnector()

        input_connections = { 'exc' : [],
                              'inh' : [] } 

        output_connections = { 'exc' : [],
                               'inh' : [] } 

        for i in inp.populations:
            for h in hid.populations:
                input_connections['exc'].append(pynn.Projection(i, h, connector, receptor_type='excitatory'))
                input_connections['inh'].append(pynn.Projection(i, h, connector, receptor_type='inhibitory'))

        for h in hid.populations:
            for o in out.populations:
                output_connections['exc'].append(pynn.Projection(h, o, connector, receptor_type='excitatory'))
                output_connections['inh'].append(pynn.Projection(h, o, connector, receptor_type='inhibitory'))


if __name__ == '__main__':
    pynn.setup()
    animat = Animat()

    # hid = Fully_connected_neurons(num_pop=1)
    # animat2 = Animat()
    # animat3 = Animat()
    

