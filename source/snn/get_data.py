from nest import *
from nestAnimat import Animat
from nestGenome import Genome

import sys
import pickle

filename = str(sys.argv[1])

log = None
with open(filename, 'rb') as f:
    log = pickle.load(f)

print("ScoreMax: \n{}".format(log['scoreMax']))
print("ScoreMean: \n{}".format(log['scoreMean']))
print("genome iw: \n{}\n\
    genome hw: \n{} \n\
    genome ow: \n{} \n".format(log['best_solution'].iw, log['best_solution'].hw, log['best_solution'].ow))



