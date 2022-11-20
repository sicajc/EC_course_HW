#
#Example: Modifying object state in worker processes
#
from multiprocessing import Process

class SomeObject:
    def __init__(self,x):
        self.x=x    

class Worker:
    @classmethod    
    def modify_obj(cls, obj):
        #modify the value of self.x on obj
        obj.x='new_x_value'
        
        #print out the current (modified) obj
        print('Worker object self.x={}'.format(obj.x))
 
if __name__ == '__main__':
    
    #first create object in host process
    host_obj=SomeObject('old_x_value')
    
    #pass object to worker process and modify self.x value
    proc = Process(target=Worker.modify_obj, args=(host_obj,))
    proc.start()
  
    #wait for worker process to finish
    proc.join()
    
    #let's take a look at self.x value for our host object
    print('Host object self.x={}'.format(host_obj.x))
    
    #...interesting, the host object's state value didn't change
    #
    #That's because only a copy of the host object was passed to the worker process
    #  (remember, host and worker processes do not share memory).
    #  If we want to get the changed object state back, we must explicitly communicate it back
    #  to the host process either as a return value, or using shared or managed variables/objects
        
    print('Goodbye from Main!')