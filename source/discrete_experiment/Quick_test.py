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
      return 1
    elif np.sum(o1) < np.sum(o2):
      return -1
    else:
      return 0

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
    names = ["Bjarne","Ola","Kari",
             "Knut","Truls","Siri",
             "Lene","Mari","Olsen",
             "Baard","Sissel","Anne",
             "Henrik","Tassen","Lutte",
             "Dag","Frode","Lenin"]

    increase=0.9 # if below 1, worse performing nets change more. If above, worse performing nets change less
    its = 12
    nets = 12
    itses = 36000
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
    List_ann=[ANN(genome,names[i]) for i in range(nets)]

    # redirect print
    local_dir = os.path.dirname(__file__)
    original = sys.stdout
    log_path = os.path.join(local_dir, 'quicktest.log')
    sys.stdout = open('quicktest.log', 'w')



    for iteration in range(itses):
      ti=time.time()
      for ann in List_ann:
        for i in range(its): #trials
          a = np.zeros([h,w]) #make game board
          p = np.random.rand() #rand number
          a[l,4:6]=1 #make paddle

          if p>0.5: #50/50 if short or long block, i.e. trial type
            a[0,4:5]=1
          else:
            a[0,4:6]=1

          for x in range(1,l+1):  #iterate over gamestates (falling block)
            #plotit(a,ann.getStuff("score"),i,ann.getStuff("name")) #plot
            d = output_func(a,ann) # here you send output and get a decision, d
            a[l] = input_func(a[l],d) # here you get input/move paddle (ANN will do this)
            update(a,x)

          #plotit(a,ann.getStuff("score"),i,ann.getStuff("name")) #plot
          u,c = np.unique(a[l],return_counts=True) #check values in bottom line (0=nothing, 1=paddle/block, 2=paddle+block)

          if p>0.5 and 2 in u: #if it didn't dodge it (2), lose a point
             ann.scoring(-1)
          elif p<0.5 and 2 not in u: #if it didn't catch any part of it (2), lose a point
             ann.scoring(-1)
          else:
             ann.scoring(1)
          #plt.close()

      scores = [ann.getStuff("score") for ann in List_ann]
      sort = np.argsort(scores)[::-1]
      scoreMean.append(np.mean(scores))
      scoreMax.append(np.max(scores))

      if iteration % 10:
        print("Iteration: {0} of {1}, ANNs: {2}, Score, mean: {3:.2f}, max: {4:.2f} - took {5:.2f}s".format(iteration,itses,nets,scoreMean[-1],scoreMax[-1],time.time()-ti))

      List_ann[0].reset(List_ann[sort[0]].getStuff("genome"),names[sort[0]]) # Best net doesn't change
      for i in range(1,nets):
        genome = List_ann[sort[i]].getStuff("genome") + ((np.random.rand(lg,nodes)-0.5)/r*increase**i)
        List_ann[i].reset(genome,names[sort[i]])


    print("{} generations with {} ANNs took {}".format(itses,nets,time.time()-t2))
    plt.plot(scoreMean)
    plt.savefig('scoreMean.png')
    plt.plot(scoreMax)
    plt.savefig('scoreMax.png')

    # redirect print
    sys.stdout = original
