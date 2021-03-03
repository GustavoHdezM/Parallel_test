# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:25:33 2021

@author: mejia
"""
# from funct_test_1_main import *
import concurrent.futures
import time
from multiprocessing import Pool
from funct_test_1_parall_main import *

start = time.perf_counter()
global sleep_sec


if __name__ == '__main__':
    # from funct_test_1_main import *
    secs = [0.8, 1, 2, .2, 0.1, .3, 0.1, 2, 0.3, 0.9]
    # with concurrent.futures.ProcessPoolExecutor(10) as executor:
    #     results = executor.map(do_something, secs)

    with Pool(10) as p:
        # secs = [0.8, 1, 0.9, 1.2, 0.1, 1.3, 0.1, 2, 0.3]
        result = p.map(do_something, secs)
        print("\np")
        print(result)
        
    
    with Pool(10) as p1:
        print()
        print("\np1")
        result1 = p1.map(do_something, secs)
        print(result1)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')