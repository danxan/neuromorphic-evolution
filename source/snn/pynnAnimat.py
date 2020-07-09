import numpy as np
import matplotlib.pyplot as plt
from quantities import nA

import pyNN.nest as pynn

from nodes import *

class Animat(object):
    def __init__(self, input_n=2, hidden_n=4, output_n=2, pop_size=1):
        self.inp = Input_nodes(num_pop=input_n, pop_size=pop_size)
        print(self.inp.populations)
        self.hid = Fully_connected_nodes(num_pop=hidden_n, pop_size=pop_size)
        print(self.hid.populations)
        self.out = Output_nodes(num_pop=output_n, pop_size=pop_size)
        print(self.out.populations)

        connector = pynn.AllToAllConnector()

        self.input_connections = { 'exc' : [],
                                   'inh' : [] }

        self.output_connections = { 'exc' : [],
                                    'inh' : [] }

        for i in self.inp.populations:
            for h in self.hid.populations:
                self.input_connections['exc'].append(pynn.Projection(i, h, connector, receptor_type='excitatory'))
                self.input_connections['inh'].append(pynn.Projection(i, h, connector, receptor_type='inhibitory'))

        for h in self.hid.populations:
            for o in self.out.populations:
                self.output_connections['exc'].append(pynn.Projection(h, o, connector, receptor_type='excitatory'))
                self.output_connections['inh'].append(pynn.Projection(h, o, connector, receptor_type='inhibitory'))

    def setWeights(self):
        for c in self.input_connections['exc']:
            c.set(weight=1e3)
        for c in self.input_connections['inh']:
            c.set(weight=1e3)

        for c in self.output_connections['exc']:
            c.set(weight=1e3)
        for c in self.output_connections['inh']:
            c.set(weight=1e3)

        for c in self.hid.connections['exc']:
            c.set(weight=1e3)
        for c in self.hid.connections['inh']:
            c.set(weight=1e3)

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

    def __call__(self, stimuli=[0,0], plot=True):
        stimuli = list(stimuli)

        steps = pynn.DCSource(start=20.0, stop=80.0)
        
        for i in self.inp.populations:
            steps.inject_into(i)

        for o in self.out.populations:
            pynn.record(['v', 'spikes'], o, filename='output1_data.pkl', sampling_interval=1.0)

        for amp in (-0.2, -0.1, 0.0, 0.1, 0.2):
            steps.amplitude = amp
            pynn.run(100.0)
            pynn.reset(annotations={"amplitude": amp * nA})

        if plot:

            fig_settings = {
                'lines.linewidth': 0.5,
                'axes.linewidth': 0.5,
                'axes.labelsize': 'small',
                'legend.fontsize': 'small',
                'font.size': 8
            }

            plt.rcParams.update(fig_settings)
            plt.figure(1, figsize=(6,8))

            n_panels = 0
            for out in self.out.populations:
                data_out = out.get_data()
                n_panels += sum(a.shape[1] for a in data_out.segments[0].analogsignals) + 2

            # plot input
            for inp in self.inp.populations:
                spikes_in = inp.get_data()
                self.plot_spiketrains(spikes_in.segments[0])
                plt.subplot(n_panels, 1, 2)

            # plot output
            for out in self.out.populations:
                data_out = out.get_data()
                plt.subplot(n_panels, 1, 1)
                self.plot_spiketrains(data_out.segments[0])
                panel = 3
                for array in data_out.segments[0].analogsignals:
                    for i in range(array.shape[1]):
                        plt.subplot(n_panels, 1, panel)
                        self.plot_signal(array, i, colour='bg'[panel % 2])
                        panel += 1

            plt.xlabel('time (%s)' % array.times.units._dimensionality.string)
            plt.setp(plt.gca().get_xticklabels(), visible=True)

            plt.show()

        pynn.end()

if __name__ == '__main__':
    pynn.setup()
    animat = Animat(pop_size=1)
    animat.setWeights()
    animat()

