%%file exercise_01.py
import os
import numpy as np

import pyhmf as pynn
from pymarocco import PyMarocco
import Coordinate as C
from pysthal.command_line_util import init_logger

init_logger("ERROR", [('sthal', 'INFO')])

marocco = PyMarocco()
marocco.default_wafer = C.Wafer(30)
marocco.calib_path = "/wang/data/calibration/brainscales/wip"
marocco.defects.path = marocco.calib_path
marocco.backend = PyMarocco.Hardware
marocco.persist = "exercise_01.xml.gz"
marocco.checkl1locking = PyMarocco.CheckButIgnore
marocco.verification = PyMarocco.Skip
pynn.setup(marocco=marocco)

# extract requested FPGA from slurm license; expect only one
fpga = [C.FPGAOnWafer(int(lic.replace("W30F", ""))) for lic in os.environ["SLURM_HARDWARE_LICENSES"].split(',') if lic.startswith("W30F")][0]
# associated HICANNs with this FPGA
hicanns = [h for h in fpga.toHICANNOnWafer()]

print str(fpga)
print map(str, hicanns)

# natural units of neuroscience: nF = mV = ms = uS = 1
neuron_parameters = {
    'cm':        0.2, # nF
    'v_reset':   -30, # mV
    'v_rest':    -20, # mV
    'v_thresh':  -16, # mV
    'e_rev_I':   -40, # mV
    'e_rev_E':     0, # mV
    'tau_m':      10, # ms
    'tau_refrac':  1, # ms
    'tau_syn_E':   5, # ms
    'tau_syn_I':   5, # ms
}

# create a population of two neurons and record there spikes
population = pynn.Population(2, pynn.IF_cond_exp, neuron_parameters)
population.record()

# place population on first allocated HICANN
marocco.manual_placement.on_hicann(population, hicanns[0])

# for both neurons also record the analog membrane
neuron0 = pynn.PopulationView(population, [0])
neuron0.record_v()
neuron1 = pynn.PopulationView(population, [1])
neuron1.record_v()

# create two stimuli
#stimulus_0 = pynn.Population(1, pynn.SpikeSourceArray, {"spike_times" : [10,50,55,60,65,105,110,115,120,125]}) # in ms
#stimulus_1 = pynn.Population(1, pynn.SpikeSourceArray, {"spike_times" : [300,310,320,325,330,335,340,345]}) # in ms

# place one stimulus on a specific HICANN
#marocco.manual_placement.on_hicann(stimulus_1, hicanns[3])

# connect one stimulus
#pynn.Projection(stimulus_0, neuron0, pynn.AllToAllConnector(weights=0.005), target="excitatory") # weight in uS
#pynn.Projection(stimulus_0, neuron1, pynn.AllToAllConnector(weights=0.005), target="excitatory") # weight in uS

# connect the other
#pynn.Projection(stimulus_1, neuron0, pynn.AllToAllConnector(weights=0.1), target="excitatory") # weight in uS
#pynn.Projection(stimulus_1, neuron1, pynn.AllToAllConnector(weights=0.1), target="excitatory") # weight in uS

# start the experiment
print "starting experiment"
pynn.run(500) # in ms
pynn.end()

# store the results for neuron 0
print "storing results"
np.savetxt("spikes_nrn0.txt", neuron0.getSpikes())
np.savetxt("membrane_nrn0.txt", neuron0.get_v())

# store the results for neuron 1
np.savetxt("spikes_nrn1.txt", neuron1.getSpikes())
np.savetxt("membrane_nrn1.txt", neuron1.get_v())

print "done"

In [ ]:

# schedule the experiment for execution
!USER=s1ext_user1 srun -p experiment --wmod 30 --fpga {FPGA} singularity exec --app visionary-wafer /containers/stable/latest python exercise_01.py

In [ ]:

import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook
from IPython.display import FileLink, FileLinks

# load the analog traces
membrane_neuron0 = np.loadtxt("membrane_nrn0.txt")
membrane_neuron1 = np.loadtxt("membrane_nrn1.txt")

# load the spikes
spikes_neuron0 = np.loadtxt("spikes_nrn0.txt")
spikes_neuron1 = np.loadtxt("spikes_nrn1.txt")

# configure a plot
fig, axs = plt.subplots(2,1, sharex=True)

# plot the analog traces
ax = axs[0]
ax.plot(membrane_neuron0[:,1], membrane_neuron0[:,2], label="membrane neuron 0", color='C0');
ax.plot(membrane_neuron1[:,1], membrane_neuron1[:,2], label="membrane neuron 1", color='C1');
ax.set_ylabel("membrane [bio mV]")

# plot the spikes (might be empty)
ax = axs[1]
try:
    times_0, neuron_idxs_0 = spikes_neuron0[:,1], spikes_neuron0[:,0]
    ax.vlines(times_0, neuron_idxs_0-0.45, neuron_idxs_0 + 0.45, linewidth=1.5, label="spikes neuron 0", color='C0')
except IndexError:
    pass

try:
    times_1, neuron_idxs_1 = spikes_neuron1[:,1], spikes_neuron1[:,0]
    ax.vlines(times_1, neuron_idxs_1-0.45, neuron_idxs_1 + 0.45, linewidth=1.5, label="spikes neuron 1", color='C1')
except IndexError:
    pass
ax.set_ylabel("neuron index")
ax.set_yticks([0,1])
ax.set_xlabel("t [bio ms]")

#plt.legend(loc='upper left')
plt.show()

