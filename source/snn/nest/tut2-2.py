# Generating populationms of neurons with deterministic connections
import pylab
import nest
pop1 = nest.Create('iaf_psc_alpha', 10)
nest.SetStatus(pop1, {'I_e': 376.0})
pop2 = nest.Create('iaf_psc_alpha', 10)
multimeter = nest.Create('multimeter', 10)
nest.SetStatus(multimeter, {'withtime':True, 'record_from':['V_m']})

# all to all
nest.Connect(pop1, pop2, syn_spec={'weight':20.0})
# one to one
nest.Connect(pop1, pop2, 'one_to_one', syn_spec={'weight':20.0, 'delay':1.0})

nest.Connect(multimeter, pop2)

