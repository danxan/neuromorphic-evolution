import nest

N=int(530000/3.5)

A=nest.Create('iaf_cond_exp',N)
B=nest.Create('iaf_cond_exp',1)

nest.Connect(A,B,'all_to_all')
print("CONNECTED")

nest.GetConnections(A,B)
print("GOT CONNECTIONS")