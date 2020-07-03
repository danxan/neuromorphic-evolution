import nest
# specifying the behaviour of devices
pg = nest.Create('poisson_generator')
nest.SetStatus(pg, {'start':100.0, 'stop':150.0})

nest.Simulate(1000.0)

# writing data to file
recdict = {"to_memory" : False, "to_file" : True, "label" : "epop_mp"}
mm1 = nest.Create("multimeter", params=recdict)

# resetting simulations

