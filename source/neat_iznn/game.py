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
    def __init__(self, game_width, time_const):
        self.time_const = time_const
        self.game_cnt = 0
        self.direction = 0
        self.game_width = 16
        self.game_height = 36

        self.moves_cnt = 0

        # The height is three times the width, to make the game possible.
        self.board = np.zeros((self.game_height, self.game_width))

        self.screen = screen.Screen()

    #def update_state(self):
    def _update_paddle(self, motor_out):
        decision = 0
        if motor_out[0] > motor_out[1]:
            decision = -1
            self.moves_cnt += 1
        elif motor_out[0] < motor_out[1]:
            decision = 1
            self.moves_cnt += 1

        self.paddle_pos = (self.paddle_pos + decision)%self.game_width

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

        #self.screen.print(vizboard)
        print(vizboard)


    def run(self, animat, d=False):
        '''
        It takes an animat player to play the game.
        '''

        #RESET GAME
        self.block_pos = [0, random.randint(0,self.game_width)] # postion in y,x / rows, cols
        # Set block size with a "coin flip"
        p = random.randint(0,2)
        if p == 1:
            self.block_size = 1
        else:
            self.block_size = 3
        #self.board[self.block_pos[0]][self.block_pos[1]] = 1
        self.paddle_pos = random.randint(0, self.game_width)# along the x-axis / cols
        self.direction = random.randint(-1,2)

        score = 0 # return value
        w = self.game_width # to make code readable

        for i in range(self.game_height):
            self._update_block()

            w = self.game_width

            start = self.block_pos[1]
            end = start+self.block_size
            left_sens = self.paddle_pos-1
            right_sens = self.paddle_pos+1

            sens_in = [0,0]

            for i in range(start, end, 1):
                if (i%w) == left_sens%w:
                    sens_in[0] = self.block_pos[0]
                if (i%w) == right_sens%w:
                    sens_in[1] = self.block_pos[0]

            if d == True:
                self._print_game()
                print(sens_in)

            outputs = np.zeros(2)
            runtime = 33 # ms
            dt = animat.get_time_step_msec()
            steps = int(runtime/dt)

            animat.set_inputs(sens_in)
            for step in range(steps): # 33 ms
                output = animat.advance(dt)
                outputs += output
            self._update_paddle(outputs)

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

        return score

if __name__ == '__main__':
    game = Game(8)
    player = player.Player()
    game.run(player, d=True)


