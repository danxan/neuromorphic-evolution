import nest

N = int(530000/2)

A = nest.Create('iaf_cond_exp', N)
B = nest.Create('iaf_cond_exp', N)

nest.Connect(A,B)
nest.Simulate(100.0)