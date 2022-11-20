import time
from multiprocessing import Process, Manager

class Worker:
    maxIters=2
    @classmethod    
    def compute(cls, label, sleepTime, l, d):
        for i in range(cls.maxIters):
            print('Iterating: ' + label + ' ' + str(i))
            time.sleep(sleepTime)
        l.append(label); d[label]=sleepTime
 
if __name__ == '__main__':
    sleepTimes = {'A':0.5,'B':1,'C':0.25,'D':0.4}
    procs = []
    mgr=Manager()
    l=mgr.list()
    d=mgr.dict()

    print('l=',l); print('d=',d)
    for st in sleepTimes:
        proc = Process(target=Worker.compute, args=(st,sleepTimes[st],l,d))
        procs.append(proc)
        proc.start()
  
    for proc in procs:
        proc.join()

    print('l=',l); print('d=',d)
    print('Goodbye from Main!')
    