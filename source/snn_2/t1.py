from nest import *
SetKernelStatus({"total_num_virtual_procs": 8,'local_num_threads':2})

sgs = [[]]
for i in range(1):
    for j in range(2):
        sgs[i].append(Create('spike_generator'))

spikes = [1,0]
for i in range(1):
    for j in range(2):
        if spikes[j] == 1:
            SetStatus(sgs[i][j], {'spike_times': [1.0]})
        else:
            SetStatus(sgs[i][j], {'spike_times': [100.0]})

sds = [[]]
for i in range(1):
    for j in range(2):
        sds[i].append(Create('spike_detector', 2))

n = Create('iaf_cond_exp', 5)
n2 = Create('iaf_cond_exp', 5)


iw = [1000.0,2000.0]
for i in range(1):
    for j in range(2):
        syn_dict = {'weight':iw[j]}
        Connect(sgs[i][j], n, syn_spec=syn_dict )
syn_dict = {'weight':1000.0}
Connect(n, n2, syn_spec=syn_dict)

Connect(n, sds[i][0])
Connect(n2, sds[i][1])


Prepare()

Run(1000)


print('SPIKE GENERATORS')
print(GetStatus(sgs[0][0]))
print('SPIKE DETECTORS')
for sd in sds:
    for i in range(2):
        print(GetStatus(sd[i]))

Cleanup()


