import numpy as np

class Animat:
    def __init__(self, num_nodes):
        self.genome = np.random.randint(-15,15, (num_nodes, num_nodes))
        #genome = genome/np.linalg.norm(genome)
        #genome = 2.*(genome - np.min(genome))/np.ptp(genome)-1
        print(f"genome: {self.genome}")
        print(f"sum:  {sum(self.genome)}")
        print(f"count zeros:  {np.count_nonzero(self.genome==0)}")

    def or_func(self, neur_in):
        # OR
        treshold = 0
        if np.mean(neur_in) > treshold:
            return 1
        elif np.mean(neur_in) < treshold:
            return -1
        else:
            return 0

class Game:
    '''
    For now the block only has the size of one unit
    '''
    def __init__(self, game_size, block_size):
        self.board = np.zeros((game_size, game_size))
        # init block
        self.board[0][0] = 1
        self.paddle_pos = 0

    #def update_state(self):
    def update_paddle(self, motor_out):
        # moves positon along axis of freedom, checks for boundaries
        if motor_out > 1 and self.paddle_pos < 32:
            self.paddle_pos += 1
        elif motor_out < 1 and self.paddle_pos > -32 :
            self.paddle_pos -= 1


def run(self, syn_in):
    neur_in = syn_in*self.genome
    ret = self.or_func(neur_in)
    self.move(ret)

if __name__ == '__main__':
    num_nodes = 8
    animat = Animat(num_nodes)

    #game =
    # each animat should receive input to one of it's nodes.
    # let it be the first node in the genome
    # all nodes receive only zero as input
    # the "sensor" node will send its output through all connections
    sense_in = np.zeros(num_nodes)
    sense_in[0] = 1
    # this can be done by:
    # Having all the connecitons to a node as a row in a 8x8 matrix.
    # The first thing that happens in the activation function would be that the input is multiplied with the row.
    # The output of each node contribute to an element in the input array for the next "layer".
    # The 1x8 input  array is multiplied with the 8x8 matrix, which generates a new 1x8 input array.
    animat.run(sense_in)
    print(animat.paddle_pos)
    # The motor is connected to one of the nodes, and will move if that element of the 1x8 input array is above treshold.


