import nest

for i in range(100000):
    a = nest.Create('iaf_cond_exp')
    b = nest.Create('iaf_cond_exp')
    nest.Connect(a,b)
    nest.GetConnections(a)


    print("The total number of Connect-calls is {} ".format(i))