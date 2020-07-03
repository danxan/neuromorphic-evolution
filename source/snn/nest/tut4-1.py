import nest
import nest.topology as topp
import matplotlib.pyplot as plt
#my_layer_dict = {...}
#my_layer = topp.CreateLayer(my_layer_dict)

# on-grid
layer_dict_ex = {'extent' : [2.,2.], \
        'rows' : 10, \
        'columns' : 10, \
        'elements' : 'iaf_psc_alpha'}

# off-grid
import numpy as np
#grid with jitter
jit = 0.03
xs = np.arange(-0.5, .501, 0.1)
poss = [[x,y] for y in xs for x in xs]
poss = [[p[0]+np.random.uniform(-jit,jit), p[1]+np.random.uniform(-jit,jit)] for p in poss]
layer_dict_ex = {'positions': poss,\
        'extent' : [1.1, 1.1], \
        'elements' : 'iaf_psc_alpha'}

# advanced: composite layers
nest.CopyModel('iaf_psc_alpha', 'pyr')
nest.CopyModel('iaf_psc_alpha', 'inh', {'V_th': -52.})
comp_layer = topp.CreateLayer({'rows':5, 'columns':5, 'elements': ['pyr',4,'inh','poisson_generator','noise_generator']})

# Defining connection profiles

# Circular mask, gaussian kernel
conn1 = { 'connection_type': 'divergent',
        'mask': {'circular': {'radius': 0.75}},
        'kernel': {'gaussian': {'p_center':1., 'sigma':0.2}},
        'allow_autapses': False }

# Recatunglar mask, constant kernel, non-centered anchor
conn2 = { 'connection_type': 'divergent',
        'mask': {'rectangular': {'lower_left': [-0.5,-0.5], 'upper_right': [0.5,0.5]},
            'anchor': [0.5,0.5],
            },
        'kernel': 0.75,
        'allow_autapses': False
        }

# Donut mask, linear kernel that decreases with distance
# Commented out line would allow connection to target the pyr neurons (useful for composite layers)
conn3 = { 'connection_type': 'divergent',
        'mask': {'doughnut': {'inner_radius': 0.1, 'outer_radius': 0.95}},
        'kernel': {'linear': {'c': 1., 'a': -0.8}},
        #'targets' : 'pyr
        }

# Rectangular mask, fixed number of connections, gaussian weights, linear delays
conn4 = { 'connection_type': 'divergent',
        'mask': {'rectangular': {'lower_left': [-0.5,-0.5], 'upper_right':[0.5,0.5]}},
        'number_of_connections': 40,
        'weights': {'gaussian': {'p_center': 0, 'sigma': 0.25}},
        'delays': {'linear': {'c':0.1, 'a':0.2}},
        'allow_autapses': False
        }

ex_layer = topp.CreateLayer({'rows':5, 'columns':5, 'elements':'iaf_psc_alpha'})
in_layer = topp.CreateLayer({'rows':4, 'columns':4, 'elements':'iaf_psc_alpha'})
conn_dict_ex = {'connection_type': 'divergent', 'mask':{'circular': {'radius':0.5}}}
conn_dict_in = {'connection_type': 'divergent', 'mask':{'circular':{'radius':0.75}},'weights':-4.}
# And now we connect E -> I
topp.ConnectLayers(ex_layer, ex_layer, conn_dict_ex)
topp.ConnectLayers(in_layer, in_layer, conn_dict_in)
topp.ConnectLayers(in_layer, ex_layer, conn3)

nest.PrintNetwork(depth=1)
topp.PlotLayer(in_layer)
plt.show()
#topp.PlotTargets()
fig, ax = plt.subplots()
topp.PlotKernel(ax, topp.FindCenterElement(in_layer), mask=conn3['mask'], kern=conn2['kernel'])
plt.show()


