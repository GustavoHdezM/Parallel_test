# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:25:33 2021

@author: mejia
"""
# from funct_test_1_main import *
import concurrent.futures
import time
from multiprocessing import Pool
# from funct_test_1_main import *

start = time.perf_counter()

def funct_2(seconds):
    seconds =seconds * 1
    return seconds


def funct_1(seconds):
    print(f'Sleeping {seconds} second(s)...')
    sec = funct_2(seconds)
    time.sleep(sec)
    print(f'Done Sleeping...{seconds}')
    return 

def do_something(seconds):
    # print(f'Sleeping {seconds} second(s)...')
    # time.sleep(seconds)
    # print(f'Done Sleeping...{seconds}')
    funct_1(seconds)
    return f'Done Sleeping...{seconds}'
    # return 

if __name__ == '__main__':
    # from funct_test_1_main import *
    secs = [0.8, 1, 0.9, 1.2, 0.1, 1.3, 0.1, 2, 0.3]
    with concurrent.futures.ProcessPoolExecutor(10) as executor:
        
        results = executor.map(do_something, secs)

    with Pool(10) as p:
        # secs = [0.8, 1, 0.9, 1.2, 0.1, 1.3, 0.1, 2, 0.3]
        result = p.map(do_something, secs)
        print(result)
    
    with Pool(10) as p1:
        print()
        result1 = p1.map(do_something, secs)
        print(result1)
        

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')