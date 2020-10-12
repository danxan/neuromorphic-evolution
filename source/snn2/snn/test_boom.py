import pyNN.nest as pynn 
import matplotlib.pyplot as plt
from pyNN.utility.plotting import Figure, Panel

def plot(pop, filename):
    from pyNN.utility.plotting import Figure, Panel
    data = pop.get_data().segments[0]

    vm = data.filter(name='v')[0]
    #gsyn = data.filter(name='gsyn_exc')[0]

    Figure(
        Panel(vm, ylabel='Membrane potential (mV)', xlabel="Time (ms)", xticks=True, yticks=True),
        #Panel(gsyn, ylabel='Synaptic conductanse (uS)'),
        Panel(data.spiketrains, xlabel=filename),
        title=filename,
    ).save(filename+'.png')

    plt.show()

def panel_plot(pop, filename, pans=[]):
    from pyNN.utility.plotting import Figure, Panel
    data = pop.get_data().segments[0]

    vm = data.filter(name='v')[0]
    #gsyn = data.filter(name='gsyn_exc')[0]

    pans.append(Panel(vm, ylabel='Membrane potential (mV)', xlabel="Time (ms)", yticks=True))
    #Panel(gsyn, ylabel='Synaptic conductanse (uS)'),
    pans.append(Panel(data.spiketrains, xlabel=filename))

    return pans

pans = []

"""
# Setting v = 10
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

pynn.run(10)
v = 10
pynn.initialize(a, v=v)
pynn.run(40)

title = "1 default IF_cond_exp stimulated by setting v="+str(v)
#plot(a, title)

pans = panel_plot(a, title, pans)

# Using a stepcurrent
pynn.setup()

t = [10, 10.1]
amp = [1000,0]
source = pynn.StepCurrentSource(times=t, amplitudes=amp)
#source = pynn.NoisyCurrentSource(mean=15, stdev=1.0, start=10.0, stop=45.0, dt=1.0)
a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

source.inject_into(a)

pynn.run(50)
name = "injecting stepcurrent. "+str(amp)+ "nA at times "+str(t)+"."
#plot(a, name)

pans = panel_plot(a, name, pans)


# Using a SpikeSourceArray
pynn.setup()

poisson = pynn.Population(1, pynn.SpikeSourceArray(spike_times=[10.0]))
poisson.record('spikes')


a = pynn.Population(1, pynn.IF_cond_exp())
connector = pynn.AllToAllConnector()
p = pynn.Projection(poisson, a, connector)
a.set(tau_refrac=1)
w = 0.1
p.set(weight=w)

a.record('v')
a.record('spikes')

pynn.run(50)

name = "Using a SpikeSourceArray with a spike at 10.0ms, connected with a weight at"+str(w)+"."
#plot(a, name)

pans = panel_plot(a, name, pans)
"""


# Setting v = 10 in input, recording output
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')
b = pynn.Population(1, pynn.IF_cond_exp())
b.record('v')
b.record('spikes')

connector = pynn.AllToAllConnector()

p = pynn.Projection(a, b, connector)
w = 0.1 
p.set(weight=w)

pynn.run(10)
v = 10
pynn.initialize(a, v=v)
pynn.run(40)

name = "CHAIN: 1 input, 1 output. input stimulated by setting weight="+str(w)+" exh spike at 10ms.\n"

#plot(b, "1 input, 1 output. input stimulated by setting v="+str(v))

pans = panel_plot(b, name, pans)



# Using a stepcurrent
pynn.setup()

t = [10, 10.1]
amp = [1000,0]
source = pynn.StepCurrentSource(times=t, amplitudes=amp)
#source = pynn.NoisyCurrentSource(mean=15, stdev=1.0, start=10.0, stop=45.0, dt=1.0)
a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

b = pynn.Population(1, pynn.IF_cond_exp())
b.record('v')
b.record('spikes')

connector = pynn.AllToAllConnector()

p = pynn.Projection(a, b, connector)
w = 0.1 
p.set(weight=w)

source.inject_into(a)

pynn.run(50)
name = "CHAIN: 1 in 1 out. Injecting stepcurrent. "+str(amp)+ "nA at times "+str(t)+".\n"
#plot(a, name)

