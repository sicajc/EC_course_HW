import math
import numpy as np

def N_Dimensional_Rastrigin(x_vec):
    A = 10
    n = len(x_vec)
    sum = 0
    for i in range(len(x_vec)):
        sum += x_vec[i]**2 - A*math.cos(2*math.pi*x_vec[i])

    fitness = A*n + sum

    return fitness

#Finding total energy of lattice
def CalulateEnergy(lattice,interactionMatrix,selfEnergyVector):
    totalEnergy = 0
    latticeLength = len(lattice)

    #Energy by self-energy
    for quantum in lattice:
        #print(f"Type extracted : {type(selfEnergyVector[quantum])} of value : {selfEnergyVector[quantum]}")
        totalEnergy += selfEnergyVector[quantum]

    #print(f"total energy after self-energy:{totalEnergy}")
    #Energy by interaction
    for idx,quantum in enumerate(lattice):
        #Interaction matrix of the quantum to itself
        if idx == 0:
            #Corner case Left Most
            quantum_right = lattice[idx+1]
            totalEnergy += interactionMatrix[quantum][quantum_right]
        elif idx == latticeLength - 1:
            #Corner case right Most
            quantum_left = lattice[idx-1]
            totalEnergy += interactionMatrix[quantum][quantum_left]
        else:
            #General case
            quantum_right = lattice[idx+1]
            quantum_left = lattice[idx-1]
            totalEnergy += interactionMatrix[quantum][quantum_right] + interactionMatrix[quantum][quantum_left]


    #print(f"Energy after interation:{totalEnergy}")
    return totalEnergy
