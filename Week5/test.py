#
# Binary tournament selection experiment
#

from random import Random
import matplotlib.pyplot as plt
import random
import copy

# A few useful constants
#
pop_size = 20
generations = 10
fit_range = 40

# Init the random number generator
#
prng = Random()
prng.seed(123)


# Let's suppose we have an imaginary problem that generates
# integer fitness values on some fixed range.  We'll start by randomly
# initializing a population of fitness values
#
pop = [prng.randrange(0, fit_range) for i in range(pop_size)]


# Helper function to plot histogram of population fitness values
#
def plt_hist(pop, generation=0, bin_limit=fit_range):
    plt.hist(pop, bins=range(0, bin_limit+1))
    plt.grid(True)
    plt.title('Generation: ' + str(generation))
    plt.show()


# Binary tournament operator:
#  - Input: population of size N (pop_size)
#  - Output: new population of size N (pop_size), the result of applying selection
#
#  - Tournament pairs should be randomly selected
#  - All individuals from input population should participate in exactly 2 tournaments
#
# Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
'''
Tournament selection (k):
1.Pick k members randomly, best one wins. (binary_tournament k=2)
2.Repeat
3.Probability of selecting i will depend on
    #1 Rank/relative fitness of i
    #2 Size of sample k (k=2 for binary_tournament, higher k increase selection pressure)
    #3 Whether fittest contestant always wins(deterministic) or this happens with probability "p"
In binary_tournament:
    a. If implemented properly, all parents will participate in exactly 2 tournament
    b. Popular selection operator:
        1.Easy to implement
        2.Linear selection pressure ---- very important
        3.Doesn't depend on absolute fitness value
    c. Works very well for multi-objective
    d. If want higher selection pressure can use k>2
'''

def binary_tournament(pop,prng):
    k=2                                 #Tournament selection "k" here is 2  (binary_selection)
    parents_selection=[]
    for i in range(k):
        pop_in=pop.copy()
        for j in range(pop_size//k):
            parents=prng.sample(pop_in,2)
            pop_in.remove(parents[0])
            pop_in.remove(parents[1])
            if parents[0] < parents[1]:
                parent=parents[0]
            else:
                parent=parents[1]
            parents_selection.append(parent)

    return parents_selection


for i in range(generations):
    print(pop)
    plt_hist(pop, i)

    pop = binary_tournament(pop, prng)