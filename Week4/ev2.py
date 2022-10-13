#
# ev2.py: Self-adaptive version of ev1/py
#
# To run: python ev2.py --input ev2.cfg
#
#

import optparse
import sys
from typing import Tuple
from cv2 import exp
from sympy import cos
import yaml
import math
from random import Random
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat


#EV1 Config file class, used to process input data, simple checking that file is there, and error checking
#But in practice we actually use the config file library.
#Actually using the config parser is more convenient

class EV1_Config:
    """
    EV1 configuration class
    """
    # class variables
    sectionName='EV1'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'minLimit': (float,True),
             'maxLimit': (float,True)
            # , 'mutationProb': (float,True),
            #  'mutationStddev': (float,True)
            }

    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing EV1 section in cfg file')

        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt] #Option variable

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


#Simple 1-D fitness function example, solving parabolic equations problems. Finding the max of function
#Also the x s.t. it gets the global maxima.
def fitnessFunc(x):
    result = 50.0 - x*x
    # result = -10 - (0.04*x)**2 + 10 * np.cos(0.04*np.pi*x)
    #print(f"fitness result {result}")
    return result

#Find index of worst individual in population
def findWorstIndex(l):
    minval=l[0].fit
    imin=0
    for i in range(len(l)):
        if l[i].fit < minval:
            minval=l[i].fit
            imin=i
    return imin

#Print some useful stats to screen
def printStats(pop,gen):
    popFitness    = []

    print('Generation:',gen)
    avgval=0
    maxval=pop[0].fit
    maxval_x=pop[0].x
    for p in pop:
        avgval+=p.fit
        if p.fit > maxval:
            maxval=p.fit
            maxval_x = p.x

        print(str(p.x)+'\t'+str(p.fit))
        popFitness.append(p.fit)

    print('Max fitness',maxval)
    print('Avg fitness',avgval/len(pop))
    print('')

    generationSTD = stat.stdev(popFitness)
    generationAVG = stat.mean(popFitness)
    bestFitness   = maxval
    stateValue    = maxval_x

    return generationSTD,generationAVG,bestFitness,stateValue

#Modified individual class
class Individual:
    def __init__(self,x=0,fit=0,sigma = 1,tau = 0.3,sigma_max = 30,sigma_min = 0):
        self.x=x
        self.fit=fit
        self.sigma = sigma
        self.tau = tau
        self.sigma_max = sigma_max
        self.sigma_min = sigma_min

    def crossover(self,other):
        alpha = np.random.uniform(0,1)
        #print(f"Alpha = {alpha}")
        x_new = self.x * alpha + (1 - alpha) * other.x

        return Individual(
            x = x_new,
            fit = self.fit,
            sigma = self.sigma,
            tau = self.tau,
            sigma_max = self.sigma_max,
            sigma_min = self.sigma_min
        )

    def mutate(self):
        #Mutate sigma first.
        sigma_new = self.sigma * exp(self.tau * np.random.normal(0,1))
        #Normal distribution generate a bunch of vectors in numpy array form
        #So we extract the float element out.
        sigma_new = sigma_new[0][0]

        #Sigma has to lie in the bound
        if sigma_new > self.sigma_max:
            sigma_new = self.sigma_max
        elif sigma_new < self.sigma_min:
            sigma_new = self.sigma_min

        #mutate x
        x_new = self.x + sigma_new * np.random.normal(0,1)

        #Update sigma and x
        self.x = x_new
        self.sigma = sigma_new

#EV2: Modified from EV1 with self-adaptive mutation
#
def ev2(cfg):
    POP_SIZE = 10
    TAU = 1/POP_SIZE**(1/2)
    SIGMA_MAX = 10
    SIGMA_MIN = 0

    generationCount = []
    bestFitness     = []
    stateValue      = []
    genSTD          = []
    genAVG          = []

    # start random number generator
    prng=Random()
    prng.seed(cfg.randomSeed)

    #random initialization of population
    population=[]
    for i in range(cfg.populationSize):
        x=prng.uniform(cfg.minLimit,cfg.maxLimit)
        #Each individual has each unique sigma to start with
        sigma = np.random.uniform(0,5)
        #print(f"sigma for each individual {i} is {sigma}")
        ind=Individual(x = x,
                       fit = fitnessFunc(x),
                       sigma = sigma,
                       tau = TAU,
                       sigma_min =SIGMA_MIN,
                       sigma_max = SIGMA_MAX)
        population.append(ind)

    #print stats
    printStats(population,0)

    #Evolution main loop
    for i in range(cfg.generationCount):
        #Randomly select two parents from population
        parents=prng.sample(population,2)

        #Create 5 children per generation
        #Compare each newly generated child with the group.
        for _ in range(5):
        #Create new child using crossover function from individual
            childnew = parents[0].crossover(parents[1])
            #print("CrossOver")

        #Mutate the child.
            childnew.mutate()
            #print("Mutated")
        #Survivor selection: replace the worst inside population,
        #For each newly generated child of the 5 children
        #Compare it with the parents immediatly after born.
            child=Individual(childnew.x,fitnessFunc(childnew.x))
            print(f"Fit calculated, fit result is : {child.fit}")

            iworst=findWorstIndex(population)
            if child.fit > population[iworst].fit:
                population[iworst]=child

        #print stats, visualize and get the std and avg of each iteration
        generationSTD,generationAvg,bestFit,stateVal = printStats(population,i+1)

        genSTD.append(generationSTD)
        genAVG.append(generationAvg)
        stateValue.append(stateVal)
        bestFitness.append(bestFit)
        generationCount.append(i)

    return generationCount,bestFitness,stateValue,genSTD,genAVG


def plot_graph(data,generationCount,title):
    plt.title(title)
    plt.plot(data,generationCount)
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
        # Command line usage
        parser = optparse.OptionParser()
        #Add the -i option for input file into the command line.
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)

        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")

        #Get EV1 config params
        cfg=EV1_Config(options.inputFileName)

        filepath = "ParabolaResult/"
        #filepath = "RastriginResult/"

        #print config params
        print(cfg)

        #run EV1
        generationCount,bestFitness,stateValue,genSTD,genAVG = ev2(cfg)

        #Plot Fitness
        x = np.arange(-100,100,0.1)
        plt.title("Fitness Funciton")
        plt.plot(x,fitnessFunc(x))
        plt.savefig(filepath + "Parabola.png")
        plt.show()

        #Plot fitness and state Value v.s. generation
        print(len(bestFitness),len(stateValue))
        plt.title("Fitness and state value v.s. generation")
        plt.plot(generationCount,bestFitness)
        plt.plot(generationCount,stateValue)
        plt.legend(["Best Fitness","StateValue"])
        plt.savefig(filepath + "Fitness and state value v.s. generation.png")
        plt.show()

        #Plot genSTD and genAVG v.s. generation
        plt.title("STD and AVG of each generation v.s. generation")
        plt.plot(generationCount,genSTD)
        plt.plot(generationCount,genAVG)
        plt.legend(["Generation STD","Generation Average"])
        plt.savefig(filepath + "STD and AVG of each generation v.s. generation.png")
        plt.show()

        if not options.quietMode:
            print('EV1 Completed!')

    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)

if __name__ == '__main__':
    main()
