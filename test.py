from __future__ import print_function
import time, threading

def thread1():
    print(" fuck");
    time.sleep(5);
    print("you");
    time.sleep(5);
    print("you");


def thread2():
    nxp=raw_input();
    print (nxp);



t1 = threading.Thread(target=thread1);
t2 = threading.Thread(target=thread2);
t1.start();
t2.start();
t1.join();
t2.join();

