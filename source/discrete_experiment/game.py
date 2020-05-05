import numpy as np
import random
import copy

class Game:
    '''
    For now the block only has the size of one unit

    Game size is fixed for now. Disregard parameter.
    '''
    def __init__(self, game_width):
        self.game_cnt = 0
        self.direction = [0,0]
        self.game_width = 16
        self.game_height = 36

    def move_paddle(self, board, ann):
        idx = [i for i in range(len(board[0])) if board[-1,i]==1] # save the indices where the paddle is
        sens_in = [0,0]
        for x in range(len(board)-1): # check all rows
            idx2 = [i for i in range(len(board[0])) if board[x,i]==1] # save indices of block
            if idx2:
                # sends the height of the block to the sensor if it aligns
                sens_in[0] = len(board)-x if idx[0] in idx2 else 0
                sens_in[1] = len(board)-x if idx[2] in idx2 else 0
                break
        motor_out = ann.activate(sens_in)
        return motor_out

    def update(self, board, row):
        # move the block
        board[row] = board[row] + self.input_func(copy.deepcopy(board[row-1]),self.direction)
        # flush previous line
        board[row-1] = np.zeros(len(board[row-1]))

    def input_func(self, b, d):
        """
        Args:
            b: input array
            d: an array of two elements. The combination determines the direction for something to be moved.
        """
        b = list(bottom_row)
        if d[0] > d[1]: # move left
            return np.array([b[-1] + b[0:-1])
        elif d[0] < d[1]: # move right
            return np.array(b[1:]+b[0])
        else:
            return np.array(b)

    def _print_game(self):
        vizboard = self.board
        vizboard[:][:] = 0
        vizboard[self.block_pos[0]][self.block_pos[1]] = 1
        vizboard[self.game_height-1][self.paddle_pos] = 2
        print(vizboard)

    def run(self, animat):
        # reset game
        self.board = np.zeros((self.game_height, self.game_width))
        # initializes the paddle based on w=16 and h=36
        self.board[-1, 7:10] = 1
        # set block size with a "coin flip"
        p = random.randint(0,1)

        if p == 0:
            # block size 1
            beg = random.randint(0, self.game_width-2)
            end = beg+1
            self.board[0, beg:end] = 1
        else:
            # block size 3
            beg = random.randint(0, self.game_width-4)
            end = beg+3
            self.board[0, beg:end] = 1

        # the direction is later based on the bigger value
        self.direction = [random.randint(-1,1), random.randint(-1,1)]

        for h in range(1, self.game_height): # until the block is at the bottom of the board
            motor_out = self.move_paddle(self.board, animat)
            self.board[-1] = self.input_func(self.board[-1], motor_out) # moving paddle
            self.update(self.board, h)

        # check values in bottom line (0=nothing, 1=paddle/block, 2=paddle+block)
        u, c = np.unique(self.board[-1], return_counts=true)

        if p == 2 and 2 in u:
            return 1
        elif p == 1 and 2 not in u:
            return 1
        else:
            return 0
