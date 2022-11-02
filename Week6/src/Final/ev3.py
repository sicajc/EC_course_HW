#
# ev3.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# To run: python ev3.py --input ev3_example.cfg
#         python ev3.py --input my_params.cfg
#
# Basic features of ev3:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors

import optparse
import sys
from typing import List
from matplotlib import markers
from numpy import linspace
import yaml
import math
from random import Random
from Population import *
from Individual import *
from fitnessFunc import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

#EV3 Config class
class EV3_Config:
    """
    EV3 configuration class
    """
    # class variables
    sectionName='EV3'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'crossoverFraction':(float,True),
             'minLimit': (float,True),
             'maxLimit': (float,True),
             'selfEnergyVector':(list,True),
             'interactionEnergyMatrix':(list,True),
             'sequenceLength':(int,True),
             'numParticleType':(int,True),
             'problemType':(str,True),
             'mode':(str,True)
             }

    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EV3 section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing {} section in cfg file'.format(self.sectionName))

        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt]

                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))

                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self,opt,None)

    #string representation for class data
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))

def plot_graph(filepath,data,generationCount,title):
    plt.title(title)
    plt.plot(generationCount,data)
    plt.savefig(filepath + title +".png")
    plt.show()

#Print some useful stats to screen
def printStats(pop,gen):
    print('Generation:',gen)
    avgval=0
    maxval=pop[0].fit
    sigma=pop[0].sigma
    for ind in pop:
        avgval+=ind.fit
        if ind.fit > maxval:
            maxval=ind.fit
            sigma=ind.sigma
        print(ind)

    print('Max fitness',maxval)
    print('Sigma',sigma)
    print('Avg fitness',avgval/len(pop))
    print('')


#EV3:
#
def ev3(cfg):
    filepath = "Result/"
    #start random number generators
    uniprng=Random()
    uniprng.seed(cfg.randomSeed)
    normprng=Random()
    normprng.seed(cfg.randomSeed+101)

    #set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    Individual.problemType          =   cfg.problemType
    Individual.minLimit             =   cfg.minLimit
    Individual.maxLimit             =   cfg.maxLimit
    Individual.fitFunc              =  CalulateEnergy if cfg.problemType == 'Problem1' else N_Dimensional_Rastrigin

    Individual.uniprng              =   uniprng
    Individual.normprng             =   normprng

    Population.uniprng              =   uniprng
    Population.crossoverFraction    =   cfg.crossoverFraction
    Population.problemType          =   cfg.problemType
    Population.mode                 =   cfg.mode
    Population.numParticleType      =   cfg.numParticleType
    Population.fitFunc              =  CalulateEnergy if cfg.problemType == 'Problem1'else N_Dimensional_Rastrigin

    #For Problem1
    Population.interactionEnergyMatrix = cfg.interactionEnergyMatrix
    Population.selfEnergyVector        = cfg.selfEnergyVector

    #create initial Population (random initialization)
    if cfg.problemType== 'Problem1':
        population = Population(populationSize = cfg.populationSize,
                                sequenceLength = cfg.sequenceLength)
    else:
        population = Population(populationSize= cfg.populationSize,
                                sequenceLength=cfg.sequenceLength)

    generationCountList = []
    bestFitnessList     = []
    bestIndividualx = []
    bestIndividualy = []

    generationCost = 0

    #evolution main loop
    for i in range(cfg.generationCount):
        # Checking when it finds the Optimal solution
        # if population.bestFitness == 41 :
            # generationCost = i
            # break
        if i%500 == 0:
            print(f"Current Generation is: {i}, bestFitness: {population.bestFitness}, bestIndividual: {population.bestIndividual}")
        generationCountList.append(i)
        #create initial offspring population by copying parent pop
        offspring=population.copy()

        #select mating pool
        offspring.conductTournament()

        #perform crossover
        offspring.crossover()

        #random mutation
        offspring.mutate()

        #update fitness values
        offspring.evaluateFitness()

        #survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)
        population.truncateSelect(cfg.populationSize)

        #ReEvaluate population
        population.evaluateFitness()

        bestFitnessList.append(population.bestFitness)
        bestIndividualx.append(population.bestIndividual[0])
        bestIndividualy.append(population.bestIndividual[1])

    population.print_info()

    plot_graph(filepath = filepath,
               generationCount = generationCountList,
               data = bestFitnessList,
               title = f'{population.problemType} with {population.mode} BestFitness')

    # print(f"Generatiion Cost: {generationCost}")

    if population.problemType == 'Problem2':
        x,y = population.bestIndividual
        z   = population.bestFitness
        #Generate 3-D Plot for Rastrigin function and its MIN and MAX
        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(projection='3d')
        fitness =[]
        title = "3-D Rastrigrin Function"

        #Use sampling point to enable better Plot
        x1 = np.arange(cfg.minLimit,cfg.maxLimit,0.01).astype('float16')
        x2 = np.arange(cfg.minLimit,cfg.maxLimit,0.01).astype('float16')

        X, Y = np.meshgrid(x1, x2)
        zs = np.array([N_Dimensional_Rastrigin([x,y]) for x,y in zip(np.ravel(X), np.ravel(Y))])
        zs =zs.reshape(X.shape)

        #Plot function is better
        ax.plot_wireframe(X, Y, zs, cmap = cm.ocean)
        ax.scatter(bestIndividualx,bestIndividualy,bestFitnessList,c = 'r',marker = 'o',s = 200)
        ax.text(x, y, z, population.mode + f'({x:.3},{y:.3},{z:.3})', color='red',size = 50)
        ax.set_title(title)
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")
        #Rotate the figure
        plt.savefig(filepath + title +".png")
        plt.show()

#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)

        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")

        #Get EV3 config params
        cfg=EV3_Config(options.inputFileName)

        #print config params
        print(cfg)

        #run EV3
        ev3(cfg)

        if not options.quietMode:
            print('EV3 Completed!')

    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)



if __name__ == '__main__':
    main()
