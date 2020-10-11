import os 

import numpy as np
import random

import matplotlib.pyplot as plt

import pyNN.nest as pynn
from nest import Rank, SetKernelStatus
import neat #with pnifconn

from pynnAnimat import Animat

class Game:
    '''
    For now the block only has the size of one unit

    Game size is fixed for now. Disregard parameter.
    '''
    def __init__(self):
        self.game_cnt = 0
        self.direction = 0
        self.game_width = 8
        self.game_height = 16

        self.moves_cnt = 0

        # The height is three times the width, to make the game possible.
        self.board = np.zeros((self.game_height, self.game_width))


    #def update_state(self):
    def _update_paddle(self, decision):
        if decision != 0:
            self.moves_cnt += 1
        self.paddle_pos += decision
            

    def _update_block(self):
        #self.board[self.block_pos[0]][self.block_pos[1]] = 0 # remove block from old pos

        # Update position
        self.block_pos[0] += 1 # move down
        if self.block_pos[1] == self.game_width - 1:
            if self.direction == 1:
                self.block_pos[1] = 0
            elif self.direction == -1:
                self.block_pos[1] = self.game_width - 2
            elif self.direction == 0:
                self.block_pos[1] = self.block_pos[1]
        elif self.block_pos[1] == 0:
            if self.direction == 1:
                self.block_pos[1] = 1
            elif self.direction == -1:
                self.block_pos[1] = self.game_width -1
            elif self.direction == 0:
                self.block_pos[1] = self.block_pos[1]
        else:
            self.block_pos[1] += self.direction

        #self.board[self.block_pos[0]][self.block_pos[1]] = 1 # set block in new pos

        self.game_cnt += 1
        #print(f'(updated game count: {self.game_cnt}')

    def _print_game(self, sens_in=""):
        vizboard = np.zeros((self.game_height, self.game_width))
        if self.block_size == 1:
            vizboard[self.block_pos[0]][self.block_pos[1]] = 1
        if self.block_size == 3:
            vizboard[self.block_pos[0]][self.block_pos[1]:self.block_pos[1]+3] = 1
        vizboard[self.game_height-1][self.paddle_pos-1:self.paddle_pos+2] = 1

        print(vizboard)

    def translate_spikes(self, animat):
        '''
        Translate spiketrains from each output node into decision.
        Asserting 2 output nodes.
        Assuming each node is AllToAllConnected.

        Return: 
            decision in range (-1,1]
        '''
        assert animat.num_out == 2, "This method only accept two output nodes."
        decision = 0 
        spiketrain_length = []
        last_spikes = []
        #print("INPUT SPIKES")
        #print(animat.inp.populations[0].get_data().segments[0].spiketrains[0])
        for o in animat.out.populations:
            # SpikeTrain is a class from the neo package
            # getting the spiketrain from the first neuron of the population, 
            # assuming the populations are alltoallconnected
            spiketrains = o.get_data(gather=False).segments[0].spiketrains[0]
            #print("\nspiketrains:")
            #print(spiketrains)

            # Get spikes from last run only
            # The elements of SpikeTrain is objects of the Quantity class from the quantities package
            for t in spiketrains:
                t = float(t)
                if t > self.prev_stop:
                    last_spikes.append(t)

            #print("\nlast spikes:")
            #print(last_spikes)

            spiketrain_length.append(len(last_spikes))
        
        if spiketrain_length[0] > spiketrain_length[1]:
            decision = 1
        elif spiketrain_length[0] < spiketrain_length[1]:
            decision = -1
        
        return decision

    def run(self, genome, params=None, config=None, fps=60, d=False, plot=False):
        '''
        It takes an animat player to play the game.
        This version takes a pynnAnimat.
        '''
        #RESET GAME
        pynn.setup()

        if config:
            animat = neat.pnifconn.pnifcoNN.create(genome, config)

        elif params:
            ps = genome.pop_size
            ni = genome.num_inp
            nh = genome.num_hid
            no = genome.num_out
            animat = Animat(pop_size=ps, input_n=ni, hidden_n=nh, output_n=no)
            animat.inp.set_params(params)
            animat.hid.set_params(params)
            animat.out.set_params(params)
            genes = genome.genes
            animat.setWeights(genes)

        else:
            ps = genome.pop_size
            ni = genome.num_inp
            nh = genome.num_hid
            no = genome.num_out
            animat = Animat(pop_size=ps, input_n=ni, hidden_n=nh, output_n=no)
            genes = genome.genes
            animat.setWeights(genes)

        

        self.total_runtime = 0
        self.prev_stop = 0
        self.runtime = int(1000/fps)

        self.block_pos = [0,0]#[0, random.randint(0,self.game_width-1)] # postion in y,x / rows, cols
        # Set block size with a "coin flip"
        p = random.randint(0,1)
        if p == 1:
            self.block_size = 1
        else:
            self.block_size = 3
        #self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = 0#random.randint(0, self.game_width-1)# along the x-axis / cols
        self.direction = random.randint(-1,1)

        score = -1 # return value
        w = self.game_width # to make code readable

        while self.block_pos[0] < self.game_height-1: # until the block is at the bottom of the board
            
            self._update_block()

            w = self.game_width

            start = self.block_pos[1]
            end = start+self.block_size
            left_sens = self.paddle_pos-1
            right_sens = self.paddle_pos+1

            sens_in = [0,0]

            for i in range(start, end, 1):
                if (i%w) == left_sens%w:
                    sens_in[0] = 1 
                if (i%w) == right_sens%w:
                    sens_in[1] = 1 

            if d == True:
                self._print_game()
                print(sens_in)
            
            self.prev_stop = self.total_runtime
            self.total_runtime = animat.run(stimuli=sens_in, start=self.prev_stop, runtime=self.runtime)

            decision = self.translate_spikes(animat)

            self._update_paddle(decision)

            # check for crash to give score for tracking
            start = self.block_pos[1]
            end = start+self.block_size
            crash = False
            paddle_start = self.paddle_pos-1
            paddle_end = self.paddle_pos+1

            for i in range(start, end, 1):
                for j in range(paddle_start, paddle_end+1, 1):
                    crash = (i%w) == (j%w)
                    if crash: break
                if crash: break

            '''
            if crash:
                if self.block_size == 1:
                    score += self.block_pos[0] # score increases when the distance to the paddle decreases
            else:
                if self.block_size == 3:
                    score += self.block_pos[0] # score increases when the distance to the paddle decreases
            '''

            if d == True:
                self._print_game()
                print(sens_in)
        
        # after while loop
        pynn.end()

        # at the last time-step
        if self.block_pos[0] == self.game_height-1:
            # TESTING "KILLING LASER"
            if self.moves_cnt == 0:
                return 0

            # check for crash
            start = self.block_pos[1]
            end = start+self.block_size
            crash = False
            paddle_start = self.paddle_pos-1
            paddle_end = self.paddle_pos+1

            for i in range(start, end, 1):
                for j in range(paddle_start, paddle_end+1, 1):
                    crash = (i%w) == (j%w)
                    if crash: break
                if crash: break

            if crash:
                if self.block_size == 1:
                    score = 1
            else:
                if self.block_size == 3:
                    score = 1

            if d == True:
                print(score)

            if plot:
                animat.plot()

            return score

if __name__ == '__main__':
    game = Game()
    animat = neat.pnifconn.pnifcoNN.create(genome, config)



