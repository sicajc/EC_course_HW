import math
def fitnessFunc(x_vec):
    An = 10
    sum = 0
    for i in range(len(x_vec)):
        sum += x_vec[i]**2 - An*math.cos(2*math.pi*x_vec[i])

    fitness = An + sum
    return fitness