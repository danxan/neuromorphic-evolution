datevar=164203062020 # date+%R-%D
mkdir $datevar
cp avg_fitness-recurrent.svg config-ff recurrentnn.log neat-checkpoint-59952 $datevar
git add -f save_data.sh avg_fitness-recurrent.svg config-ff recurrentnn.log neat-checkpoint-59952 evoalg.py game.py
git commit -m "60k gen with popsize 150 and fixed topology. Low compability rate (1). Max stagnation 10. Species Elitism 5. Elitism 5. Best fitness was 90"
