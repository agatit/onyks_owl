from multiprocessing import Process, Queue, Array, Manager
from time import sleep

def f(m):
    a = m.image
    print(a)
    sleep(2)    
    a.append("asasd")
    print("wysłano task")

def g(am):
    sleep(4)
    print(a)

if __name__ == '__main__':
    manager = Manager()
    
    a = manager.list()
    d = manager.dict()

    d.append()

    a.append("123")
    p = Process(target=f, args=(manager,))
    p.start()
    r = Process(target=g, args=(manager,))
    r.start()
    
    p.join()    
    r.join()