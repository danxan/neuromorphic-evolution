import nest
nest.ResetKernel()
n = 4
epop1 = nest.Create('iaf_psc_alpha',n)
epop2 = nest.Create('iaf_psc_alpha',n)
nest.Connect(epop1, epop2, {'rule':'all_to_all'})
conns = nest.GetConnections(epop1, target = epop2)
nest.GetStatus(conns, ["target", "weight"])
epop3 = nest.Create('iaf_psc_alpha',n)
epop4 = nest.Create('iaf_psc_alpha',n)
nest.Connect(epop3, epop4, {'rule':'all_to_all'})
conns = nest.GetConnections(epop3, target = epop4)
nest.GetStatus(conns, ["target", "weight"])

