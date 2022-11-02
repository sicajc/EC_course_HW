#
# Individual.py
#
#

import math
import copy
from pickletools import float8
from random import Random, normalvariate
import numpy as np

#A simple 1-D Individual class
class Individual:
    """
    Individual
    """
    minSigma=1e-100
    maxSigma=1
    learningRate=1
    minLimit=None
    maxLimit=None
    uniprng=None
    normprng=None
    fitFunc=None
    problemType = None #Picks which problem it belongs to

    def __init__(self,
                 latticeLength = None,
                 vectorLength    = None,
                 numParticleType = None,
                 interactionEnergyMatrix = None,
                 selfEnergyVector = None
                 ):
        #Different initilzation
        if self.problemType == 'Problem1':
            self.numParticleType = numParticleType
            self.latticeLength = latticeLength
            self.sequence = [self.uniprng.randrange(0,self.numParticleType)for _ in range(latticeLength)]
            self.fit=self.__class__.fitFunc(lattice = self.sequence,
                                            interactionMatrix = interactionEnergyMatrix,
                                            selfEnergyVector  = selfEnergyVector)
        else:
            self.vectorLength = vectorLength
            self.sequence = [np.array(self.uniprng.uniform(self.minLimit,self.maxLimit),dtype = 'float16') for _ in range(vectorLength)]
            self.fit=self.__class__.fitFunc(self.sequence)

        self.sigma=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma

    def crossover(self, other):
        child = copy.deepcopy(self)
        child.sequence = []

        sequenceLength = len(self.sequence)
        #Set alpha
        alpha= self.uniprng.uniform(0,1)
        #Portion of each sequence
        l1_length = int(sequenceLength*alpha)
        l2_length = sequenceLength - l1_length
        #Portion of self piece and other piece needed for crossOver
        #Piece them together Creating new child
        s1 = self.uniprng.sample(self.sequence,l1_length)
        s2 = self.uniprng.sample(other.sequence,l2_length)
        childSequence = s1 + s2
        child.sequence = childSequence

        return child

    def mutate(self):

        self.sigma =self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma

        if self.sigma > 0.2:
            if self.problemType == 'Problem2':
            #Float Vector CrossOver, note it cannot goes beyond the min and max value of x = [-5.12,5.12]
                for i,x in enumerate(self.sequence):
                    #Shift the value of x to postive first
                    tmp = x + abs(self.minLimit)
                    #Bias can only be positive, there would be no negative bias
                    bias = (self.maxLimit-self.minLimit)*self.normprng.normalvariate(self.sigma,1)
                    tmp = bias + tmp
                    #Shift x back
                    mutated_value = tmp - abs(self.minLimit)

                    if mutated_value > self.maxLimit:
                        self.sequence[i]  = self.maxLimit
                    elif mutated_value < self.minLimit:
                        self.sequence[i]  = self.minLimit
                    else:
                        self.sequence[i]  = mutated_value
            else:
                #QuantumLattice CrossOver
                #Mutation by changing the quantum types within a lattice
                mu = self.sigma*len(self.sequence)
                var = self.LearningRate * len(self.sequence)
                UpperBound = len(self.sequence)
                LowerBound = 1
                NumOfMutateParticles = int(self.normprng.normalvariate(mu,mu))

                if NumOfMutateParticles > UpperBound:
                    NumOfMutateParticles = UpperBound
                elif NumOfMutateParticles < LowerBound:
                    NumOfMutateParticles = LowerBound

                for _ in range(NumOfMutateParticles):
                    self.uniprng.shuffle(self.sequence)
                    self.sequence.pop()
                    self.sequence.append(self.uniprng.randrange(0,self.numParticleType))


    def evaluateFitness(self,
                        interactionMatrix = None,
                        selfEnergyVector  = None):
        if self.problemType == 'Problem1':
            self.fit=self.__class__.fitFunc(self.sequence,interactionMatrix,selfEnergyVector)
        else:
            self.fit=self.__class__.fitFunc(self.sequence)

    def __str__(self):
        return "\n"

    def display_info(self):
        print("--------------------------------\n[INFO]\n")
        print(f"Sequence: \n {self.sequence}")
        print(f"Parameters: \n sigma = {self.sigma}")
