import numpy as np

import pyNN.nest as pynn

from neurons import *

class Animat(object):
    def __init__(self, input_n=2, hidden_n=4, output_n=2):
        inp = Input_neurons(num_pop=input_n)
        hid = Fully_connected_neurons(num_pop=hidden_n)
        out = Output_neurons(num_pop=output_n)

        self.input_connections = []
        self.output_connections = []

        for i in inp.populations:
            for h in hid.populations:
                c = nest.Connect(i, h, "all_to_all")
                self.input_connections.append(c)

        for h in hid.populations:
            for o in out.populations:
                c = nest.Connect(h, o, "all_to_all")
                self.output_connections.append(c)


if __name__ == '__main__':
    for i in range(1000):
        animat = Animat()

    # hid = Fully_connected_neurons(num_pop=1)
    # animat2 = Animat()
    # animat3 = Animat()
    

