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
## Individual.Dominates()
  Compares two individuals based on multi-objective dominance

## Prerequisite
  1. We must first understand what Optimal Pareto front is, and what it means by domination and non-domination sets.
  2. How to segregate non-domination sets and determine the ranking of those pareto fronts.

## Pareto Optimal Concept with example.
https://www.youtube.com/watch?v=Hm2LK4vJzRw&list=PLbRMhDVUMnge0CU8o2gWwKXANADrpTc1q&index=40

## NSGA-II Example
https://www.youtube.com/watch?v=Yb82W2Bolqc&list=PLbRMhDVUMnge0CU8o2gWwKXANADrpTc1q&index=41

##