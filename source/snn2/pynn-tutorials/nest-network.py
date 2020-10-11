from pyNN.nest import native_cell_type, Population, run, setup

setup()

ht_neuron = native_cell_type('iaf_cond_exp')
p1 = Population(10, ht_neuron())

p1.parameter_names




