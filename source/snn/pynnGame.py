import numpy as np
import random

import pyNN.nest as pynn

import pynnAnimat

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
            spiketrains = o.get_data().segments[0].spiketrains[0]
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

    def run(self, animat, fps=60, d=False):
        '''
        It takes an animat player to play the game.
        This version takes a pynnAnimat.
        '''
        #RESET GAME
        pynn.reset()

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
            
            #sens_in = [1,1]
            self.prev_stop = self.total_runtime
            self.total_runtime = animat.run(stimuli=sens_in, start=self.prev_stop, runtime=self.runtime, plot=False)

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

            print(score)
            return score

if __name__ == '__main__':
    game = Game()
    animat = pynnAnimat.Animat(pop_size=5)
    genome = np.array([15,15,0,8,6,0,0,14,0,0,0,12,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,8,13,0,0,13,9,0,0,0,0,0,0,3,0,0,5,6,4,7,0,0,13,0,0,0,0,0,0,13,6,13,0,0,0,0,8,5,0])
    genome = np.random.randint(0,15, 2*(2*4+4*4+4*2))
    for i, g in enumerate(genome):
        if np.random.random() > 0.9:
            genome[i] = 0
    genome[0] = 15
    genome[1] = 15
    print(genome)
    animat.setWeights(genome)
    game.run(animat, fps=30, d=False)            
    animat.plot()


