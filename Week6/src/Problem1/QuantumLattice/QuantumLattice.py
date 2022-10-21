#
# QuantumLattice.py
#

import math
import numpy as np
import random
from CalculateEnergy import CalulateEnergy

#A simple 1-D QuantumLattice class
class QuantumLattice:
    """
    QuantumLattice
    """
    minSigma=1e-100
    maxSigma=1
    learningRate=1
    numParticleType = 2
    latticeLength = 3
    minLimit=None
    maxLimit=None
    uniprng=None
    normprng=None
    fitFunc=None

    def __init__(self,latticeLength,numParticleType):
        #lattice full of quantum
        self.latticeLength = latticeLength
        self.numParticleType = numParticleType
        #self.fit=self.__class__.fitFunc(self.x)
        self.sigma=random.uniform(0.9,0.1) #use "normalized" sigma
        self.lattice=[random.randrange(0,self.numParticleType) for _ in range(self.latticeLength)]
        self.energy = 0

    def crossover(self, other):
        child = QuantumLattice(latticeLength=self.latticeLength,numParticleType=self.numParticleType)

        #perform crossover "in-place"
        alpha= random.uniform(0,1)

        #Portion of each lattice
        l1_length = int(self.latticeLength*alpha)
        l2_length = self.latticeLength - l1_length

        #Portion of self piece and other piece needed for crossOver
        #Piece them together Creating new child
        s1 = random.sample(self.lattice,l1_length)
        s2 = random.sample(self.lattice,l2_length)
        childLattice = s1 + s2

        child.lattice = childLattice

        return child

    def mutate(self):
        #Mutate by Randomly changing the type of particles in lattice

        #Mutation param, determines how many quantums needed to be changed.
        self.sigma=self.sigma*math.exp(self.learningRate*random.normalvariate(0,1))
        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma
        NumOfMutateParticles = random.randrange(0,int(self.sigma*self.latticeLength)+1)

        #Mutation by changing the quantum types within a lattice
        for _ in range(NumOfMutateParticles):
            random.shuffle(self.lattice)
            self.lattice.pop()
            self.lattice.append(random.randrange(0,self.numParticleType))

    def evaluateFitness(self,selfEnergyVector,interactionEnergyMatrix):
        #Calculate the total energy of this sequence.
        self.energy = CalulateEnergy(self.lattice,
                                 selfEnergyVector=selfEnergyVector,
                                 interactionMatrix=interactionEnergyMatrix)

    def __str__(self):
        print("---------------------------------\nChild's INFO:")
        print(f"Lattice is : {self.lattice}")
        print(f"Total energy:{self.energy}")
        return 'LatticeLength:'+ '%d'%self.latticeLength + '\nNumOfParticleTypes: '+ '%d'%self.numParticleType + '\nSigma = ' + '%0.8e'%self.sigma


#For testing purposes
#Set Basic parameter for test
# u = [1,2,3]
# N = 11
# t = [[10,4,1],[4,10,5],[1,5,10]]
# M = 3
#
# entity1 = QuantumLattice(latticeLength = N,numParticleType = M)
# entity2 = QuantumLattice(latticeLength = N,numParticleType = M)
#
# child = entity1.crossover(entity2)
#
# child.mutate()
#
# child.evaluateFitness(selfEnergyVector = u,interactionEnergyMatrix= t)
# print(child)