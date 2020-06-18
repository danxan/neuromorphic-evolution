# Plotting parameters
After getting NEAT to >90% fitness with fixed topology of 5 hidden neurons, in the experiment discrete\_B-fixed-60k, I want to use that experiment's config as a baseline for plotting a variation in parameters over several epochs.

## Population size
Population size is the easiest parameter to plot over, and it is a reasonable parameter to question:
What size is optimal in order to explore the solution space for the problem.

A problem with the population size in neat is that it is not static, it changes with the number of species, survivability and so on (elaborate later).
The pop\_size attribute in the Config class is controlling the maximum amount of species, not individuals.
However, I have tried to plot the initial population size for each run.

## Elitism
Elitism is another good parameter to plot, as I have tried to figure out what is optimal.

