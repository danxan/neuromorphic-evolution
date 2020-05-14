datevar=date+%R-%D
mkdir $datevar
cp avg_fitness.svg config-ff ffnn.log Digraph.gv Digraph.gv.svg neat-checkpoint-9999 speciation.svg $datevar
git add -f save_data.sh avg_fitness.svg config-ff ffnn.log Digraph.gv Digraph.gv.svg neat-checkpoint-9999 speciation.svg evoalg.py game.py
git commit -m "replication of albantakis, except logic functions are precoded aggregation functions instead of HMG (as earlier, but added copy and not). game_widt=16, game_height=36, direction is fixed for entire run, Only include Task 1 (from paper)... Improved the implementation of boundaryless. 10 000 instead of 60 000 gens, mutate rates/powers are increased with a power of ten. Implemented exponential fitness measure."

