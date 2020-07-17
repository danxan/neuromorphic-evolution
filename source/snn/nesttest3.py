import nest
import nest.voltage_trace

sg = nest.Create('spike_generator', 2)
print(sg)

inp = nest.Create('iaf_cond_exp', 2)
print(inp)

hid = nest.Create('iaf_cond_exp', 4)
print(hid)

out = nest.Create('iaf_cond_exp', 2)
print(out)

vm = nest.Create('voltmeter')

for s, i in zip(sg, inp):
    nest.Connect(sg, inp)

nest.Connect(inp, hid)

nest.Connect(hid, hid)

nest.Connect(hid, out)

for o in out:
    o = [o]
    nest.Connect(vm, o)

