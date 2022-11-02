# Multi-objective binary-tournament selection

## Notes:
1. In this code we will simplify things a bit by assuming that
         minimization is desired for all objectives (in the more general
         case you could have a mix of minimization and maximization on various objectives.)

2. As an example test case, we will use Deb's Min-Ex function here.
         Min-Ex State is 2-D real, with 2 minimization objectives.

## Instructions for this assignment:
  1. Implement Individual.dominates method
  2. Implement Individual.compareRankAndCrowding method
  3. Implement Population.computeFrontRanks method
  4. Implement Population.binaryTournament method
  5. Run experiments and examine resulting data plots, do they make sense?

## Code structure
``` mermaid
classDiagram

    BinaryTournament <|-- Population
    Population -- MinExInitializer
    Population --  Individual

    class BinaryTournament{
        Multi-Objective BinaryTournament Selection
    }


    class Population{
      -list Individual pop = []

      -computeCrowding(self)
      -computeFrontRanks(self)
      -updateRanking(self)
      -binaryTournament(self,prng)
      -generatePlots(self,title=None,showScreen=True,saveToFile=False,fileName=None)
    }
    class Individual{
      -list float state = []
      -list str objectives = []
      -int  numObj
      -int  frontRank
      -int  crowdDist

      -dominates(self,others)
      -compareRankAndCrowding(self, other)
      -distance(self,other,normalizationVec=[None])
    }
    class MinExInitializer{
        Generate Random Pop for population with Individual
    }

```
# Implementation
> Details in jupyter Notebook

## Prerequisite
  1. We must first understand what Optimal Pareto front is, and what it means by domination and non-domination sets.
  2. How to segregate non-domination sets and determine the ranking of those pareto fronts.

## Pareto Optimal Concept with example.
https://www.youtube.com/watch?v=Hm2LK4vJzRw&list=PLbRMhDVUMnge0CU8o2gWwKXANADrpTc1q&index=40

## NSGA-II Example
https://www.youtube.com/watch?v=Yb82W2Bolqc&list=PLbRMhDVUMnge0CU8o2gWwKXANADrpTc1q&index=41

## Procedures
  1. Random generate objective Individual list for Population
  2. Determine the domination relationship of each individual
  3. Generate and then assign the rank for each individual using the domination relationship of each individual
  4. From rank, conduct the binary tournament, the one with lowest rank will eventually survive.
  5. Distance function compute the relative distance of a specific front
  6. From the rank and crowding distance of each individual, select the individual with the lower rank and larger crowding distance (higher diversity)
  7. Repeats from 2 until running out of generation counts.