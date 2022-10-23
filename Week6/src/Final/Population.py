#
# Population.py
#
#

import copy
import math
from operator import attrgetter
from Individual import *

class Population:
    """
    Population
    """

    uniprng                 = None
    crossoverFraction       = None
    problemType             = 'Problem1'
    mode                    = 'MIN'
    selfEnergyVector        = None
    interactionEnergyMatrix = None
    numParticleType         = None
    fitFunc                 = None

    def __init__(self, populationSize,sequenceLength = None):
        """
        Population constructor
        """
        self.population=[]
        for i in range(populationSize):
            if self.problemType == 'Problem1':
                self.population.append(Individual(numParticleType           = self.numParticleType,
                                                  latticeLength             = sequenceLength,
                                                  interactionEnergyMatrix   = self.interactionEnergyMatrix,
                                                  selfEnergyVector          = self.selfEnergyVector))
            else:
                self.population.append(Individual(vectorLength=sequenceLength))

        self.averageFitness =   None
        self.bestFitness    =   None
        self.bestIndividual =   None

        self.sequenceLength = sequenceLength

    def __len__(self):
        return len(self.population)

    def __getitem__(self,key):
        return self.population[key]

    def __setitem__(self,key,newValue):
        self.population[key]=newValue

    def copy(self):
        return copy.deepcopy(self)

    def evaluateFitness(self):

        fitnessDistribution = []

        for individual in self.population:
            if self.problemType == 'Problem1':
                individual.evaluateFitness(interactionMatrix = self.interactionEnergyMatrix,
                                           selfEnergyVector  = self.selfEnergyVector)
                fitnessDistribution.append(individual.fit)
            else:
                individual.evaluateFitness()
                fitnessDistribution.append(individual.fit)

        averageFitness = sum(fitnessDistribution)/ len(self.population)

        if self.mode == 'MIN':
            bestFitness = min(fitnessDistribution)
        else:
            bestFitness = max(fitnessDistribution)

        bestFitness_idx = fitnessDistribution.index(bestFitness)

        bestIndividual = self.population[bestFitness_idx].sequence

        self.averageFitness =   averageFitness
        self.bestFitness    =   bestFitness
        self.bestIndividual =   bestIndividual

    def mutate(self):
        for individual in self.population:
            individual.mutate()

    def crossover(self):
        children = []
        indexList1=list(range(len(self.population)))
        indexList2=list(range(len(self.population)))
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)

        if self.crossoverFraction == 1.0:
            for index1,index2 in zip(indexList1,indexList2):
                childx = self.population[index1].crossover(self.population[index2])
                children.append(childx)
        else:
            for index1,index2 in zip(indexList1,indexList2):
                rn= self.uniprng.random()
                if rn <  self.crossoverFraction:
                    childx = self.population[index1].crossover(self.population[index2])
                    children.append(childx)

        # Childrem Compete then Replace some parents.
        for childx in children:
            for idx, parent in enumerate(self.population):
                if self.mode == 'MIN':
                    if childx.fit < parent.fit:
                        self.population[idx] = childx
                        break
                else:
                    if childx.fit > parent.fit:
                        self.population[idx] = childx
                        break


    def conductTournament(self):
        # binary tournament
        indexList1=list(range(len(self.population)))
        indexList2=list(range(len(self.population)))
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)

        # do not allow population competition
        for i in range(len(self.population)):
            if indexList1[i] == indexList2[i]:
                temp=indexList2[i]
                if i == 0:
                    indexList2[i]=indexList2[-1]
                    indexList2[-1]=temp
                else:
                    indexList2[i]=indexList2[i-1]
                    indexList2[i-1]=temp
        #compete
        newPop=[]
        for index1,index2 in zip(indexList1,indexList2):
            if self.mode == 'MIN':
                if self.population[index1].fit < self.population[index2].fit:
                    newPop.append(copy.deepcopy(self.population[index1]))
                elif self.population[index1].fit > self.population[index2].fit:
                    newPop.append(copy.deepcopy(self.population[index2]))
                else:
                    rn= self.uniprng.random()
                    if rn > 0.5:
                        newPop.append(copy.deepcopy(self.population[index1]))
                    else:
                        newPop.append(copy.deepcopy(self.population[index2]))
            else:
                if self.population[index1].fit > self.population[index2].fit:
                    newPop.append(copy.deepcopy(self.population[index1]))
                elif self.population[index1].fit < self.population[index2].fit:
                    newPop.append(copy.deepcopy(self.population[index2]))
                else:
                    rn= self.uniprng.random()
                    if rn > 0.5:
                        newPop.append(copy.deepcopy(self.population[index1]))
                    else:
                        newPop.append(copy.deepcopy(self.population[index2]))

        # overwrite old pop with newPop
        self.population=newPop

    def combinePops(self,otherPop):
        self.population.extend(otherPop.population)

    def truncateSelect(self,newPopSize):
        #sort by fitness
        if self.mode == 'MIN':
            self.population.sort(key=attrgetter('fit'),reverse=False)
        else:
            self.population.sort(key=attrgetter('fit'),reverse=True)

        #then truncate the bottom
        self.population=self.population[:newPopSize]

    def __str__(self):
        return '\n'

    def print_info(self):
        print("--------------------------------[INFO]---------------------------------------------------")
        print(f"MODE:               {self.mode}")
        print(f"ProblemType:        {self.problemType}")
        print(f"Population Size:    {len(self.population)}")
        print(f"CrossOverFraction:  {self.crossoverFraction}")
        print(f"--------------------------------\nFitness Function:\n {self.fitFunc}")

        if self.problemType == 'Problem1':
            print(f"Interaction Matrix:\n{self.interactionEnergyMatrix}")
            print(f"SelfEnergyVector:\n{self.selfEnergyVector}")
            print(f"NumOfParticles: {self.numParticleType}")

        print(f"---------------------------------\nSequenceLength:\n {self.sequenceLength}")
        print("----------------------------------\nPopulation:\n")
        for individual in self.population:
            print(individual.sequence)

        print(f"---------------------------------\nAverage Fitness Of population:\n {self.averageFitness}")
        print(f"bestFitness:\n{self.bestFitness}")
        print(f"bestIndividual:\n{self.bestIndividual}")
