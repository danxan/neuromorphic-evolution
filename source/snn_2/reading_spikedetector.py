import nest

a = nest.Create('iaf_cond_exp', 1)

sg = nest.Create('spike_generator')
sd = nest.Create('spike_detector')

nest.Connect(sg, a, syn_spec={'weight': 1000})
nest.Connect(a, sd)



nest.SetStatus(sg, {'spike_times': [1.0]})

nest.Simulate(100)

res = nest.GetStatus(sd)[0]['events']['times'][0]
print(res)
nest.SetStatus(sd, {'n_events': 0})
res = nest.GetStatus(sd)[0]['events']['times'][0]
print(res)
