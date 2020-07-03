# Tutorial 1.2 from NEST.. How to simulate and probe a neuron
from sklearn.svm import LinearSVC
from scipy.special import erf
import pylab
import nest

neuron = nest.Create('iaf_psc_alpha')
# Creating a second neuron and reading data from both with the same multimeter.
neuron2 = nest.Create('iaf_psc_alpha')
nest.SetStatus(neuron2, {'I_e': 370.0})

nest.GetStatus(neuron)


nest.GetStatus(neuron, "I_e")
nest.GetStatus(neuron, ["V_reset", "V_th"])
nest.SetStatus(neuron, {"I_e": 376.0})
#nest.SetStatus(neuron, {"I_e": 376})


multimeter = nest.Create("multimeter")
nest.SetStatus(multimeter, {"withtime":True, "record_from":["V_m"]})
spikedetector = nest.Create("spike_detector",
                params={"withgid": True, "withtime": True})

nest.Connect(multimeter, neuron)
# connecting the same multimeter to the second neuron
nest.Connect(multimeter, neuron2)
nest.Connect(neuron, spikedetector)
nest.Simulate(1000.0)


dmm = nest.GetStatus(multimeter)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]

pylab.figure(1)
pylab.plot(ts, Vms)

# How to slice the data properly. The data is interlaced...
pylab.figure(2)
dmm = nest.GetStatus(multimeter)[0]
Vms1 = dmm["events"]["V_m"][::2] # start at index 0: till the end: each second entry
ts1 = dmm["events"]["times"][::2]
pylab.plot(ts1, Vms1)
Vms2 = dmm["events"]["V_m"][1::2] # start at index 1: till the end: each second entry
ts2 = dmm["events"]["times"][1::2]
pylab.plot(ts2, Vms2)

dSD = nest.GetStatus(spikedetector,keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
pylab.figure(2)
pylab.plot(ts, evs, ".")
pylab.show()




# writing data to file
recdict = {"to_memory" : False, "to_file" : True, "label" : "epop_mp"}
mm1 = nest.Create("multimeter", params=recdict)

