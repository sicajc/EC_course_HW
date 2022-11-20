import time
from multiprocessing import Process,Queue

class Worker:
    maxIters=4
    @classmethod    
    def compute(cls, label, sleepTime,q):
        for i in range(cls.maxIters):
            print('Iterating: ' + label + ' ' + str(i))
            time.sleep(sleepTime) 
            
        q.put('Result from worker ' + str(label))
 
if __name__ == '__main__':
    q=Queue()
    sleepTimes = {'A':2,'B':1,'C':1}
    procs = []
 
    for st in sleepTimes:
        proc = Process(target=Worker.compute, args=(st,sleepTimes[st],q))
        procs.append(proc)
        proc.start()
  
    for proc in procs:
        proc.join()
        
    for proc in procs:
        print(q.get())       
        
    print('Goodbye from Main!')