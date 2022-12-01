# Notes for this week

## Meaning of @classmethod
https://www.zhihu.com/question/49660420
<br /> Allows us to call the function within class using cls variable instead of self, dont need to instantiate the class itself.


## Pool usage and problem when not passing the init value.
1. The process instantiation will not be successful if you dont set the init value of Pool in the correct way.
2. You had better use the following format for reference.
3. The pool initilizer must be instantiated, otherwise the process argument will receive NONE type and behave in an unexpected way.

```python
import time
from multiprocessing import Pool
import os

class Worker:
    maxIters=3
    multiplier=None
    showPid=None

    #This is similar to static method in C++, which allows function to be called without instatantiation
    @classmethod
    def compute(cls, sleepTime):
        for i in range(cls.maxIters):
            print('Iterating: ' + sleepTime[0] + ' ' + str(i))

            #say hello from this worker process?
            if cls.showPid:
                print('Hello from worker process pid:{}!'.format(os.getpid()))

            #sleep for awhile
            time.sleep(sleepTime[1])

        return sleepTime[1]*cls.multiplier


# Helper function to init settable class variables
# This must be set, otherwise the process cannot find the instaitation of objects.
def init_class_vars(cfg):
    Worker.multiplier=cfg['multiplier']
    Worker.showPid=cfg['show_pid']


#Main program
#
if __name__ == '__main__':

    #settable configuration parameters (via a dictionary)
    config_params={'multiplier': 30, 'show_pid': True}

    #Needed for the processes to find the init variables s.t. we can use them.
    p=Pool(initializer=init_class_vars, initargs=(config_params,),processes=3)
    sleepTimes = [('A',2),('B',1),('C',1)]

    results=p.map(Worker.compute,sleepTimes)

    print('Hello from Main!')

    for result in results:
        print(result)

    print('Goodbye from Main!')
```

## Error usage of process Pool
1. Process distributing should be made in main() instead of doing it inside a certain class function, otherwise it would just get destroyed and remake again and again?
2.  You had better not instantiate Pool within the function itself

```python
#Originally In class Population
def evaluateFitness(self):
    #
    #for individual in self.population: individual.evaluateFitness()
    cpus = mp.cpu_count()
    #print(cpus)
    p = mp.Pool(processes = cpus)
    states = [ind.state for ind in self.population]
    fitFunc = self.population[0].__class__.fitFunc
    #ind = self.population
    print(f"State is of type : {type(states)}")
    print(f"Function passed in is of type:{fitFunc}")
    fitnesses = p.map(fitFunc, states) #<- Why NoneType even if the
    p.close()
    p.join()
    for i in range(self.__len__) : self.population[i].fit = fitnesses[i]

```

3. You can actually use map within function as long as Pool is instantiated in a global perspective.
4. So Pool shall be instantiated in global main
5. The reason why we have to pass parameters in is because the individuals are all in another memory chunks.
