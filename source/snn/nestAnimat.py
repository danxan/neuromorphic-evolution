from nest import *
from nestGenome import Genome

class Animat(object):
    def __init__(self, genome):
        self.ps = genome.ps # population size / neurons per node
        self.genome = genome
        self.ni = genome.ni # num input nodes
        self.nh = genome.nh # num hidden nodes
        self.no = genome.no # num output nodes

        self.iw = genome.iw
        self.hw = genome.hw
        self.ow = genome.ow

        self.sgs = []
        for i in range(self.ni):
            self.sgs.append(Create('spike_generator'))

        #self.sds = sds
        self.sds = []
        for o in range(self.no):
            self.sds.append(Create('spike_detector'))

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
            for j in range(self.nh):
                syn_dict = {'weight': self.iw[i][j]}
                Connect(self.sgs[i], self.hid[j], syn_spec=syn_dict)

        for i in range(self.nh):
            for j in range(self.nh):
                syn_dict = {'weight': self.hw[i][j]}
                Connect(self.hid[i], self.hid[j], syn_spec=syn_dict)

            self.conn['out'].append([])
            for j in range(self.no):
                syn_dict = {'weight': self.ow[i][j]}
                Connect(self.hid[i], self.out[j], syn_spec=syn_dict)

        for i in range(self.no):
            Connect(self.out[i], self.sds[i])

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


