import pyNN.nest as pynn 
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

pynn.setup()

a = pynn.Population(5, pynn.SpikeSourceArray(spike_times=[10]))
b = pynn.Population(5, pynn.IF_cond_exp())
c = pynn.Population(5, pynn.IF_cond_exp())
d = pynn.Population(5, pynn.IF_cond_exp())
e = pynn.Population(5, pynn.IF_cond_exp())
o = pynn.Population(5, pynn.IF_cond_exp())
o.record('spikes')
a.record('spikes')
o.set(tau_syn_E=0.017)
o.set(tau_syn_I=0.01)
o.set(tau_m=0.10)
o.set(e_rev_E=-40)
o.set(e_rev_I=0)
o.set(v_reset=-90)
connector = pynn.AllToAllConnector()

w = 15 

pa = pynn.Projection(a, o, connector)
pb = pynn.Projection(b, o, connector)
pc = pynn.Projection(c, o, connector)
pd = pynn.Projection(d, o, connector)
pe = pynn.Projection(e, o, connector)
po = pynn.Projection(o, o, connector)

pai = pynn.Projection(a, o, connector, receptor_type='inhibitory')
pbi = pynn.Projection(b, o, connector, receptor_type='inhibitory')
pci = pynn.Projection(c, o, connector, receptor_type='inhibitory')
pdi = pynn.Projection(d, o, connector, receptor_type='inhibitory')
pei = pynn.Projection(e, o, connector, receptor_type='inhibitory')
poi = pynn.Projection(o, o, connector, receptor_type='inhibitory')

pa.set(weight=8)
pb.set(weight=8)
pc.set(weight=8)
pd.set(weight=8)
pe.set(weight=8)
po.set(weight=8)

pai.set(weight=8)
pbi.set(weight=8)
pci.set(weight=8)
pdi.set(weight=8)
pei.set(weight=8)
poi.set(weight=8)

pynn.run_until(10)
pynn.run_until(12)
b.initialize(v=1)
c.initialize(v=1)
d.initialize(v=1)
time = pynn.get_current_time()
stop = time+20
pynn.run_until(stop)
a.set(spike_times=[20])
time = pynn.get_current_time()
stop = time+20
pynn.run_until(stop)


do = o.get_data().segments[0]
print(len(do.spiketrains[0]))
da = a.get_data().segments[0]
print(len(da.spiketrains[0]))

Figure(
    Panel(do.spiketrains),
    Panel(da.spiketrains)
)


plt.show(20)