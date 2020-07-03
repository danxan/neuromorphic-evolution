import nest

ndict = {'I_e': 199.0, 'tau_m': 20.0}
neuronpop = nest.Create('iaf_psc_alpha', 100, params=ndict)

neuronpop1 = nest.Create('iaf_psc_alpha', 100)
neuronpop2 = nest.Create('iaf_psc_alpha', 100)
neuronpop3 = nest.Create('iaf_psc_alpha', 100)

# set up a customized model in 1 steps
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

# Connecting networks with synapses
nest.SetDefaults('stdp_synapse', {'tau_plus': 15.0})

nest.CopyModel('stdp_synapse', 'layer1_stdp_synapse', {'Wmax': 90.0})
# STDP synapses
nest.Create('iaf_psc_alpha', params={'tau_minus': 30.0})

# Connecting with synapse models
K = 12
conn_dict = {'rule': 'fixed_indegree', 'indegree': K}
syn_dict = {'model': 'stdp_synapse', 'alpha': 1.0}
#nest.Connect(epop1, epop2, conn_dict, syn_dict)

# Distributing synapse parameters
alpha_min = 0.1
alpha_max = 2.
w_min = 0.5
w_max = 5.

syn_dict = {'model': 'stdp_synapse', 'alpha': {'distribution': 'uniform', 'low': alpha_min, 'high': alpha_max}, 'weight': {'distribution': 'uniform', 'low': w_min, 'high': w_max}, 'delay': 1.0}
#nest.Connect(epop1, epop2, conn_dict, syn_dict)
nest.Connect(epop1, epop2, 'all_to_all', syn_dict)
#
# Querying the synapses
print('epop1:')
print(nest.GetConnections(epop1))

print('epop2:')
print(nest.GetConnections(target=epop2))

print('given synapse: stdp synapse')
print(nest.GetConnections(synapse_model='stdp_synapse'))
# examine one paraemter target
conns = nest.GetConnections(epop1, synapse_model='stdp_synapse')
targets = nest.GetStatus(conns, 'target')

# examine several parameters
conns = nest.GetConnections(epop1, synapse_model='stdp_synapse')
conn_vals = nest.GetStatus(conns, ['target', 'weight'])



