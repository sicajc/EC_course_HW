import time
from multiprocessing import Pool

class Worker:
    maxIters=3
    @classmethod    
    def compute(cls, label, sleepTime):
        for i in range(cls.maxIters):
            print('Iterating: ' + label + ' ' + str(i))
            time.sleep(sleepTime) 
            
        return sleepTime*10
 
if __name__ == '__main__':
    p=Pool(processes=3)
    sleepTimes = {'A':2,'B':1,'C':1}
 
    results=[p.apply_async(Worker.compute,(st,sleepTimes[st])) for st in sleepTimes]
          
    for result in results:
        print(result.get(timeout=20))       
        
    print('Goodbye from Main!')