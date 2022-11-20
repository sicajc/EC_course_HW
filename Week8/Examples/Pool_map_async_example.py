import time
from multiprocessing import Pool

class Worker:
    maxIters=3
    @classmethod    
    def compute(cls, sleepTime):
        for i in range(cls.maxIters):
            print('Iterating: ' + sleepTime[0] + ' ' + str(i))
            time.sleep(sleepTime[1]) 
            
        return sleepTime[1]*10
 
if __name__ == '__main__':
    p=Pool(processes=3)
    sleepTimes = [('A',2),('B',1),('C',1),
                  ('D',2),('E',0.5),('F',0.25)]
    #sleepTimes = [('A',2),('B',1),('C',1)]
 
    results=p.map_async(Worker.compute,sleepTimes)
    
    print('Hello from Main!')
    print(results.get(timeout=20))       
    print('Goodbye from Main!')