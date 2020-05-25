## SOME FUN TESTING
import sys
import os
import numpy as np
import scipy as sp
import time
import copy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from datetime import datetime

from game import Game


def org_seed(nodes):
  genome=list(np.random.randint(1,nodes+2,size=[1,nodes]))
  genome.extend(list(np.random.rand(9,nodes)))
  return genome

def update(a,x):
    a[x]=a[x]+input_func(copy.deepcopy(a[x-1]),np.random.randint(-1,2)) #move the block
    a[x-1]=y #flush previous line

def output_func(c,ann):
  #Function that controls paddle.
  idx=[i for i in range(len(c[0])) if c[-1,i]==1]
  dist = [0,0]
  for x in range(len(c)-1):
    idx2=[i for i in range(len(c[0])) if c[x,i]==1]
    if idx2:
      dist[0]=len(c)-x if idx[0] in idx2 else 0
      dist[1]=len(c)-x if idx[1] in idx2 else 0
      break
  d=ann.input_output(dist)
  return d

def plotit(a,score,i,n):
  plt.imshow(a,vmin=0,vmax=2) #plot
  plt.title("Score: {}, Round: {}, Net: {}".format(score, i, n)) #text update
  plt.pause(0.05) #plot stuff

def input_func(b,d):
  #Function for moving something one step.
  #b=input array, d=direction (0,1)
  b=list(b)
  if d>0: #move left
    return np.array([b[-1]]+b[0:-1])
  elif d<0: #move right
    return np.array(b[1:]+[b[0]])
  else:
    return np.array(b)

class ANN():
  def __init__(self,g,name):
    self.reset(g,name)

  def reset(self,g,name):
    self.genome=g
    self.thresh=self.genome[0]
    self.matrix=self.genome[1:6]
    self.input_nodes=self.genome[6:8]
    self.output_nodes=self.genome[8:10]
    self.temp=np.zeros([5])
    self.score=0
    self.name=name

  def input_output(self,i):

    for x in range(len(self.matrix)):
      self.temp=self.temp+(self.temp[x]*self.matrix[x])

    self.temp=self.temp+(self.input_nodes[0]*i[0])
    self.temp=self.temp+(self.input_nodes[1]*i[1])

    for x in range(len(self.temp)):
      self.temp[x] = 1 if self.temp[x] >= self.thresh[x] else 0

    o1 = self.output_nodes[0]*self.temp
    o2 = self.output_nodes[1]*self.temp

    if np.sum(o1) > np.sum(o2):
      return [1,0]

    elif np.sum(o1) < np.sum(o2):
      return [0,1]

    else:
      return [0,0]

  def scoring(self,score):
    self.score=self.score + score

  def getStuff(self,what):
    stuff= {"genome":self.genome,
            "thresh":self.thresh,
            "matrix":self.matrix,
            "temp":self.temp,
            "input_nodes":self.input_nodes,
            "output_nodes":self.output_nodes,
            "score":self.score,
            "name":self.name,
            }
    return stuff[what]

if __name__ == "__main__":
    '''
    genome_id = ["Bjarne","Ola","Kari",
             "Knut","Truls","Siri",
             "Lene","Mari","Olsen",
             "Baard","Sissel","Anne",
             "Henrik","Tassen","Lutte",
             "Dag","Frode","Lenin"]
    '''
    num_nets = 20
    genome_id = list(range(num_nets))

    increase=0.9 # if below 1, worse performing num_nets change more. If above, worse performing num_nets change less
    its = 128
    itses = 60000
    w,h=10,10
    l = h-1 #find length
    score=0
    sleep = 0.2
    scoreMean=[]
    scoreMax=[]
    sort=[]
    y = np.zeros([w])
    r=12 #mutation rate (1/r), follows formula gene+rand[-0.5,0.5]/r*inc^i, where i is rank. Best net doesn't change-
    a = np.zeros([h,w])
    nodes=5
    genome=org_seed(nodes)
    lg=len(genome)
    t2=time.time()
    List_ann=[ANN(genome,genome_id[i]) for i in range(num_nets)]
    # List_ann=[ANN(genome,i) for i in range(num_nets)]

    # redirect print
    local_dir = os.path.dirname(__file__)
    original = sys.stdout
    log_path = os.path.join(local_dir, 'quicktest.log')
    sys.stdout = open(log_path, 'w')



    for iteration in range(itses):
      print("Timestamp: {}".format(datetime.now()))
      ti=time.time()
      for ann in List_ann:
        game = Game(8)

        for i in range(its): #trials
          score = game.run(ann)
          ann.scoring(score)


      scores = [ann.getStuff("score") for ann in List_ann]
      sort = np.argsort(scores)[::-1]
      scoreMean.append(np.mean(scores))
      scoreMax.append(np.max(scores))

      if iteration % 10:
        print("Iteration: {0} of {1}, ANNs: {2}, Score, mean: {3:.2f}, max: {4:.2f} - took {5:.2f}s".format(iteration,itses,num_nets,scoreMean[-1],scoreMax[-1],time.time()-ti))

      List_ann[0].reset(List_ann[sort[0]].getStuff("genome"),genome_id[sort[0]]) # Best net doesn't change
      for i in range(1,num_nets):
        genome = List_ann[sort[i]].getStuff("genome") + ((np.random.rand(lg,nodes)-0.5)/r*increase**i)
        List_ann[i].reset(genome,genome_id[sort[i]])


    print("{} generations with {} ANNs took {}".format(itses,num_nets,time.time()-t2))
    plt.plot(scoreMean)
    log_path = os.path.join(local_dir, 'scoreMean.png')
    plt.savefig(log_path)
    plt.plot(scoreMax)
    log_path = os.path.join(local_dir, 'scoreMax.png')
    plt.savefig(log_path)

    # redirect print
    sys.stdout = original
