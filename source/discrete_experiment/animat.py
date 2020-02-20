import numpy as np

genome = np.random.randint(-15,15, 8**8)
genome = 1000*genome/np.linalg.norm(genome)
#genome = 2.*(genome - np.min(genome))/np.ptp(genome)-1
print(genome)
print(sum(genome))
print(np.count_nonzero(genome==0))

def activation(input):
    treshold = 0
    # OR
    if any(input) > treshold:
        return 1
    else:
        return 0

# each animat should receive input to one of it's nodes.
# let it be the first node in the genome
# all nodes receive only zero as input
# the "sensor" node will send its output through all connections
# this can be done by:
# Having all the connecitons to a node as a row in a 8x8 matrix.
# The first thing that happens in the activation function would be that the input is multiplied with the row.
# The output of each node contribute to an element in the input array for the next "layer".
# The 1x8 input  array is multiplied with the 8x8 matrix, which generates a new 1x8 input array.
# The motor is connected to one of the nodes, and will move if that element of the 1x8 input array is above treshold.




#class animat:
#    ''' each animat is initialized with possible connections to all others,
#    but most weights should be 0 to cancel the connection '''
#    # for a mlp this only describe the weights
#    # there's 8 nodes, meaning 8**8 weights



