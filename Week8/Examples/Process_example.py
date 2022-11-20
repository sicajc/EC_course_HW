import time
from multiprocessing import Process

class Worker:
    maxIters=4
    @classmethod    
    def compute(cls, label, sleepTime):
        for i in range(cls.maxIters):
            print('Iterating: ' + label + ' ' + str(i))
            time.sleep(sleepTime) 
 
if __name__ == '__main__':
    sleepTimes = {'A':1,'B':2,'C':4}
    procs = []
 
    for st in sleepTimes:
        proc = Process(target=Worker.compute, args=(st,sleepTimes[st]))
        procs.append(proc)
        proc.start()
  
    for proc in procs:
        proc.join()
        
    print('Goodbye from Main!')