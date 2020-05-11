import numpy as np
import random
import screen
import player
import getch

class Game:
    '''
    For now the block only has the size of one unit

    Game size is fixed for now. Disregard parameter.
    '''
    def __init__(self, game_width):
        self.game_cnt = 0
        self.direction = 0
        self.game_width = 8
        self.game_height = 16

        self.moves_cnt = 0

        # The height is three times the width, to make the game possible.
        self.board = np.zeros((self.game_height, self.game_width))

        self.screen = screen.Screen()

    #def update_state(self):
    def _update_paddle(self, motor_out):
        if motor_out[0] == 0 and motor_out[1] == 0:
            self.paddle_pos = self.paddle_pos
        elif motor_out[0] == 1 and motor_out[1] == 1:
            self.paddle_pos = self.paddle_pos
        elif motor_out[1] == 1:
            self.moves_cnt += 1
            if self.paddle_pos == self.game_width-1:
                self.paddle_pos = 0
            else:
                self.paddle_pos += 1
        elif motor_out[0] == 1:
            self.moves_cnt += 1
            if self.paddle_pos == 0:
                self.paddle_pos = self.game_width-1
            else:
                self.paddle_pos -= 1

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

    def _print_game(self):
        vizboard = np.zeros((self.game_height, self.game_width))
        if self.block_size == 1:
            vizboard[self.block_pos[0]][self.block_pos[1]] = 1
        if self.block_size == 3:
            vizboard[self.block_pos[0]][self.block_pos[1]:self.block_pos[1]+3] = 1
        vizboard[self.game_height-1][self.paddle_pos-1:self.paddle_pos+2] = 1
#        self.screen.print(vizboard)
        print(vizboard)


    def run(self, animat, d=False):
        '''
        It takes an animat player to play the game.
        '''

        #RESET GAME
        self.block_pos = [0, random.randint(0,self.game_width-1)] # postion in y,x / rows, cols
        # Set block size with a "coin flip"
        p = random.randint(0,1)
        if p == 1:
            self.block_size = 1
        else:
            self.block_size = 3
        #self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = random.randint(0, self.game_width-1)# along the x-axis / cols
        self.direction = random.randint(-1,1)

        while self.block_pos[0] < self.game_height-1: # until the block is at the bottom of the board
            self._update_block()
            if self.block_size == 1:
                # The animat views the board with its two sensors. Has a view of one unit to the left or right.
                if self.block_pos[1] == self.paddle_pos - 1:
                    #print("sensed block on right sensor")
                    sens_in = [1,0]
                elif self.block_pos[1] == self.paddle_pos +1:
                    sens_in = [0,1]
                    #print("sensed block on left sensor")
                else:
                    sens_in = [0,0]
                    #print("didnt sense block")
            if self.block_size == 3:
                # The animat views the board with its two sensors. Has a view of one unit to the left or right.
                if self.block_pos[1] == self.paddle_pos-1:
                    sens_in = [1,1]
                elif self.block_pos[1] == self.paddle_pos:
                    sens_in = [0,1]
                elif self.block_pos[1] == self.paddle_pos+1:
                    sens_in = [0,1]
                elif self.block_pos[1]+1 == self.paddle_pos-1:
                    sens_in = [1,0]
                elif self.block_pos[1]+1 == self.paddle_pos+1:
                    sens_in = [0,1]
                elif self.block_pos[1]+2 == self.paddle_pos-1:
                    sens_in = [1,0]
                elif self.block_pos[1]+2 == self.paddle_pos:
                    sens_in = [1,0]
                else:
                    sens_in = [0,0]

            output = animat.activate(sens_in)
            self._update_paddle(output)

            if d == True:
                self._print_game()

        # at the last time-step
        if self.block_pos[0] == self.game_height-1:
            # TESTING "KILLING LASER"
            if self.moves_cnt == 0:
                return 0

            w = self.game_width

            start = self.block_pos[1]
            end = start+self.block_size
            crash = False
            paddle_start = self.paddle_pos-1
            paddle_end = self.paddle_pos+1

            #print('block: %d, %d',start, end)
            #print('paddle: %d, %d',paddle_start, paddle_end)
            for i in range(start, end, 1):
                for j in range(paddle_start, paddle_end+1, 1):
                    crash = (i%w) == (j%w)
                    #print(i, "==", j , "|", i%w, "==", j%w , "|", crash)
                    if crash: break
                if crash: break


            ret = 0
            if crash:
                if self.block_size == 1:
                    ret = 1
            else:
                if self.block_size == 3:
                    ret = 1

            if d == True:
                print(ret)

            return ret



            '''
            # catch
            if self.block_size == 1:
                if self.paddle_pos == 0: # handle left edge-case wraparound
                    if self.game_width-1 == self.block_pos[1] or 1 == self.block_pos[1] or 0 == self.block_pos[1]:
                        if d == True:
                            print('1')
                        return 1
                    else:
                        if d == True:
                            print('0')
                        return 0
                elif self.paddle_pos == self.game_width-1:
                    if self.game_width-2 == self.block_pos[1] or 0 == self.block_pos[1] or self.game_width-1==self.block_pos[1]:
                        if d == True:
                            print('1')
                        return 1
                    else:
                        if d == True:
                            print('0')
                        return 0
                else:
                    if self.paddle_pos-1 == self.block_pos[1] or self.paddle_pos == self.block_pos[1] or self.paddle_pos+1 == self.block_pos[1]: # paddle size is 3
                        if d == True:
                            print('1')
                        return 1 #self.game_width-3 # point
                    else:
                        if d == True:
                            print('0')
                        return 0
            # avoid
            elif self.block_size == 3:
                if self.paddle_pos == 0:
                    if self.block_pos[1]+2 >= self.game_width-1:
                        if d == True:
                            print('0')
                        return 0
                    elif self.block_pos[1] <= 1:
                        if d == True:
                            print('0')
                        return 0
                    else:
                        if d == True:
                            print('1')
                        return 1 # successfully avoided
                elif self.paddle_pos == self.game_width-1:
                    if self.block_pos[1] >= self.game_width-4:
                        if d == True:
                            print('0')
                        return 0
                    elif self.block_pos[1] <= 0:
                        if d == True:
                            print('0')
                        return 0
                    else:
                        if d == True:
                            print('1')
                        return 1 # successfully avoided
                else:
                    # is the left side of the block on the right side of the paddle
                    if self.block_pos[1] > self.paddle_pos + 1:
                        if d == True:
                            print('1')
                        return 1# successfully avoided
                    elif self.block_pos[1] + 2 < self.paddle_pos - 1:
                        if d == True:
                            print('1')
                        return 1# successfully avoided
                    else:
                        if d == True:
                            print('0')
                        return 0
            '''

if __name__ == '__main__':
    game = Game(8)
    player = player.Player()
    game.run(player, d=True)


