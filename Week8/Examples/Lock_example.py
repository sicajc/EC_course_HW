import time
from multiprocessing import Process,Lock

class Worker:
    maxIters=4
    @classmethod    
    def compute(cls, label, sleepTime,lck):
        lck.acquire()
        try:
            for i in range(cls.maxIters):
                print('Iterating: ' + label + ' ' + str(i))
                time.sleep(sleepTime)
        finally:
            lck.release()
             
if __name__ == '__main__':
    lck=Lock()
    sleepTimes = {'A':1,'B':1,'C':1}
    procs = []
 
    for st in sleepTimes:
        proc = Process(target=Worker.compute, args=(st,sleepTimes[st],lck))
        procs.append(proc)
        proc.start()
  
    for proc in procs:
        proc.join()
        
    print('Goodbye from Main!')