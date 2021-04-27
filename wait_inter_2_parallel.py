# -*- coding: utf-8 -*-
"""
Model Agents for Emergency department

Shared with Victoria Tomori 03.02.2021

@author: Gustavo"""

from funct_interv_2_parallel import *
import concurrent.futures



t1 = time.perf_counter()

if __name__ == '__main__': 
    save_results = []
    with concurrent.futures.ProcessPoolExecutor() as executor: 
        future_results =  [executor.submit(big_func)for _ in range(100)]
        for fut in concurrent.futures.as_completed(future_results):
            #print(fut.result())
            print(fut.done())
            save_results.append(fut.result())#
            counter=0
            for i in save_results:
                from collections import Counter
                with open('Test6/reesult/Result'+str(counter)+'.txt', 'w') as f:
                    wr = csv.writer(f,delimiter=":")
                    wr.writerows(Counter(i).items())
                    counter = counter + 1
            
        t2 = time.perf_counter()
            
        print("finished in " + str(round((t2-t1)/60,2))   + " minute(s)")         
            

#t1 = time.perf_counter()
#if __name__ == '__main__': 
#    ex = concurrent.futures.ProcessPoolExecutor(max_workers=2)
#    print('main: starting')
#    
#    wait_for = [ex.submit(big_func)for _ in range(9)]
#    
#    for f in concurrent.futures.as_completed(wait_for):
#        print(f.result())
#        t2 = time.perf_counter()
#                
#        print("finished in " + str(round((t2-t1)/60,2))   + " minute(s)")         
#                

