# %%
import sys
sys.path.insert(0, 'Week6/src/Problem1/QuantumLattice')

from QuantumLattice import QuantumLattice
import copy
from operator import attrgetter
import random

class LatticePop:
    """
    LatticePop
    """
    # uniprng=None
    crossoverFraction=None
    minEnergy = 0

    def __init__(self,
                 populationSize,
                 latticeLength,
                 numParticleType,
                 selfEnergyVector,
                 interactionEnergyMatrix,
                 crossoverFraction):
        """
        LatticePop constructor
        """
        self.population=[]
        self.selfEnergyVector = selfEnergyVector
        self.interactionEnergyMatrix = interactionEnergyMatrix
        self.crossoverFraction = crossoverFraction
        self.minEnergyLattice = []

        for i in range(populationSize):
            self.population.append(QuantumLattice(latticeLength = latticeLength,numParticleType = numParticleType))


    def __len__(self):
        return len(self.population)

    def __getitem__(self,key):
        return self.population[key]

    def __setitem__(self,key,newValue):
        self.population[key]=newValue

    def copy(self):
        return copy.deepcopy(self)

    def evaluateFitness(self):
        #Finding the minimum Energy of Pop and Calculate the Energy for every individuals
        energy_distribution = []

        for individual in self.population:
            individual.evaluateFitness(self.selfEnergyVector,
                                       self.interactionEnergyMatrix)
            energy_distribution.append(individual.energy)

        self.minEnergy = min(energy_distribution)
        minEnergy_idx = energy_distribution.index(self.minEnergy)

        self.minEnergyLattice = self.population[minEnergy_idx].lattice

    # def mutate(self):
        # for individual in self.population:
            # individual.mutate()

    def crossover(self):
        children = []
        indexList1=list(range(len(self)))
        indexList2=list(range(len(self)))
        random.shuffle(indexList1)
        random.shuffle(indexList2)

        #Generate children
        if self.crossoverFraction == 1.0:
            for index1,index2 in zip(indexList1,indexList2):
                childx = self[index1].crossover(self[index2])
                childx.mutate()
                children.append(childx)
        else:
            for index1,index2 in zip(indexList1,indexList2):
                rn=random.random()
                if rn < self.crossoverFraction:
                    childx = self[index1].crossover(self[index2])
                    childx.mutate()
                    children.append(childx)

        #Children has to be evaluated
        for child in children:
            child.evaluateFitness(selfEnergyVector=self.selfEnergyVector,
                                  interactionEnergyMatrix=self.interactionEnergyMatrix)

        #Childrem Compete then Replace some parents.
        for childx in children:
            for idx,parent in enumerate(self.population):
                if childx.energy < parent.energy:
                    self.population[idx] = childx
                    break

    def conductTournament(self):
        # binary tournament, by finding the minEnergy.
        indexList1=list(range(len(self.population)))
        indexList2=list(range(len(self.population)))

        random.shuffle(indexList1)
        random.shuffle(indexList2)

        # do not allow self competition
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
            if self.population[index1].energy < self.population[index2].energy:
                newPop.append(copy.deepcopy(self.population[index1]))
            elif self.population[index1].energy > self.population[index2].energy:
                newPop.append(copy.deepcopy(self.population[index2]))
            else:
                rn=random.random()
                if rn > 0.5:
                    newPop.append(copy.deepcopy(self.population[index1]))
                else:
                    newPop.append(copy.deepcopy(self.population[index2]))

        # overwrite old pop with newPop
        self.population=newPop


    # def combinePops(self,otherPop):
        # self.population.extend(otherPop.population)

    def truncateSelect(self,newPopSize):
        #sort by fitness
        self.population.sort(key=attrgetter('energy'),reverse=True)

        #then truncate the bottom
        self.population=self.population[:newPopSize]

    def __str__(self):
        print("------------------------------\nPopulation [INFO]")
        print(f"\nInteractionMatrix : \n {self.interactionEnergyMatrix}")
        print(f"\nEnergyVector : \n {self.selfEnergyVector}")
        print(f"\nPopulation:\n")
        for individual in self.population:
            print(individual.lattice)
        print(f"\nMinEnergy : \n {self.minEnergy} with lattice {self.minEnergyLattice}")

        return "\n"


# %%
#Testing
# def main():
    # P = 20
    # u = [1,2,3]
    # N = 11
    # t = [[10,4,1],[4,10,5],[1,5,10]]
    # M = 3
    # generations = 10
    # crossoverfraction = 0.2
#
    # Pop = LatticePop(populationSize = P,
                    #  latticeLength = N,
                    #  numParticleType = M,
                    #  selfEnergyVector = u,
                    #  interactionEnergyMatrix = t,
                    #  crossoverFraction = crossoverfraction)
#
    # for _ in range(generations):
        # Pop.crossover()
        # Pop.evaluateFitness()
        # Pop.conductTournament()
        # Pop.evaluateFitness()
#
    # print(Pop)
#
# if __name__ == '__main__':
    # main()
