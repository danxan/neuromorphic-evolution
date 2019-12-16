
#Initialize population. Block space is 9. So the network would have to be sqrt(9)+1=3.
# num_individuals can be 100.
def create_networks(network_size, num_individuals):
    """
    Create network_size number of populations using pynn.Population().
    Add to each population to a network, and add each network to networks.

    """
    return networks

def create_block_spaces(size_block_space, num_individuals):
    """
    Create size_block_space number of populations using pynn.Population().
    Add to each population to a network, and add each network to networks.
    """
    return block_spaces

    """
    Normally the connections are defined by a genome of random numbers.
    Here it could be that for every individual,
    the projections to be made is defined by a list of random values in the range [-a,a],
    where a is the strength of the synapses.
    This could be represented in a list genomes, which would be used in the loop below.
    """
def init_pop(size_block_space, num_individuals):
    network_size = 2**(size_block_space) -1
    block_spaces = create_block_spaces(size_block_space, num_individuals)
    networks = create_networks(network_size, num_individuals)
    #genomes is a list of lists genome, where each genome has size_block_space*network_size values between -a and a
    genomes[num_individuals] = random.sample(range(-a,a,), size_block_space*network_size)
    individuals = zip(block_spaces, networks, genomes)
    for block_space, network, genome in individuals:
        """
        Create synapses between block_space and network.
        The synapses are defined by the genome of the individuals.
        """
    return individuals

##REPEAT:
#Run "ring-game".
#Evaluate fitness. Exponential fitness measure of S = 1.02**(fitness*128)
def run_ring_game(individuals):
    """
    A stimulus is given to neuron 0 of every unit in every block_space.
    Number of spikes in every network is measured and counted in fitness,
    where fitness[i] correspond to block_spaces[i] and networks[i].

    The ring game is run 128 times for every network,
    and the count is appended to fitness.
    After 128 trials, the exponential fitness measure is applied:
    fitness = 1.02**(fitness*128)
    """
    return fitness

#Crossover.
def differential_replication(fitness, individuals):
    """
    Individuals are selected into the next generation by a probability proportional to their fitness.
    Selected individuals are differentially replicated.
    """
    return new_population

#Mutation
def mutation(new_population):
    """
    TODO: Need to figure out when the three different scenarios will happen...
    For every connection of the population, there's a probability the following will happen:
    a) 0.5%: The strength will change randomly.
    b) 2%: A sequence of adjacent connections of size ranging between 16 and 512 is deleted.
    c) 5%: A sequence of adjacent connections of size ranging between 16 and 512 is duplicated and inserted at a random location in the genome.
    """
    for block_space, network, genome in individuals:
        """
        Create synapses between block_space and network.
        The synapses are defined by the genome of the individuals.
        """
    return mutated_population

