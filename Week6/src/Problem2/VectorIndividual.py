#Individuals(vector of floats)
#
# Individual.py
#
#

import random
import math
from random import Random
import copy

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
    vectorLength = None

    def __init__(self,name = None):
        self.vector_x = [self.uniprng.uniform(self.minLimit,self.maxLimit) for _ in range(self.vectorLength)]
        self.fit=self.__class__.fitFunc(self.vector_x)
        self.sigma=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma
        self.name = name

    def crossover(self, other):
        child = copy.deepcopy(self)
        child.vector_x = []
        #Set alpha
        alpha= random.uniform(0,1)
        #Portion of each vector_x
        l1_length = int(self.vectorLength*alpha)
        l2_length = self.vectorLength - l1_length
        #Portion of self piece and other piece needed for crossOver
        #Piece them together Creating new child
        s1 = random.sample(self.vector_x,l1_length)
        s2 = random.sample(other.vector_x,l2_length)
        childVector = s1 + s2
        child.vector_x = childVector

        #ReEvaluate fitness
        child.evaluateFitness()

        return child


    def mutate(self):
        self.sigma=self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0,1))

        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma

        for i,x in enumerate(self.vector_x):
            if(self.sigma < 0.3): break #Simply not mutating
            #Shift the value of x to postive first
            tmp = x + abs(self.minLimit)
            #Bias can only be positive, there would be no negative bias
            bias = (self.maxLimit-self.minLimit)*self.sigma*self.normprng.normalvariate(0,1)
            tmp = bias + tmp

            #Shift x back
            self.vector_x[i] = tmp - abs(self.minLimit)

        #ReEvaluate Fitness
        self.evaluateFitness()

    def evaluateFitness(self):
        self.fit=self.__class__.fitFunc(self.vector_x)

    def __str__(self):
        if self.name is not None:
            print(f"Name :\n{self.name}")
        print(f"x_vec:\n{self.vector_x}      Fit:{self.fit}")
        return '\n'
