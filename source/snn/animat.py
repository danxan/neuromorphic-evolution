import numpy as np

import nest
import nest.voltage_trace

from nodes import *

class Animat(object):
    """
    The animat always has 2 sensory nodes and 2 motor nodes
    """
    def __init__(self, num_hid=4):
        nest.ResetKernel() # the simulation kernel is put back to its initial state

        self.num_inp = 2
        self.num_outp = 2
        self.inp = Input_nodes(num_pop=self.num_inp)
        self.hid = Fully_connected_nodes(num_pop=num_hid)
        self.out = Output_nodes(num_pop=self.num_outp)

        # connections going from spikegenerators to input nodes
        self.inc_inp_con = []
        # connections going from input nodes to hidden nodes
        self.outg_inp_con = []
        # connections going from hidden nodes to output nodes
        self.inc_outp_con = []
        # connections going from output nodes to voltmeter 
        self.outg_outp__con = []

        # setting up "input synapses" to a spike generator 
        self.spikegenerators = []
        for i in self.inp.populations:
            self.spikegenerators.append(nest.Create('spike_generator'))
            c = nest.Connect(self.spikegenerators[-1], i)
            self.inc_inp_con.append(c)

        # connecting all input nodes to all hidden nodes
        for i in self.inp.populations:
            for h in self.hid.populations:
                c = nest.Connect(i, h, "all_to_all")
                self.outg_inp_con.append(c)

        # connecting all hidden nodes to all output nodes
        for h in self.hid.populations:
            for o in self.out.populations:
                c = nest.Connect(h, o, "all_to_all")
                self.inc_outp_con.append(c)

        # setting up "voltmeters" to read output from output nodes
        self.voltmeters = []
        for o in self.out.populations:
            self.voltmeters.append(nest.Create('voltmeter'))
            c = nest.Connect(self.voltmeters[-1], o)
            self.outg_outp__con.append(c)
            
        sens_inp = [1,0]

        sens_inp = list(sens_inp)
        for i, inp in enumerate(self.inp.populations):
            if sens_inp[i] > 0:
                nest.SetStatus(self.spikegenerators[i], {'spike_times': [10.0]})

        nest.Simulate(100.0)

        # nest.voltage_trace.from_device(self.voltmeters[0])
        # nest.voltage_trace.show()
        # nest.voltage_trace.from_device(self.voltmeters[1])
        # nest.voltage_trace.show()

    def __call__(self, sens_inp=[0,0]):
        """
        Spikes are generated based on input
        """

        sens_inp = list(sens_inp)
        for i, inp in enumerate(self.inp.populations):
            if sens_inp[i] > 0:
                nest.SetStatus(self.spikegenerators[i], {'spike_times': [10.0]})

        nest.Simulate(100.0)

        nest.voltage_trace.from_device(self.voltmeters[0])
        nest.voltage_trace.show()
        nest.voltage_trace.from_device(self.voltmeters[1])
        nest.voltage_trace.show()

if __name__ == '__main__':
    animats = []
    animat = Animat()
    animats.append(animat)

    # animat([1,0])

    # hid = Fully_connected_nodes(num_pop=1)
    # animat2 = Animat()
    # animat3 = Animat()
    

