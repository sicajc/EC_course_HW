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
generations=20
fit_range=50

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

    #Binary Tournament
    #1. Creating compete pairs
    compete_pairs = []
    for _ in range(pop_size//2):
        #Shuffle the list
        random.shuffle(pop)
        x1 = pop.pop()
        x2 = pop.pop()
        compete_pairs.append([x1,x2])

    #2.Conduct binary tournament
    competed_result = []
    for pairs in compete_pairs:
        if pairs[0] < pairs[1]:
            competed_result.append(pairs[0])
        else:
            competed_result.append(pairs[1])

    #3. Perform mating,create children using weight bias
    for _ in range(pop_size//2):
        parent = random.sample(competed_result,2)
        alpha = np.random.uniform(0,1)
        child = parent[0] * alpha + (1 - alpha) * parent[1]
        competed_result.append(int(child))

    newPop = competed_result

    return newPop


#Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
for i in range(generations):
    print(pop)
    plt_hist(pop,i)

    pop=binary_tournament(pop, prng)
