#
#Example to demonstrate initialization of class variables
#  when using a Pool of worker processes

# - Notice in the following Worker class, we now have
#    two class variables "multiplier" and "showPid"
#    that can be set at runtime.
# - Worker processes do not share
#    memory or state, so settable class variables must
#    be explicitly initialized on all worker processes
# - Luckily the Pool class has built-in functionality
#    for just this purpose.  We can pass the Pool
#    object an initialization function with parameters
#    when we create the Pool.
#    Example:
#      p=Pool(initializer=some_init_function, initargs=(param1,param2,), processes=4)
#

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