pans = panel_plot(b, name, pans)

# Two input manual stim

# Chain 2 in 1 out. Setting v = 10 in input, recording output
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

b = pynn.Population(1, pynn.IF_cond_exp())
b.record('v')
b.record('spikes')

o = pynn.Population(1, pynn.IF_cond_exp())
o.record('v')
o.record('spikes')

connector = pynn.AllToAllConnector()

p = pynn.Projection(a, o, connector)
wa = 0.1
p.set(weight=wa)

p = pynn.Projection(b, o, connector, receptor_type="inhibitory")
wb = 10
p.set(weight=wb)

pynn.run(10)
va = 10
pynn.initialize(a, v=va)
pynn.run(10)
vb = 10
pynn.initialize(b, v=vb)

pynn.run(40)

name = "CHAIN: 2 input, 1 output. input stimulated by weight="+str(wa)+" exh spike at 10ms and weight="+str(wb)+" inh spike at 20ms.\n"

pans = panel_plot(o, name, pans)

# 1 recurrent. Setting v = 10
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

b = pynn.Population(1, pynn.SpikeSourceArray(spike_times=list(range(0,50,5))))
b.record('spikes')

o = pynn.Population(1, pynn.IF_cond_exp())
o.record('v')
o.record('spikes')

connector = pynn.AllToAllConnector()

p = pynn.Projection(a, a, connector)
wa = 0.1
p.set(weight=wa)

p = pynn.Projection(b, o, connector, receptor_type="inhibitory")
wb = 0.1
p.set(weight=wb)

pynn.run(10)
va = 10
pynn.initialize(a, v=va)
pynn.run(40)

name = "Recurrent 1 neuron. input stimulated by weight="+str(wa)+" exh spike at 10ms\n"

pans = panel_plot(a, name, pans)

# 1 recurrent. Setting v = 10
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

b = pynn.Population(1, pynn.SpikeSourceArray(spike_times=list(range(0,50,5))))
b.record('spikes')

o = pynn.Population(1, pynn.IF_cond_exp())
o.record('v')
o.record('spikes')

connector = pynn.AllToAllConnector()

p = pynn.Projection(a, o, connector)
wa = 0.1
p.set(weight=wa)

p = pynn.Projection(b, o, connector, receptor_type="excitatory")
wb = 0.019
p.set(weight=wb)

pynn.run(10)
va = 10
pynn.initialize(a, v=va)
pynn.run(40)

name = "1 input at weight="+str(wa)+" exc spike at 10ms. 1 w="+str(wb)+"exc poisson generator input"

pans = panel_plot(o, name, pans)

# 1 generator input, 1 recurrent output
pynn.setup()

a = pynn.Population(1, pynn.IF_cond_exp())
a.record('v')
a.record('spikes')

b = pynn.Population(1, pynn.SpikeSourceArray(spike_times=list(range(0,50,5))))
b.record('spikes')

o = pynn.Population(1, pynn.IF_cond_exp())
o.record('v')
o.record('spikes')

connector = pynn.AllToAllConnector()

pa = pynn.Projection(a, o, connector)
wa = 0.1
pa.set(weight=wa)

pb = pynn.Projection(b, o, connector, receptor_type='inhibitory')
wb = 0.019
pb.set(weight=wb)

pynn.run(10)
va = 10
pynn.initialize(a, v=va)
pynn.run(40)

name = "1 input at weight="+str(wa)+" exc spike at 10ms. 1 w="+str(wb)+" inh spikesourcearray generator input"

pans = panel_plot(o, name, pans)

# 1 generator input, 1 recurrent output
pynn.setup()

stimuli = [1,0]
a = pynn.Population(1, pynn.SpikeSourceArray())
a.set(spike_times = [stimuli[1]])
a.record('spikes')
pynn.run(10)

pynn.run(50)

name = "1 poisson generator at rate=10.0"

from pyNN.utility.plotting import Figure, Panel
data = a.get_data().segments[0]
pans.append(Panel(data.spiketrains, xlabel="poissongenerator"))
Figure(*pans).save("singleneurons_and_chains")
plt.show()