import pylab
import nest
neuron1 = nest.Create('iaf_psc_alpha')
nest.SetStatus(neuron1, {'I_e': 376.0})
neuron2 = nest.Create('iaf_psc_alpha')
multimeter = nest.Create('multimeter')
nest.SetStatus(multimeter, {'withtime':True, 'record_from':['V_m']})

# Connect neuron1 to neuron2

nest.Connect(neuron1, neuron2, syn_spec = {'weight': 20.0})
nest.Connect(multimeter, neuron2)

nest.Simulate(1000.0)

pylab.figure(2)
dmm = nest.GetStatus(multimeter)[0]
Vms1 = dmm["events"]["V_m"][::2] # start at index 0: till the end: each second entry
ts1 = dmm["events"]["times"][::2]
pylab.plot(ts1, Vms1)
Vms2 = dmm["events"]["V_m"][1::2] # start at index 1: till the end: each second entry
ts2 = dmm["events"]["times"][1::2]
pylab.plot(ts2, Vms2)
pylab.show()
