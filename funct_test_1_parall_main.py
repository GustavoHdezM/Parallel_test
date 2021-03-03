# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:25:33 2021

@author: mejia
"""

# import concurrent.futures
import time

# def funct_1(seconds):
#     print(f'Sleeping {seconds} second(s)...')
#     time.sleep(seconds*2)
#     print(f'Done Sleeping...{seconds}')
#     return

global sleep_sec


sleep_sec = 1

def funct_2(seconds):
    seconds =seconds * sleep_sec
    print("Sleeping...")
    return seconds


def funct_1(seconds):
    # print(f'Sleeping {seconds} second(s)...')
    sec = funct_2(seconds)
    time.sleep(sec)
    # print(f'Done Sleeping...{seconds}')
    return 

def do_something(seconds):
    # print(f'Sleeping {seconds} second(s)...')
    # time.sleep(seconds)
    # print(f'Done Sleeping...{seconds}')
    funct_1(seconds)
    return f'Done Sleeping...{seconds}'