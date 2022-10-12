# To do list

## To enable self adpative do the following
>1. Remove mutationProb and mutationStddev, they are no longer needed, since a sigma would be added to each individual

>2. The mutation step is determined by $\sigma$, and $\sigma$ would get carried and changed in each mutation for each individual.


>3. Individual shall be modified to have
>* self-adaptive varaible $\sigma$
>* crossover(self,other) -> return new individual
>* mutate(self) the internal state mutation
>* crossOver operator uses stohastic arithmetic crossover.

## Mutation
>1. Pick two parents and then with crossover producing new children and mutate them repetitively for 5 times.

>2. Save these generated new children into a list.

>3. Compete these new children with their parenets.

>4. Run Replace-Worst selection Competing with parent, only 10 individuals survive.

# Testing.
Uses Parabola and Rastrigin function for test.