#
# Binary tournament selection experiment
#

from random import Random
import random
import matplotlib.pyplot as plt
import numpy as np

#A few useful constants
#
pop_size=20
generations=15
fit_range = 40

#Init the random number generator
#
prng=Random()
prng.seed(123)

#Let's suppose we have an imaginary problem that generates
#integer fitness values on some fixed range.  We'll start by randomly
#initializing a population of fitness values
#
pop = [prng.randrange(0,fit_range) for _ in range(pop_size)]


#Helper function to plot histogram of population fitness values
#
def plt_hist(pop, generation=0, bin_limit=fit_range):
    plt.hist(pop, bins=range(bin_limit+1))
    plt.grid(True)
    plt.title(f'Generation: {str(generation)}')
    plt.show()


#Binary tournament operator:
#  - Input: population of size N (pop_size)
#  - Output: new population of size N (pop_size), the result of applying selection
#
#  - Tournament pairs should be randomly selected
#  - All individuals from input population should participate in exactly 2 tournaments
#
def binary_tournament(pop_in, prng):
    newPop=[]

    if(len(pop_in) == 1): return pop_in
    #Binary Tournament
    competed_result = []

    for _ in range(len(pop_in)//2):
        # mutate = random.randint(0,1)
        #Shuffle the list
        #1. Creating compete pairs
        random.shuffle(pop_in)

        x1 = pop_in.pop()
        x2 = fit_range if len(pop_in)==1 else pop_in.pop()

        #2. binary tournament
        if x1 < x2:
            competed_result.append(x1)
        else:
            competed_result.append(x2)

    #3. Mating
    # for _ in range(pop_size//2):
        # parent = random.sample(competed_result,2)
        # alpha = np.random.uniform(0,1)
        # child = parent[0] * alpha + (1 - alpha) * parent[1]
        # competed_result.append(int(child))

    newPop = competed_result
    #print(f"Length of newPop = {len(newPop)}")
    return newPop


#Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
for i in range(generations):
    print(pop)
    plt_hist(pop,i)

    pop=binary_tournament(pop, prng)
