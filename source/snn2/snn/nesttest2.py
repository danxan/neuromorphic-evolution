import nest 
import nest.voltage_trace
nest.ResetKernel()

spikegenerator1 = nest.Create('spike_generator')
nest.SetStatus(spikegenerator1, {'spike_times' : [10.0, 50.0]})

voltmeter = nest.Create('voltmeter')


n = nest.Create('iaf_cond_exp', 10000)
n2 = nest.Create('iaf_cond_exp', 10000)
# Her lager vi 100 000 connections i et call, og det krasjer ikke..
nest.Connect(n, n2, 'all_to_all', syn_spec={'weight':1e3})


nest.Connect(spikegenerator1, n, syn_spec={'weight':1e3})
nest.Connect(voltmeter, n2, syn_spec={'weight':1e3})

nest.Simulate(100.0)

nest.voltage_trace.from_device(voltmeter)
nest.voltage_trace.show()