"""
## NOTES:

    For the following two ring games, a network is actually an unconnected set of units.
    All synapses to be evolved are between the sensor space and the "network, and between the "network" and the motor space.
    (sensor space and motor space can be abstracted away, leaving synapses in both directions between block space and the network (which would still leave the "network" unconnected).
    The number of units in the network would have to be 2**n -1, where n is the number of units in block space.
    (For a network of size n, where n is the number of units in the network, allows a block space of size 2**n - 1.

# Simple Ring game 1:
    (NOTE: The complexity of the neural networks can not grow)
    A fixed size block is moving in a determined direction in a ring called block space.
    The block is unit of neurons that excite their neightbours in the determined direction.
    Under the block space is two sets of units the same size as the block, called paddle space.


    Each units in block space are connected by an excitatory synapse to the unit directly under it in paddle space,
    this allows the block to excite the unit directly under it.

    When a unit in paddle space is excited, it will fire inhibitory signals to all units in block space.
    The block is stopped if the incoming inhibitory signal is sufficiently strong.
    The weights of the inhibitory signals is to be evolved.

    Fitness is determined by how many excitations followed by inhibitions is required to stop the block.

# Simple Ring game 2:
    *THE NETWORK ALWAYS SEES THE BLOCK, BUT NEEDS TO AIM CORRECTLY.*
    (NOTE: For now, this is the solution I'd go for)
    A fixed size block is moving in a determined direction in a ring called block space.
    A block is a unit of neurons that excite their neighbours in the determined direction.
    Under the block space is a set of units the same size as the block, called sensor space and motor space respectively.

    __________________
    (ALTERNATIVELY:
    Excitatory synapse to motor space could be replaced by inhibitory synapse to block space, directly.
    The same for sensor space. Where, instead, the units in block space would be directly connected to the network with excitatory synapses.
    ____________________

    Each unit in the block space are connected by an excitatory synapse to the unit directly under it in sensor space,
    this allows the block to excite the unit directly under it.

    Each unit in the motor space is connected to the unit directly above it in block space by an inhibitory synapse,
    this allows the motor space unit to inhibit the block space unit, and this stop the block.

    When a unit in sensor space is excited, it will fire and excitatory signal to the network.
    The signal will pass through the network, and eventually excite a unit in motor space.
    Exciting the right motor space unit would inhibit the next block unit and stop the block.

    Which motor space unit to be excited is up the the network, but how to constrain it so that it can't excite more than one motor space unit?
        A possible solution is to let all units in sensor space be connected to all units in the network,
        and all units of the network would be connected to all units in block space.
        The evolution would be about finding the correct the weights and signs of the synapses between sensor space and network space in order to stop the block with as few fires as possible.

        So, without the fitness score, the ideal solution would be to have strong inhibitory synapses between all network units and all block space units
        so that all block space units would be inhibited no matter where the block was.
        However, with a fitness score measuring the number of spikes, the networks exploiting this tactic would have a lower score, and thus be excluded.
        The worst score would then be the number of block units, and the best score would be 1.

    When no units in sensor space is excited, the trial stops,
    and fitness can be determined by the amount of spikes in motor space during the trial.
    A low amount of spikes would mean a high fitness.

# Ring game (advanced):
Right now the ring game is a block moving back and forth in a horizontal direction.
The networks is to successfully assess the size and direction of this block and fire inhibitory stimulus to the block to stop "the ring".

Stopping the ring:
    A paddle will be used,
    the paddle will have to be moved under the moving block to stop it.

Implementation of the paddle:
    The paddle consist of a certain number of units that constantly fire inhibitory stimulus to the neurons directly above them.
    Each unit should consist of the same number of neurons as the maximum amount of neurons allowed in a block.
    The paddle is moved by motors, and a sensor is used to assess the direction and size of the block.
    When the size is assessed, the paddle neurons will have to fire the right amount of signals to the block,
    to the right neurons in the block.

    Assumption:
    All units in "block space" consist of the max size of a block,
    and all units in block space have full connectivity to the units in paddle space located directly beneath.
    The size of the block is determined by how many neurons fired per unit.

Implementation of the motors (left and right):
    Each motor can move the paddle one unit at a time.
    E.g. the left motor moves one unit left by removing stopping the fire from the unit farthest to the right and starting firing from the unit one step to the left.

How to implement the sensors:
    The sensors are units located next to the paddle on either side. The sensors are excited by the units firing directly above them.
    The sensors move with the paddle.

How I think this works in brainscales:
    (SEE WHITEBOARD):
        Case A: Block found and stopped.
        How do I tell if it's stopped?
        How do I measure fitness from this? (The block is always stopped.)

        Case B: The block have to be found first.
        The directions are sorted out by having two parallel rings, and a change in direction would mean to change ring.
        Question? Using the implementation described on the whiteboard under A the block will eventually be stopped when enough "weak signals" are fired at it.
        By weak signal I mean that the number of neurons firing is smaller than the number of neurons in the block unit.

#To replicate the Larissa article I eventually want a "falling blocks" game,
where the size of the block is to be determined. Some sizes are to be caught, and some are to be avoided.
The game consist of 16x36 units (where a unit is a population of neurons).

The game is run 128 times, and the fitness is calculated from the percentage of successfully caught and avoided blocks out of possible 128 trials.
In each trial, the block falls from top to bottom in 36 time steps, moving 1 unit downwards and sideways always in the same direction.
I think that the size of the block could be the size of the population that is the block.

The "paddle" of the network would be a number of neurons in the bottom row of the game, the network will always fire inhibitory signals to it's paddle,
and will move the paddle by changing which neurons it fires to. When the block lands at the paddle it is caught.
If the block lands outside the paddle is avoided.

The network has two sensors, which are used to assess the direction and size of the falling blocks from each initial condition.

The fitness is calculated from the percentage of successfully caught or avoided blocks.

"""
