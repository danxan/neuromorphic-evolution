#Introduction
* Two versions of the falling blocks game has been implemented. A solution to the game is found using a simple GA without crossover, but no good solution is found when using NEAT.
In this report I will describe the game, the solutions and the results.

#The Falling Blocks Game
*This section will give a general description of the game, and then each of its elements. After each description, a description of the implementation is given.*
The game consists of a 2-dimensional environment in which there are spawned a block and a paddle with sensors and motors.
The neural network agent is supposed to control the paddle, to either catch or avoid the block.
Whether the block is to be caught or avoided is to be determined based on observation of the block size.

The various tasks of the game:
###Task 1:
* Catch blocks of size 1
* Avoid blocks of size 3
###Task 2:
* Catch blocks of size 1
* Avoid blocks of size 2
###Task 3:
* Catch blocks of size 1
* Catch blocks of size 4
* Avoid blocks of size 2
* Avoid blocks of size 3
###Task 4:
* Catch blocks of size 3
* Catch blocks of size 6
* Avoid blocks of size 4
* Avoid blocks of size 5

##The Environment
The environment in which the block and paddle are spawned is 2-dimensional, but the lateral edges are wrapped around.
This means that the block and paddle can move from the right edge to the left edge with one step to the right(, and the other way around).
The size of the environment is 36 units high and 16 units wide.

##The Block
The block is always initialized at a random position on the upper edge of the environment, with a random falling-direction which is either straight down, diagonal down-left or diagonal down-right.
During the game instance, the falling direction will never change.
The block will be initialized with different sizes, where each size determines whether the agent should catch or avoid the block.

The block falls with one unit per time-step.

##The Paddle
The paddle is initialized in the middle position at the lower edge of the environment.
The paddle always has a size of 3 units. Where a sensor is placed at the first and third unit - the edges of the paddle.
This means the paddle has a "blind spot" on its second unit.
A sensor can see the closest object that is in a straight line upwards from the sensor.
The motors of the paddle can be activated to propel it to the left or right, respectively.
If both motors are activated simultaneusly the paddle will not move.
The neural network agent's input nodes is connected to the sensors on the paddle, while its output is connected to the motors of the paddle.
This implies that each neural network has 2 input nodes and 2 output nodes, while they have an unknown amount of hidden nodes.

The paddle can be moved one unit per timestep.

##Implementation
###A:
The height and width of the environment is simply constraints limiting the number of possible positions and the duration of the game.
The position of the block and the paddle are stored as integers in a vector, and updated at every timestep.
The update is based on the direction of the block or the decision of the agent, and the update-functions contain several if-conditions that make up for the contraints of the environment.
When a unit of the block is vertically aligned with the position of a sensor, the sensor will light up.

The function for updating the paddle is implemented as follows:
```
def _update_paddle(self, motor_out):
    if motor_out[0] == 0 and motor_out[1] == 0:
        self.paddle_pos = self.paddle_pos # nothing happens
    elif motor_out[0] == 1 and motor_out[1] == 1:
        self.paddle_pos = self.paddle_pos # nothing happens
    elif motor_out[1] == 1: # move right
        if self.paddle_pos == self.game_width-1: # wrap-around
            self.paddle_pos = 0
        else:
            self.paddle_pos += 1
    elif motor_out[0] == 1: # move left
        if self.paddle_pos == 0:
            self.paddle_pos = self.game_width-1 # wrap-around
        else:
            self.paddle_pos -= 1
```

The function for updating the block is implemented as follows:
```
def _update_block(self):
    self.block_pos[0] += 1 # move down
    if self.block_pos[1] == self.game_width -1: # handle edge-case on the right
        if self.direction == 1:
            self.block_pos[1] = 0 # wrap-around
        elif self.direction == -1:
            self.block_pos[1] = self.game_width - 2 # move left
        elif self.direction == 0:
            self.block_pos[1] = self.block_pos[1] # no vertical movement / falling straight down
    elif self.block_pos[1] == 0: # handle edge-case on the left
        if self.direction == 1: # move right
            self.block_pos[1] = 1
        elif self.direction == -1: # wrap-around
            self.block_pos[1] = self.game_width -1
        elif self.direction == 0:  # no vertical movement / falling straight down
            self.block_pos[1] = self.block_pos[1]
    else:
        self.block_pos[1] += self.direction
```

These update-functions should be efficient and error-free.






