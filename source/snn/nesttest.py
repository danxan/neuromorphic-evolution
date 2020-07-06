import nest
import nest.voltage_trace
nest.ResetKernel()

inp = []
for i in range(2):
    in1 = nest.Create('iaf_cond_exp', 1)
    inp.append(in1)

inputs = [10.0, 50.0]
sg = []
for i in range(2):
    spikegenerator1 = nest.Create('spike_generator')
    nest.SetStatus(spikegenerator1, {'spike_times' : [inputs[i]]})
    sg.append(spikegenerator1)

voltmeter = nest.Create('voltmeter')

for i in range(2):
    nest.Connect(sg[i], inp[i], 'all_to_all', syn_spec={'weight':1e3})

h = []
for i in range(4):
    h1 = nest.Create('iaf_cond_exp', 1)
    h.append(h1)

nest.Connect(sg[0], h[0], 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(sg[1], h[1], 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(sg[1], h[2], 'all_to_all', syn_spec={'weight':1e3})

# LEGG TIL CONNECT CALLES NEDENFOR FOR Å SE NÅR DET KRASJER... 
cons = []
cons.append(nest.Connect(inp[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[0], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[0], h[2], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[0], h[3], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[1], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[1], h[2], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(inp[1], h[3], 'all_to_all', syn_spec={'weight':1e3}))

cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[0], h[0], 'all_to_all', syn_spec={'weight':1e3}))
cons.append(nest.Connect(h[1], h[1], 'all_to_all', syn_spec={'weight':1e3}))

o1 = nest.Create('iaf_cond_exp', 1)
o2 = nest.Create('iaf_cond_exp', 1)
nest.Connect(h[0], o1, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[1], o1, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[2], o1, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[3], o1, 'all_to_all', syn_spec={'weight':1e3})

nest.Connect(h[0], o2, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[1], o2, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[2], o2, 'all_to_all', syn_spec={'weight':1e3})
nest.Connect(h[3], o2, 'all_to_all', syn_spec={'weight':1e3})

nest.Connect(voltmeter, o1)
nest.Connect(voltmeter, o2)
nest.Connect(voltmeter, h[0])
nest.Connect(voltmeter, h[1])
nest.Connect(voltmeter, h[2])
nest.Connect(voltmeter, h[3])

nest.Simulate(100.0)

nest.voltage_trace.from_device(voltmeter)
nest.voltage_trace.show()