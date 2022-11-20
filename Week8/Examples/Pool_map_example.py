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
    sleepTimes = [('A',2),('B',1),('C',1)]
 
    results=p.map(Worker.compute,sleepTimes)
    
    print('Hello from Main!')
         
    for result in results:
        print(result)       
        
    print('Goodbye from Main!')