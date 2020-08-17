from nest import *
from nestGenome import Genome

class Animat(object):
    def __init__(self, sgs, sds, genome):
        self.ps = genome.ps # population size / neurons per node
        self.ni = genome.ni # num input nodes
        self.nh = genome.nh # num hidden nodes
        self.no = genome.no # num output nodes

        self.iw = genome.iw
        self.hw = genome.hw
        self.ow = genome.ow

        self.sgs = sgs
        self.sds = sds

        self.conn = { "in": [],
                 "out": [],
                 "hid": []}

        self.hid = []
        for i in range(self.nh):
            self.hid.append(Create('iaf_cond_exp', self.ps))

        self.out = []
        for i in range(self.no):
            self.out.append(Create('iaf_cond_exp', self.ps))

        for i in range(self.ni):
            self.conn['in'].append([])
            for j in range(self.nh):
                syn_dict = {'weight': self.iw[i][j]}
                Connect(self.sgs[i], self.hid[j], syn_spec=syn_dict)
                #print(self.conn['in'][i].append(GetConnections(sgs[i],self.hid[j])))

        for i in range(self.nh):
            self.conn['hid'].append([])
            for j in range(self.nh):
                syn_dict = {'weight': self.hw[i][j]}
                Connect(self.hid[i], self.hid[j], syn_spec=syn_dict)
                #self.conn['hid'][i].append(GetConnections(self.hid[i],self.hid[j]))

            self.conn['out'].append([])
            for j in range(self.no):
                syn_dict = {'weight': self.ow[i][j]}
                Connect(self.hid[i], self.out[j], syn_spec=syn_dict)
                #self.conn['out'][i].append(GetConnections(self.hid[i],self.out[j]))

        for i in range(self.no):
            Connect(self.out[i], sds[i])

    def set_weights(self, genome):
        self.iw = genome.iw
        self.hw = genome.hw
        self.ow = genome.ow

        for i in range(self.ni):
            for j in range(self.nh):
                conn = GetConnections(self.sgs[i], self.hid[j])
                SetStatus(conn, params='weight', val=self.iw[i][j])

        for i in range(self.nh):
            for j in range(self.nh):
                conn = GetConnections(self.hid[i], self.hid[j])
                SetStatus(conn, params='weight', val=self.hw[i][j])

            for j in range(self.no):
                conn = GetConnections(self.hid[i], self.out[j])
                SetStatus(conn, {'weight':self.ow[i][j]})


