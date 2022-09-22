# %%
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_NUM = 10000
sample = np.random.uniform(0,1,SAMPLE_NUM)
print(sample[:30])


# %%

count, bins, ignored = plt.hist(sample, 30, density=True)


plt.title("Unform Distribution from 0~1")
plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')

plt.show()

# %%
mu, sigma = 5, 2 # mean and standard deviation

sample = np.random.normal(mu, sigma, SAMPLE_NUM)
print(sample[:5])

# %%
type(sample)

# %%
count, bins, ignored = plt.hist(sample, 30, density=True)

plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *

               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),

         linewidth=2, color='r')
plt.title(f"Normal distribution with mean {mu}, std {sigma}")
plt.show()

# %%
import random
from random import randint
#2d6
NUM_OF_DICE = 2
SIZE_OF_DIE = 6
NUM_OF_TRIALS = 10000

list_of_sum = []

random.seed()
randint(1,SIZE_OF_DIE)

# %%
#Testing with the dice roll generator
for _ in range(NUM_OF_TRIALS):
    sum_of_die = 0
    for _ in range(NUM_OF_DICE):
        sum_of_die += randint(1,SIZE_OF_DIE)

    list_of_sum.append(sum_of_die)

print(list_of_sum[:20])

# %%
from typing import List

#Creating function for reusability
def dice_roll_generator(num_of_dice:int , size_of_die : int,num_of_trials:int) -> np.ndarray:
    """
    Args:
        num_of_dice (int): The number of dices you have
        size_of_die (int): The upper limit of a single die
        num_of_trials (int): Trials you want to commit

    Returns:
        List: Return a list of summation of die value after a number of trials
    """
    list_of_sum =[]
    for _ in range(num_of_trials):
        sum_of_die = 0
        for _ in range(num_of_dice):
            random.seed()
            sum_of_die += randint(1,size_of_die)

        list_of_sum.append(sum_of_die)

    return np.array(list_of_sum)

# %%
#2d6
two_die_six = []
two_die_six = dice_roll_generator(2,6,10000)
print(f'type:{type(two_die_six)} , {two_die_six[:5]}')


# %%
#Creating plot histogram function
def plt_hist(list:np.ndarray,title:str)->None:
    plt.hist(list, 50, density=False)
    plt.title(title)
    plt.show()

# %%
#2d6
plt_hist(dice_roll_generator(2,6,10000),"2d6")

# %%
#1d12
plt_hist(dice_roll_generator(1,12,10000),"1d12")

# %%
#2d10
plt_hist(dice_roll_generator(2,10,10000),"2d10")

# %%
#1d20
plt_hist(dice_roll_generator(1,20,10000),"1d20")

# %%
