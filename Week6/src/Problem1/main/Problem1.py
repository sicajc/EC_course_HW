#
# latticeMinimize.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# To run: python latticeMinimize.py --input lattice_params.cfg
#         python latticeMinimize.py --input my_params.cfg
#
# Basic features of latticeMinimize:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors
#

import optparse
import sys
sys.path.append("../LatticePopulation")
sys.path.append("../QuantumLattice")

from LatticePop import *
from typing import List
import yaml
import math
from random import Random


#LatticeMinimize Config class
class LatticeMin_Config:
    """
    LatticeMinimize configuration class
    """
    # class variables
    sectionName='LatticeMinimize'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'crossoverFraction':(float,True),
             'selfEnergyVector':(list,True),
             'interactionEnergyMatrix':(list,True),
             'latticeLength':(int,True),
             'numParticleType':(int,True),
             'minSigma'  :(float,True),
             'maxSigma'  :(float,True),
             'learningRate' :(float,True)
             }

    #constructor
    def __init__(self, inFileName):
        #read YAML config and get LatticeMinimize section
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


#LatticeMinimize:
#
def latticeMinimize(cfg):
    #start random number generators
    random.seed(cfg.randomSeed)

    #Instantiate classes and set parameters
    LatticePop.minSigma                 = cfg.minSigma
    LatticePop.maxSigma                 = cfg.maxSigma
    LatticePop.numParticleType          = cfg.numParticleType
    LatticePop.crossoverFraction        = cfg.crossoverFraction
    LatticePop.selfEnergyVector         = cfg.selfEnergyVector
    LatticePop.interactionEnergyMatrix  = cfg.interactionEnergyMatrix
    LatticePop.latticeLength            = cfg.latticeLength
    LatticePop.learningRate             = cfg.learningRate

    #create initial Population (random initialization)
    population=LatticePop(populationSize = cfg.populationSize)
    print("Pop Instantiated")
    #print initial pop stats
    #evolution main loop
    for i in range(cfg.generationCount):
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

    population.evaluateFitness()
    print(population)
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

        #Get LatticeMinimize config params
        cfg=LatticeMin_Config(options.inputFileName)

        #print config params
        print(cfg)

        #run LatticeMinimize
        latticeMinimize(cfg)

        if not options.quietMode:
            print('LatticeMinimize Completed!')

    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)


if __name__ == '__main__':
    main()
