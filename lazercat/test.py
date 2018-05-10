from stepper2 import printme
from multiprocessing import Process

rocket = 0


def func1():
    global rocket
    print('start func1')
    while rocket < 100000:
        rocket += 1
    print('end func1')


def func2():
    global rocket
    print('start func2')
    while rocket < 10000:
        rocket += 1
    print('end func2')


if __name__ == '__main__':
    p1 = Process(target=func1)
    p2 = Process(target=func2)
    p1.start()
    p2.start()


printme();

