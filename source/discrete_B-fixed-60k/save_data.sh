datevar=085726052020 # date+%R-%D
mkdir $datevar
cp avg_fitness-recurrent.svg config-ff recurrentnn.log neat-checkpoint-23969 $datevar
git add -f save_data.sh avg_fitness-recurrent.svg config-ff recurrentnn.log neat-checkpoint-23969 evoalg.py game.py
git commit -m "60k gen with popsize 100 and fixed topology. Low compability rate (1). Max stagnation 1. best fitness was 74, wantto see this network if possible"
