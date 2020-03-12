import numpy as np
import random

from animat import Animat

class Game:
    '''
    For now the block only has the size of one unit
    '''
    def __init__(self, game_width):
        self.game_width = game_width
        self.game_height = 3*game_width

        # The height is three times the width, to make the game possible.
        self.board = np.zeros((self.game_height, self.game_width))

    #def update_state(self):
    def _update_paddle(self, motor_out):
        # moves positon along axis of freedom, checks for boundaries
        if motor_out[0] > motor_out[1] and self.paddle_pos > 0:
            self.paddle_pos -= 1
        elif motor_out[0] < motor_out[1] and self.paddle_pos < self.game_width-1:
            self.paddle_pos += 1
        elif motor_out[0] < 1E-3 and motor_out[1] < 1E-3:
            if self.paddle_pos == 0:
                self.paddle_pos += 1
            elif self.paddle_pos == self.game_width-1:
                self.paddle_pos -= 1
            else:
                self.paddle_pos += random.randint(-1,1)
        '''
        if motor_out[0] > 0.5 and motor_out[1] > 0.5:
            self.paddle_pos = self.paddle_pos
        elif motor_out[1] > 0.5 and self.paddle_pos < self.game_width-1:
            self.paddle_pos += 1 # move right
        elif motor_out[0] > 0.5 and self.paddle_pos > 0:
            self.paddle_pos -= 1 # move left
        else:
            self.paddle_pos = self.paddle_pos
        '''

    def _update_block(self):
            self.board[self.block_pos[0]][self.block_pos[1]] = 0 # remove block from old pos

            # Update position
            self.block_pos[0] += 1 # move down
            if self.block_pos[1] > 0 and self.block_pos[1] < self.game_width-1:
                self.block_pos[1] = random.randint(self.block_pos[1] - 1, self.block_pos[1] + 1) # move left or right
            elif self.block_pos[1] == 0:
                self.block_pos[1] += 1 # move right
            elif self.block_pos[1] == self.game_width-1:
                self.block_pos[1] -= 1 # move left

            self.board[self.block_pos[0]][self.block_pos[1]] = 1 # set block in new pos

    def _print_game(self):
        vizboard = self.board
        vizboard[self.game_height-1, :] = 0
        vizboard[self.game_height-1][self.paddle_pos] = 1
        print(vizboard)


    def run(self, animat):
        '''
        It takes an animat player to play the game.
        '''
        #RESET GAME
        self.block_pos = [0, random.randint(0,self.game_width-1)] # postion in y,x / rows, cols
        self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = int(self.game_width/2) # along the x-axis / cols

        while self.block_pos[0] < self.game_height-1: # until the block is at the bottom of the board
            self._update_block()
            # The animat views the board with its two sensors. Has a view of one unit to the left or right.
            if self.block_pos[1] == self.paddle_pos:
                sens_in = [10,10]
                #print("sensed block on both sensors")
            elif self.block_pos[1] - 1 == self.paddle_pos:
                #print("sensed block on right sensor")
                sens_in = [0,10]
            elif self.block_pos[1] + 1 == self.paddle_pos:
                sens_in = [10,0]
                #print("sensed block on left sensor")
            else:
                sens_in = [-10,-10]
                #print("didnt sense block")

            motor_out = animat.activate(sens_in)
            self._update_paddle(motor_out)
            #self._print_game()

        if self.block_pos[0] == self.game_height-1:
            if self.paddle_pos-1 == self.block_pos[1] or self.paddle_pos == self.block_pos[1] or self.paddle_pos+1 == self.block_pos[1]: # paddle size is 3
                return 1 # point
            else:
                return 0

    def run_print(self, animat):
        '''
        It takes an animat player to play the game.
        '''

        #RESET GAME
        self.block_pos = [0, random.randint(0,self.game_width-1)] # postion in y,x / rows, cols
        self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = int(self.game_width/2) # along the x-axis / cols

        while self.block_pos[0] < self.game_height-1: # until the block is at the bottom of the board
            self._update_block()
            # The animat views the board with its two sensors. Has a view of one unit to the left or right.
            if self.block_pos[1] == self.paddle_pos:
                sens_in = [10,10]
                print("sensed block on both sensors")
            elif self.block_pos[1] - 1 == self.paddle_pos:
                print("sensed block on right sensor")
                sens_in = [0,10]
            elif self.block_pos[1] + 1 == self.paddle_pos:
                sens_in = [10,0]
                print("sensed block on left sensor")
            else:
                sens_in = [-10,-10]
                print("didnt sense block")

            #self._print_game()
            print(f'PADDLE POS IS {self.paddle_pos}')
            print(f'BLOCK POS is {self.block_pos[1]}')

            motor_out = animat.activate(sens_in)
            print(f'MOTOR OUT: {motor_out}')
            self._update_paddle(motor_out)



        if self.block_pos[0] == self.game_height-1:
            if self.paddle_pos-1 == self.block_pos[1] or self.paddle_pos == self.block_pos[1] or self.paddle_pos+1 == self.block_pos[1]: # paddle size is 3
                return 1 # point
            else:
                return 0

if __name__ == '__main__':
    num_nodes = 8
    animat = Animat(num_nodes)
    game_width = 8
    game = Game(game_width)
    game.run(animat)


