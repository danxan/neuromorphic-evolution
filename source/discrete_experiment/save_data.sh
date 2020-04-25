datevar=250411422020
mkdir $datevar
cp avg_fitness.svg config-ff ffnn.log Digraph.gv Digraph.gv.svg neat-checkpoint-277 speciation.svg $datevar
git add -f save_data.sh avg_fitness.svg config-ff ffnn.log Digraph.gv Digraph.gv.svg neat-checkpoint-277 speciation.svg evoalg.py game.py
# git commit -m "replication of albantakis, except logic functions are precoded aggregation functions instead of HMG (as earlier, but added copy and not). game_widt=16, game_height=32, direction is fixed for entire run, Only include Task 1 (from paper)... Improved the implementation of boundaryless. 10000 instead of 60 000 gens, mutate rates/powers are increased with a power of ten. Implemented exponential fitness measure. Tried to run with the same logic as quick test. Still same results (60% fitness). NEW: Will evolve topologies with HIGH mutation rate and high pop size"
git commit -m "replication of albantiks, no fixed-topology, pop 1000, high mutation rates"

