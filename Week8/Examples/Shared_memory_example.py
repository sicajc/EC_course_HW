import time
from multiprocessing import Process, Lock, Value, Array

class Worker:
    maxIters=4
    @classmethod
    def compute(cls, label, sleepTime, n, v): #What is this cls? why is it needed?
        for i in range(cls.maxIters):
            print('Iterating: ' + label + ' ' + str(i))
            time.sleep(sleepTime)
        n.value=sleepTime*10; v[0]=sleepTime*10.0; v[1]=sleepTime*20.0

if __name__ == '__main__':
    sleepTimes = {'A':4,'B':1}
    procs = []; lock = Lock()

    n = Value('i', -99, lock=lock)
    v = Array('d', [1.23,4.56,7.89], lock=lock)

    print('n=',n.value); print('v=',list(v))
    for st in sleepTimes:
        proc = Process(target=Worker.compute, args=(st,sleepTimes[st],n,v))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print('n=',n.value); print('v=',list(v))
    print('Goodbye from Main!')