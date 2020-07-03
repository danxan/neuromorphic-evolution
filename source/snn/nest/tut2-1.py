import nest
import numpy

ndict = {'I_e': 200.0, 'tau_m': 20.0}
neuronpop = nest.Create('iaf_psc_alpha', 100, params=ndict)

neuronpop1 = nest.Create('iaf_psc_alpha', 100)
neuronpop2 = nest.Create('iaf_psc_alpha', 100)
neuronpop3 = nest.Create('iaf_psc_alpha', 100)

# set up a customized model in 2 steps
edict = {'I_e': 200.0, 'tau_m': 20.0}
nest.CopyModel('iaf_psc_alpha', 'exc_iaf_psc_alpha')
nest.SetDefaults('exc_iaf_psc_alpha', edict)

# set up a customized model in 1 step
idict = {'I_e': 300.0}
nest.CopyModel('iaf_psc_alpha', 'inh_iaf_psc_alpha', params=idict)

epop1 = nest.Create('exc_iaf_psc_alpha', 100)
epop2 = nest.Create('exc_iaf_psc_alpha', 100)
ipop1 = nest.Create('inh_iaf_psc_alpha', 30)
ipop2 = nest.Create('inh_iaf_psc_alpha', 30)

parameter_list = [{'I_e': 200.0, 'tau_m': 20.0}, {'I_e': 150.0, 'tau_m': 30.0}]
epop3 = nest.Create('exc_iaf_psc_alpha', 2, parameter_list)

Vth=-55.
Vrest=-70.
for neuron in epop1:
    nest.SetStatus([neuron], {'V_m': Vrest+(Vth-Vrest)*numpy.random.rand()})

# passing a list to set parameters
dVms =  [{"V_m": Vrest+(Vth-Vrest)*numpy.random.rand()} for x in epop1]
nest.SetStatus(epop1, dVms)

# setting one parameter
Vms = Vrest+(Vth-Vrest)*numpy.random.rand()
nest.SetStatus(epop1, 'V_m', Vms)
