import numpy as np
import random

from animat import Animat

class Game:
    '''
    For now the block only has the size of one unit
    '''
    def __init__(self):
        game_size = 8
        self.board = np.zeros((game_size, game_size))
        # init block
        self.block_pos = [0,0] # postion in y,x / rows, cols
        self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = 0 # along the x-axis / cols
        self.game_size = game_size

    #def update_state(self):
    def _update_paddle(self, motor_out):
        # moves positon along axis of freedom, checks for boundaries
        if motor_out[0] > 0 and self.paddle_pos < self.game_size-1:
            self.paddle_pos += 1 # move right
        elif motor_out[0] < 0 and self.paddle_pos > 0  :
            self.paddle_pos -= 1 # move left

    def _update_block(self):
            self.board[self.block_pos[0]][self.block_pos[1]] = 0 # remove block from old pos

            # Update position
            self.block_pos[0] += 1 # move down
            if self.block_pos[1] > 0 and self.block_pos[1] < self.game_size-1:
                self.block_pos[1] = random.randint(self.block_pos[1] - 1, self.block_pos[1] + 1) # move left or right
            elif self.block_pos[1] == 0:
                self.block_pos[1] += 1 # move right
            elif self.block_pos[1] == self.game_size-1:
                self.block_pos[1] -= 1 # move left

            self.board[self.block_pos[0]][self.block_pos[1]] = 1 # set block in new pos

    def _print_game(self):
        vizboard = self.board
        vizboard[self.game_size-1, 0:self.game_size-1] = 0
        vizboard[self.game_size-1][self.paddle_pos] = 1
        print(vizboard)


    def run(self, animat):
        '''
        It takes an animat player to play the game.
        '''
        while self.block_pos[0] < self.game_size-1: # until the block is at the bottom of the board
            # The animat views the board with its two sensors. Has a view of one unit to the left or right.
            if self.block_pos[1] - 1 == self.paddle_pos:
                print("sensed block on right sensor")
                sens_in = [0,1]
            elif self.block_pos[1] + 1 == self.paddle_pos:
                sens_in = [1,0]
                print("sensed block on left sensor")
            elif self.block_pos[1] == self.paddle_pos:
                sens_in = [1,1]
                print("sensed block on both sensors")
            else:
                sens_in = np.zeros(2)
                print("didnt sense block")

            motor_out = animat.activate(sens_in)
            self._update_paddle(motor_out)

            self._update_block()

            self._print_game()

        if self.block_pos[0] == self.game_size-1:
            if self.block_pos[1] == self.paddle_pos: # paddle_size is 1
                return 1 # point
            else:
                return 0

if __name__ == '__main__':
    num_nodes = 8
    animat = Animat(num_nodes)
    game_size = 8
    game = Game(game_size)
    game.run(animat)


