# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4  2021

Paral 365 days
      250 patients per day
      

@author: Gustavo Hernandez-Mejia
         WWU Institute of Epidemiology
         Karch Group
"""

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import os
import math 
from multiprocessing import Pool
# from funct_parall_main_ED_1 import *

start = time.perf_counter()
global sleep_sec
global origin_path, Newfolder

Newfolder = 'Res_3'

def funct_isolat(P_R,j): 
#    day_current = day
    Inf_test = random.random() < Suspicion_of_infection # Is there a test? Suspicion of infection?
    if Inf_test:
        Isolation = random.random() < Isolation_needed     # ISOLATION NEEDED?
        if Isolation:
            Users[j][1] = 1
            Next_ED = ISOLA
            Users[j][2] = ISOLA 
            Users[j][9] = ISOLA 
            User_track_1.append([j+1, Users[j][1], Users[j][2],
                                                         0])
        else:
            Next_ED = RECEP
            Users[j][2] = RECEP     # AREA ASIGNATION
            RECEP_t = random.randint(5, 10)
            Users[j][3] = RECEP_t
            Users[j][6] = random.randint(1, RECEP_t)
            User_track_1.append([j+1, Users[j][1], Users[j][2],
                                                         Users[j][3]])
    else:
        Next_ED = RECEP
        Users[j][2] = RECEP     # AREA ASIGNATION
        RECEP_t = random.randint(5, 10)
        Users[j][3] = RECEP_t
        Users[j][6] = random.randint(1, RECEP_t)
        User_track_1.append([j+1, Users[j][1], Users[j][2],
                                                         Users[j][3]])

    return Next_ED

def entrance_routine(time):
    Time_var = time
    for j in range(Num_Aget):
        if Time_var == Users[j][5]:
            Own = random.random() < Own_Arrive
            if Own:
                if Isolation_room:
    #                        if day > 0:
    #                            print(day)
                    funct_isolat(Users[j],j)
                    # print("Isolation")
                else:
                    Users[j][2] = RECEP     # AREA ASIGNATION
                    RECEP_t = random.randint(5, 10)
                    Users[j][3] = RECEP_t
                    Users[j][6] = random.randint(1, RECEP_t)
                    User_track_1.append([j+1, Users[j][1], Users[j][2],
                                                         Users[j][3]])
            else: 
                Users[j][2] = TRIAG_U   # AREA ASIGNATION
                TRIAG_U_t = random.randint(5, 15)
                Users[j][3] = TRIAG_U_t
                Users[j][6] = random.randint(1, TRIAG_U_t)
                User_track_1.append([j+1, Users[j][1], Users[j][2],
                                                         Users[j][3]])
    return

def area_desit_tree(agent,i):   
#    day = da        
    Curr_Area = agent[2]
    
    if RECEP == Curr_Area:
        Next_Area = TRIAG
        Users[i][2] = Next_Area
        t_triage = random.randint(5, 15)
        Users[i][3] = t_triage
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_triage)
    
    if TRIAG == Curr_Area:
        Next_Area = WAI_N
        Users[i][2] = Next_Area
        t_wait_Nu = random.randint(20, 3*60)
        Users[i][3] = t_wait_Nu
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_wait_Nu)
    
    if TRIAG_U == Curr_Area:
        Next_Area = WAI_U
        Users[i][2] = Next_Area
        t_wait_Ur = random.randint(1, 30)
        Users[i][3] = t_wait_Ur
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_wait_Ur)
        
    if WAI_U == Curr_Area:
        Next_Area = AT_UR  # U_URG
        Users[i][2] = Next_Area
        t_Urgent = random.randint(90, 4*60)
        Users[i][3] = t_Urgent
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_Urgent)
        
        
    if WAI_N == Curr_Area:
        Next_Area = At_NU  # N_URG
        Users[i][2] = Next_Area
        t_N_Urgen = random.randint(30, 4*60)
        Users[i][3] = t_N_Urgen
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_N_Urgen)
        
#------------------------------------------------------------------------------    
      # To unseat patient once in attention services
#        ind = [(index, row.index(Users[i][0])) for index, row in enumerate(Seat_map) if (Users[i][0]) in row]
        ind = np.where(Seat_map == Users[i][0])
        Seat_map[ind[0], ind[1]] = 0
#------------------------------------------------------------------------------    
        
    if At_NU == Curr_Area or AT_UR == Curr_Area:
        Next_Area = EXIT_
        Users[i][2] = Next_Area
        # t_N_Urgen = random.randint(40, 2*60)
        Users[i][3] = 0
        Users[i][4] = 0
        
    
    
    return agent

def med_test_funct(agent,i, day):
    day_current = day
    Immagin = random.random() < 0.5
    t_med_test = random.randint(1, 20)
    agent[8] = agent[2]
    # Users[i][3] = t_med_test
    agent[7] = agent[6] + t_med_test
    if Immagin:
        agent[2] = IMAGI
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        
        for i in range(imagi_N):
                if (agent[1] == 1):                       # Agent infected
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D and V_imagin[i][6] == 0:
                        if V_imagin[i][1] == 0:
#                            V_imagin[i][1] = 1        # Worker potential infection
                            V_imagin[i][3] = day_current + 1
                            V_imagin[i][5] = PATIEN
                            V_imagin[i][6] = day_current + 1 
#                            print("worker:",V_imagin[i])
#                            print("Area:",agent[2])
                elif V_imagin[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
#                            print("agent:",agent)
#                            print("Area:",agent[2])
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = STAFF_1
    else:    
        agent[2] = LABOR 
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        for i in range(labor_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_labor[i][1] == 0 and V_labor[i][6] == 0:
#                        V_labor[i][1] = 1        # Worker potential infection
                        V_labor[i][3] = day_current + 1 
                        V_labor[i][5] = PATIEN
                        V_labor[i][6] = day_current + 1 
#                        print("worker:",V_labor[i])
#                        print("Area:",agent[2])
            elif V_labor[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",agent[2])
                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
#    invasi_emerg = random.random() < invasiv_prob
#    if invasi_emerg:
#        invasi_emerg_funct(agent,i)
    return

def med_test_funct_2(agent,i, day): 
    day_current = day
    Immagin = random.random() < 0.5
    t_med_test = random.randint(1, 20)
    agent[8] = agent[2]
    # Users[i][3] = t_med_test
    agent[7] = agent[6] + t_med_test
    if Immagin:
        agent[2] = IMAGI
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        
        for i in range(imagi_N):
                if (agent[1] == 1):                       # Agent infected
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D and V_imagin_2[i][6] == 0:
                        if V_imagin_2[i][1] == 0:
#                            V_imagin[i][1] = 1        # Worker potential infection
                            V_imagin_2[i][3] = day_current + 1
                            V_imagin_2[i][5] = PATIEN
                            V_imagin_2[i][6] = day_current + 1 
#                            print("worker:",V_imagin[i])
#                            print("Area:",agent[2])
                elif V_imagin_2[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
#                            print("agent:",agent)
#                            print("Area:",agent[2])
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = STAFF_2
    else:    
        agent[2] = LABOR 
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        for i in range(labor_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_labor_2[i][1] == 0 and V_labor_2[i][6] == 0:
#                        V_labor[i][1] = 1        # Worker potential infection
                        V_labor_2[i][3] = day_current + 1 
                        V_labor_2[i][5] = PATIEN
                        V_labor_2[i][6] = day_current + 1 
#                        print("worker:",V_labor[i])
#                        print("Area:",agent[2])
            elif V_labor_2[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",agent[2])
                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2

    return

def med_test_funct_3(agent,i, day):
    day_current = day
    Immagin = random.random() < 0.5
    t_med_test = random.randint(1, 20)
    agent[8] = agent[2]
    # Users[i][3] = t_med_test
    agent[7] = agent[6] + t_med_test
    if Immagin:
        agent[2] = IMAGI
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        
        for i in range(imagi_N):
                if (agent[1] == 1):                       # Agent infected
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D and V_imagin_3[i][6] == 0:
                        if V_imagin_3[i][1] == 0:
#                            V_imagin[i][1] = 1        # Worker potential infection
                            V_imagin_3[i][3] = day_current + 1
                            V_imagin_3[i][5] = PATIEN
                            V_imagin_3[i][6] = day_current + 1 
#                            print("worker:",V_imagin[i])
#                            print("Area:",agent[2])
                elif V_imagin_3[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
#                            print("agent:",agent)
#                            print("Area:",agent[2])
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = STAFF_3
    else:    
        agent[2] = LABOR 
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        for i in range(labor_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_labor_3[i][1] == 0 and V_labor_3[i][6] == 0:
#                        V_labor[i][1] = 1        # Worker potential infection
                        V_labor_3[i][3] = day_current + 1 
                        V_labor_3[i][5] = PATIEN
                        V_labor_3[i][6] = day_current + 1 
#                        print("worker:",V_labor[i])
#                        print("Area:",agent[2])
            elif V_labor_3[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",agent[2])
                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3

    return

def action_desit_tree(agent,i, da):    
    Curr_Area = agent[2]
    day_current = da     
    # interact_event = agent[6]
    # current_time = agent[4]
    
    
    if RECEP == Curr_Area:
        # if interact_event == current_time:
        for i in range(recep_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if V_recep[i][1] == 0 and V_recep[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_recep[i][3] = day_current + 1 
                        V_recep[i][5] = PATIEN
                        V_recep[i][6] = day_current + 1 
                        
#                        V_recep[i][9] = Curr_Area
#                        print("worker:",V_recep[i])
#                        print("Area:",Curr_Area)
            elif V_recep[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
    
    if TRIAG == Curr_Area:
        for i in range(triag_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if V_triag[i][1] == 0 and V_triag[i][6] == 0:
#                        V_triag[i][1] = 1        # Worker potential infection
                        V_triag[i][3] = day_current + 1 
                        V_triag[i][5] = PATIEN
                        V_triag[i][6] = day_current + 1 
#                        V_triag[i][9] = Curr_Area
#                        print("worker:",V_triag[i])
#                        print("Area:",Curr_Area)
            elif V_triag[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
    
    if TRIAG_U == Curr_Area:
        for i in range(triag_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if V_triag_U[i][1] == 0 and V_triag_U[i][6] == 0:
#                        V_triag_U[i][1] = 1        # Worker potential infection
                        V_triag_U[i][3] = day_current + 1 
                        V_triag_U[i][5] = PATIEN
                        V_triag_U[i][6] = day_current + 1 
#                        print("worker:",V_triag_U[i])
#                        print("Area:",Curr_Area)
            elif V_triag_U[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
#        invasi_emerg = random.random() < invasiv_prob
#        if invasi_emerg:
#            invasi_emerg_funct(agent,i)
        
    if WAI_U == Curr_Area:
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_U # Risk per area
                Dt_wa_u = random.randint(40, 120)
        
    if WAI_N == Curr_Area:
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_N # Risk per area
#                if Trnasmiss:
    
    
    if AT_UR == Curr_Area:
        #    Nurses Urgent Area
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_nurse_Urg[i][1] == 0  and V_nurse_Urg[i][6] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
                        V_nurse_Urg[i][3] = day_current + 1 
                        V_nurse_Urg[i][5] = PATIEN
                        V_nurse_Urg[i][6] = day_current + 1 
#                        print("worker:",V_nurse_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_Urg[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
                Dt_urge = random.randint(20, 80)
                Trnasmiss = random.random() < PB_URGE # Risk per area
                if Trnasmiss and Dt_urge < M_D and V_dr_Urg[0][5] == UNDEF: 
                    if V_dr_Urg[0][1] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg[0][3] = day_current + 1    
                        V_dr_Urg[0][5] = N_URGE
                        V_dr_Urg[0][6] = day_current + 1 
                        
                    
        #    physician Urgent Area
        for i in range(Dr_Ur_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_dr_Urg[i][1] == 0 and V_dr_Urg[i][6] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg[i][3] = day_current + 1 
                        V_dr_Urg[i][5] = PATIEN
                        V_dr_Urg[i][6] = day_current + 1 
#                        print("worker:",V_dr_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_dr_Urg[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < PB_URGE # Risk per area
                    Dt_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_urge < M_D and V_nurse_Urg[j][5] == UNDEF:
                        if V_nurse_Urg[j][1] == 0:
                            V_nurse_Urg[j][3] = day_current + 1     
                            V_nurse_Urg[j][5] = DR_URGE
                            V_nurse_Urg[i][6] = day_current + 1                  
                        
                        
        # med_test = random.random() < Medic_test
        # if med_test:
        #     med_test_funct(agent,i, da)
            
        
    if At_NU == Curr_Area:  
        #    Nurses Non-Urgent Area
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_nurse_No_Urg[i][1] == 0 and V_nurse_No_Urg[i][6] == 0:
                        V_nurse_No_Urg[i][3] = day_current + 1
                        V_nurse_No_Urg[i][5] = PATIEN
                        V_nurse_No_Urg[i][6] = day_current + 1 
#                        V_nurse_No_Urg[i][1] = 1        # Worker potential infection
#                        print("worker:",V_nurse_No_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_No_Urg[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D and dr_No_Urg_V[0][5] == UNDEF:
                    if dr_No_Urg_V[0][1] == 0:
                        dr_No_Urg_V[0][3] = day_current + 1
                        dr_No_Urg_V[0][5] = N_N_URG
                        dr_No_Urg_V[0][6] = day_current + 1 
                        
                        
        #    physician Non-Urgent Area
        for i in range(Dr_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if dr_No_Urg_V[i][1] == 0 and dr_No_Urg_V[i][6] == 0:
#                        dr_No_Urg_V[i][1] = 1        # Worker potential infection
                        dr_No_Urg_V[i][3] = day_current + 1 
                        dr_No_Urg_V[i][5] = PATIEN
                        dr_No_Urg_V[i][6] = day_current + 1 
#                        print("worker:",dr_No_Urg_V[i])
#                        print("Area:",Curr_Area)
            elif dr_No_Urg_V[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_1
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < P_N_URE # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if V_nurse_No_Urg[j][1] == 0 and V_nurse_No_Urg[j][5] == UNDEF:
                            V_nurse_No_Urg[j][3] = day_current + 1     
                            V_nurse_No_Urg[j][5] = D_N_URG
                            V_nurse_No_Urg[j][6] = day_current + 1 
            
            # med_test = random.random() < Medic_test
            # if med_test:
            #     med_test_funct(agent,i, da)

    return agent


def action_desit_tree_2(agent,i, da):    
    Curr_Area = agent[2]
    day_current = da     

    if RECEP == Curr_Area:
        # if interact_event == current_time:
        for i in range(recep_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_recep_2[i][3] = day_current + 1 
                        V_recep_2[i][5] = PATIEN
                        V_recep_2[i][6] = day_current + 1 
                        
#                        V_recep[i][9] = Curr_Area
#                        print("worker:",V_recep[i])
#                        print("Area:",Curr_Area)
            elif V_recep_2[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
    
    if TRIAG == Curr_Area:
        for i in range(triag_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if V_triag_2[i][1] == 0 and V_triag_2[i][6] == 0:
#                        V_triag[i][1] = 1        # Worker potential infection
                        V_triag_2[i][3] = day_current + 1 
                        V_triag_2[i][5] = PATIEN
                        V_triag_2[i][6] = day_current + 1 
#                        V_triag[i][9] = Curr_Area
#                        print("worker:",V_triag[i])
#                        print("Area:",Curr_Area)
            elif V_triag_2[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
                        
    if TRIAG_U == Curr_Area:
        for i in range(triag_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if V_triag_U_2[i][1] == 0 and V_triag_U_2[i][6] == 0:
#                        V_triag_U[i][1] = 1        # Worker potential infection
                        V_triag_U_2[i][3] = day_current + 1 
                        V_triag_U_2[i][5] = PATIEN
                        V_triag_U_2[i][6] = day_current + 1 
#                        print("worker:",V_triag_U[i])
#                        print("Area:",Curr_Area)
            elif V_triag_U_2[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
#        invasi_emerg = random.random() < invasiv_prob
#        if invasi_emerg:
#            invasi_emerg_funct(agent,i)
        
    if WAI_U == Curr_Area:
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_U # Risk per area
                Dt_wa_u = random.randint(40, 120)

        
    if WAI_N == Curr_Area:
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_N # Risk per area

    
    
    if AT_UR == Curr_Area:
        #    Nurses Urgent Area
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_nurse_Urg_2[i][1] == 0  and V_nurse_Urg_2[i][6] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
                        V_nurse_Urg_2[i][3] = day_current + 1 
                        V_nurse_Urg_2[i][5] = PATIEN
                        V_nurse_Urg_2[i][6] = day_current + 1 
#                        print("worker:",V_nurse_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
                Dt_urge = random.randint(20, 80)
                Trnasmiss = random.random() < PB_URGE # Risk per area
                if Trnasmiss and Dt_urge < M_D and V_dr_Urg_2[0][5] == UNDEF: 
                    if V_dr_Urg_2[0][1] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_2[0][3] = day_current + 1    
                        V_dr_Urg_2[0][5] = N_URGE
                        V_dr_Urg_2[0][6] = day_current + 1 
                        
                    
        #    physician Urgent Area
        for i in range(Dr_Ur_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_dr_Urg_2[i][1] == 0 and V_dr_Urg_2[i][6] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_2[i][3] = day_current + 1 
                        V_dr_Urg_2[i][5] = PATIEN
                        V_dr_Urg_2[i][6] = day_current + 1 
#                        print("worker:",V_dr_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_dr_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < PB_URGE # Risk per area
                    Dt_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_urge < M_D and V_nurse_Urg_2[j][5] == UNDEF:
                        if V_nurse_Urg_2[j][1] == 0:
                            V_nurse_Urg_2[j][3] = day_current + 1     
                            V_nurse_Urg_2[j][5] = DR_URGE
                            V_nurse_Urg_2[i][6] = day_current + 1 
                        
                        
                        
        med_test = random.random() < Medic_test
        if med_test:
            med_test_funct_2(agent,i, da)
            
#        invasi_emerg = random.random() < invasiv_prob

            
        
    if At_NU == Curr_Area:  
        #    Nurses Non-Urgent Area
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
                        V_nurse_No_Urg_2[i][3] = day_current + 1
                        V_nurse_No_Urg_2[i][5] = PATIEN
                        V_nurse_No_Urg_2[i][6] = day_current + 1 
#                        V_nurse_No_Urg[i][1] = 1        # Worker potential infection
#                        print("worker:",V_nurse_No_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_No_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D and dr_No_Urg_V_2[0][5] == UNDEF:
                    if dr_No_Urg_V_2[0][1] == 0:
                        dr_No_Urg_V_2[0][3] = day_current + 1
                        dr_No_Urg_V_2[0][5] = N_N_URG
                        dr_No_Urg_V_2[0][6] = day_current + 1 
                        
                        
        #    physician Non-Urgent Area
        for i in range(Dr_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
#                        dr_No_Urg_V[i][1] = 1        # Worker potential infection
                        dr_No_Urg_V_2[i][3] = day_current + 1 
                        dr_No_Urg_V_2[i][5] = PATIEN
                        dr_No_Urg_V_2[i][6] = day_current + 1 
#                        print("worker:",dr_No_Urg_V[i])
#                        print("Area:",Curr_Area)
            elif dr_No_Urg_V_2[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_2
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < P_N_URE # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if V_nurse_No_Urg_2[j][1] == 0 and V_nurse_No_Urg_2[j][5] == UNDEF:
                            V_nurse_No_Urg_2[j][3] = day_current + 1     
                            V_nurse_No_Urg_2[j][5] = D_N_URG
                            V_nurse_No_Urg_2[j][6] = day_current + 1 
            
            med_test = random.random() < Medic_test
            if med_test:
                med_test_funct_2(agent,i, da)

    return agent


def action_desit_tree_3(agent,i, da):    
    Curr_Area = agent[2]
    day_current = da     
    # interact_event = agent[6]
    # current_time = agent[4]
    
    
    if RECEP == Curr_Area:
        # if interact_event == current_time:
        for i in range(recep_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if V_recep_3[i][1] == 0 and V_recep_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_recep_3[i][3] = day_current + 1 
                        V_recep_3[i][5] = PATIEN
                        V_recep_3[i][6] = day_current + 1 
                        
#                        V_recep[i][9] = Curr_Area
#                        print("worker:",V_recep[i])
#                        print("Area:",Curr_Area)
            elif V_recep_3[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
    
    if TRIAG == Curr_Area:
        for i in range(triag_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if V_triag_3[i][1] == 0 and V_triag_3[i][6] == 0:
#                        V_triag[i][1] = 1        # Worker potential infection
                        V_triag_3[i][3] = day_current + 1 
                        V_triag_3[i][5] = PATIEN
                        V_triag_3[i][6] = day_current + 1 
#                        V_triag[i][9] = Curr_Area
#                        print("worker:",V_triag[i])
#                        print("Area:",Curr_Area)
            elif V_triag_3[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
    
    if TRIAG_U == Curr_Area:
        for i in range(triag_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if V_triag_U_3[i][1] == 0 and V_triag_U_3[i][6] == 0:
#                        V_triag_U[i][1] = 1        # Worker potential infection
                        V_triag_U_3[i][3] = day_current + 1 
                        V_triag_U_3[i][5] = PATIEN
                        V_triag_U_3[i][6] = day_current + 1 
#                        print("worker:",V_triag_U[i])
#                        print("Area:",Curr_Area)
            elif V_triag_U_3[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
#        invasi_emerg = random.random() < invasiv_prob
#        if invasi_emerg:
#            invasi_emerg_funct(agent,i)
        
    if WAI_U == Curr_Area:
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_U # Risk per area
                Dt_wa_u = random.randint(40, 120)
#                if Trnasmiss and Dt_wa_u < M_D:
#                    if V_nurse_Urg[i][1] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
#                        V_nurse_Urg[i][3] = day_current + 1 
#                        print("worker:",V_nurse_Urg[i])
#                        print("Area:",Curr_Area)
#            elif V_nurse_Urg[i][1] == 1:
#                Trnasmiss = random.random() < P_WAT_U # Risk per area
#                Dt_wa_u = random.randint(40, 120)
#                if Trnasmiss and Dt_wa_u < M_D:
#                    if agent[1] == 0:
#                        agent[1] = 2
##                        print("agent:",agent)
##                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
#                        agent[10] = day_current + 1 
        
    if WAI_N == Curr_Area:
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_WAT_N # Risk per area
#                if Trnasmiss:
#                    if V_nurse_No_Urg[i][1] == 0:
#                        V_nurse_No_Urg[i][1] = 1        # Worker potential infection
#                        print("worker:",V_nurse_No_Urg[i])
#                        print("Area:",Curr_Area)
#            elif V_nurse_No_Urg[i][1] == 1:
#                Trnasmiss = random.random() < P_WAT_N # Risk per area
#                if Trnasmiss:
#                    if agent[1] == 0:
#                        agent[1] = 1
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
    
    
    if AT_UR == Curr_Area:
        #    Nurses Urgent Area
        for i in range(nurs_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_nurse_Urg_3[i][1] == 0  and V_nurse_Urg_3[i][6] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
                        V_nurse_Urg_3[i][3] = day_current + 1 
                        V_nurse_Urg_3[i][5] = PATIEN
                        V_nurse_Urg_3[i][6] = day_current + 1 
#                        print("worker:",V_nurse_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
                Dt_urge = random.randint(20, 80)
                Trnasmiss = random.random() < PB_URGE # Risk per area
                if Trnasmiss and Dt_urge < M_D and V_dr_Urg_3[0][5] == UNDEF: 
                    if V_dr_Urg_3[0][1] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_3[0][3] = day_current + 1    
                        V_dr_Urg_3[0][5] = N_URGE
                        V_dr_Urg_3[0][6] = day_current + 1 
                        
                    
        #    physician Urgent Area
        for i in range(Dr_Ur_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_dr_Urg_3[i][1] == 0 and V_dr_Urg_3[i][6] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_3[i][3] = day_current + 1 
                        V_dr_Urg_3[i][5] = PATIEN
                        V_dr_Urg_3[i][6] = day_current + 1 
#                        print("worker:",V_dr_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_dr_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < PB_URGE # Risk per area
                    Dt_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_urge < M_D and V_nurse_Urg_3[j][5] == UNDEF:
                        if V_nurse_Urg_3[j][1] == 0:
                            V_nurse_Urg_3[j][3] = day_current + 1     
                            V_nurse_Urg_3[j][5] = DR_URGE
                            V_nurse_Urg_3[i][6] = day_current + 1 
#                V_dr_Urg[0][1]
#                if Trnasmiss and Dt_urge < M_D:
#                    if V_nurse_Urg[i][1] == 0:
##                        V_nurse_Urg[i][1] = 1        # Worker potential infection
#                        V_nurse_Urg[i][3] = day_current + 1 
                        
                        
                        
        med_test = random.random() < Medic_test
        if med_test:
            med_test_funct_3(agent,i, da)
            
#        invasi_emerg = random.random() < invasiv_prob
        
#        if invasi_emerg:
#            invasi_emerg_funct(agent,i)
        
#        neg_pres_emerg = random.random() < neg_press_prob
#        if neg_pres_emerg:
#            neg_pres_room_funct(agent,i)
            
        
    if At_NU == Curr_Area:  
        #    Nurses Non-Urgent Area
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
                        V_nurse_No_Urg_3[i][3] = day_current + 1
                        V_nurse_No_Urg_3[i][5] = PATIEN
                        V_nurse_No_Urg_3[i][6] = day_current + 1 
#                        V_nurse_No_Urg[i][1] = 1        # Worker potential infection
#                        print("worker:",V_nurse_No_Urg[i])
#                        print("Area:",Curr_Area)
            elif V_nurse_No_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D and dr_No_Urg_V_3[0][5] == UNDEF:
                    if dr_No_Urg_V_3[0][1] == 0:
                        dr_No_Urg_V_3[0][3] = day_current + 1
                        dr_No_Urg_V_3[0][5] = N_N_URG
                        dr_No_Urg_V_3[0][6] = day_current + 1 
                        
                        
        #    physician Non-Urgent Area
        for i in range(Dr_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
#                        dr_No_Urg_V[i][1] = 1        # Worker potential infection
                        dr_No_Urg_V_3[i][3] = day_current + 1 
                        dr_No_Urg_V_3[i][5] = PATIEN
                        dr_No_Urg_V_3[i][6] = day_current + 1 
#                        print("worker:",dr_No_Urg_V[i])
#                        print("Area:",Curr_Area)
            elif dr_No_Urg_V_3[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        print("agent:",agent)
#                        print("Area:",Curr_Area)
#                        agent[9] = Curr_Area
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = STAFF_3
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < P_N_URE # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if V_nurse_No_Urg_3[j][1] == 0 and V_nurse_No_Urg_3[j][5] == UNDEF:
                            V_nurse_No_Urg_3[j][3] = day_current + 1     
                            V_nurse_No_Urg_3[j][5] = D_N_URG
                            V_nurse_No_Urg_3[j][6] = day_current + 1 
            
            med_test = random.random() < Medic_test
            if med_test:
                med_test_funct_3(agent,i, da)

    return agent


def wait_room_routine(k,d_d):
    day_current = d_d
    if Users[k][2] == WAI_N:
        if Users[k][1] == 1:
            #   1. interaction with agents in Matrix
            for i in range(Seat_map.shape[0]):
                for j in range(Seat_map.shape[1]):
                    if (Seat_map[i,j]!= 0):
                        # euclidean + area + time
                        ind = np.where(Seat_map == Users[k][0])
                        row_1 = ind[0][0] + 1  # infected row
                        col_1 = ind[1][0] + 1  # infected col
                        row_2 = (i+1)          # suscept row
                        col_2 = (j+1)          # suscept col
                        Row = abs(row_1-row_2)*1
    
                        if (col_1 <= 5 and col_2 <= 5)or (col_1 
                                            >= 6 and col_2 >= 6):
                            Col = abs(col_1-col_2)*0.7
                            within = 0.7
                            
                        if (col_1 <= 5 and col_2 >= 6) or (col_1 
                                            >= 6 and col_2 <= 5):
                            within = 0.5
                            if (col_1 <= 5 and col_2 >= 6):
                                coll = abs(5 - col_1)*0.7 + abs(col_2 - 6)*0.7
                                Col = coll + 2
                            if (col_1 >= 6 and col_2 <= 5):
                                coll = abs(5 - col_2)*0.7 + abs(col_1 - 6)*0.7
                                Col = coll + 2
                        
                        
                        if ((row_1 <= 2 and row_2 <= 2) or 
                                   (row_1 >= 3 and row_2 >= 3)):
                            Row = abs(row_1-row_2)*1
                            within = 0.7
                        if ((row_1 <= 2 and row_2 >= 3) or 
                                  (row_1 >= 3 and row_2 <= 2)):
                            within = 0.5
                            if (row_1 <= 2 and row_2 >= 3):
                                Row = abs(2 - row_1)*1 + abs(row_2 - 3)
                                Row = Row + 2
                            if (row_1 >= 3 and row_2 <= 2):
                                Row = abs(2 - row_2)*1 + abs(row_1 - 3)
                                Row = Row + 2
    
    
                        eucl = math.sqrt((Row)**2 + (Col)**2)
                        
                        # between and within group prob.
                        
                        
                        if eucl < 1:
                            Trnasmiss = random.random() < P_WAT_N * within # Risk per area
    #                                            if (Trnasmiss):
                            if (Trnasmiss and Users[(Seat_map[i,j])
                                                -1][9] != INFEC):
                                Users[(Seat_map[i,j])-1][1] = 2
                                Users[(Seat_map[i,j])
                                         -1][9] = WAI_N+' -PATIENT'
                                Users[(Seat_map[i,j])-1][10] = day_current + 1 
    return


def restore_routine(k):
    
    if (Users[k][2] == IMAGI) or (Users[k][2] == LABOR):
        # back_time = Users[k][6] + t_med_test
        if Users[k][4] == Users[k][7]:
            Users[k][2] = Users[k][8]

    if (Users[k][2] == INVAS):
        if Users[k][4] == Users[k][7]:
            Users[k][2] = Users[k][8]
    return


def worker_appe_rout(staff,staff_2,staff_3):
    Users_workers = staff
    Users_workers_2 = staff_2
    Users_workers_3 = staff_3
    
    for i in range(recep_N):
        Users_workers.append(V_recep[i])
        Users_workers_2.append(V_recep_2[i])
        Users_workers_3.append(V_recep_3[i])
    
    for i in range(triag_N):
        Users_workers.append(V_triag[i])
        Users_workers_2.append(V_triag_2[i])
        Users_workers_3.append(V_triag_3[i])
        
    for i in range(triag_U_N):
        Users_workers.append(V_triag_U[i])
        Users_workers_2.append(V_triag_U_2[i])
        Users_workers_3.append(V_triag_U_3[i])
        
    for i in range(nur_NU_N):
        Users_workers.append(V_nurse_No_Urg[i])
        Users_workers_2.append(V_nurse_No_Urg_2[i])
        Users_workers_3.append(V_nurse_No_Urg_3[i])
        
    for i in range(Dr_NU_N):
        Users_workers.append(dr_No_Urg_V[i])
        Users_workers_2.append(dr_No_Urg_V_2[i])
        Users_workers_3.append(dr_No_Urg_V_3[i])

    for i in range(nurs_U_N):
        Users_workers.append(V_nurse_Urg[i])
        Users_workers_2.append(V_nurse_Urg_2[i])
        Users_workers_3.append(V_nurse_Urg_3[i])
        
    for i in range(Dr_Ur_N):
        Users_workers.append(V_dr_Urg[i])
        Users_workers_2.append(V_dr_Urg_2[i])
        Users_workers_3.append(V_dr_Urg_3[i])

    for i in range(imagi_N):
        Users_workers.append(V_imagin[i])
        Users_workers_2.append(V_imagin_2[i])
        Users_workers_3.append(V_imagin_3[i])
        
    for i in range(labor_N):
        Users_workers.append(V_labor[i])
        Users_workers_2.append(V_labor_2[i])
        Users_workers_3.append(V_labor_3[i])
    
    return Users_workers,Users_workers_2,Users_workers_3

def work_statu_rout(staff,staff_2,staff_3,day):
    Users_workers = staff
    Users_workers_2 = staff_2
    Users_workers_3 = staff_3
    day_current = day
    #-------------------------------------------------------------------------
    for i in range(len(Users_workers)):
        if (Users_workers[i][3] != 0) and (Users_workers[i][4] == 0):
            Users_workers[i][4] = Users_workers[i][3] + Infect_day
            Users_workers[i][8] = NO_INFE
            Users_workers[i][10] = NO_SYMT
            Users_workers[i][11] = Users_workers[i][3] + NO_symt_perd
    
    for i in range(len(Users_workers)):
        if (Users_workers[i][3] != 0) and (Users_workers[i][4] != 0):
            Users_workers[i][3] = day_current + 1 
    
    for i in range(len(Users_workers)):
        if ((Users_workers[i][3] == Users_workers[i][4]) and 
                                     (Users_workers[i][5] != UNDEF )):
            Users_workers[i][1] = 1
            Users_workers[i][8] = INFTOUS
            Users_workers[i][9] = Users_workers[i][3] + days_infectious
    
    for i in range(len(Users_workers)):
        if ((Users_workers[i][3] == Users_workers[i][9]) and 
                                     (Users_workers[i][8] == INFTOUS)):
            Users_workers[i][8] = IMMUNE
    
    for i in range(len(Users_workers)):
        if ((Users_workers[i][3] == Users_workers[i][11]) and 
         (Users_workers[i][10] == NO_SYMT) and (Users_workers[i][8] == INFTOUS)):
            Symto = random.random() < SYMT_PROB
            if Symto:
                Users_workers[i][10] = SYMP_Y 
            else:
                Users_workers[i][10] = SYMP_N   
                
    for i in range(len(Users_workers)):
        if ((Users_workers[i][10] == SYMP_Y) and (Users_workers[i][8] == INFTOUS)):
            Users_workers[i][8] = REPLACE
            Users_workers[i][1] = 0
            Users_workers[i][3] = 0
            Users_workers[i][4] = 0
            Users_workers[i][5] = UNDEF
            Users_workers[i][6] = 0
            Users_workers[i][9] = 0
            Users_workers[i][10] = UNDEF
            Users_workers[i][11] = 0
            # [i, 0, TRIAG_U, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0]
      
    for i in range(len(Users_workers)):
        if ((Users_workers[i][10] == SYMP_N) and (Users_workers[i][8] == IMMUNE)):
            Users_workers[i][1] = 0
            
    #-------------------------------------------------------------------------
    for i in range(len(Users_workers_2)):
        if (Users_workers_2[i][3] != 0) and (Users_workers_2[i][4] == 0):
            Users_workers_2[i][4] = Users_workers_2[i][3] + Infect_day
            Users_workers_2[i][8] = NO_INFE
            Users_workers_2[i][10] = NO_SYMT
            Users_workers_2[i][11] = Users_workers_2[i][3] + NO_symt_perd
    
    for i in range(len(Users_workers_2)):
        if (Users_workers_2[i][3] != 0) and (Users_workers_2[i][4] != 0):
            Users_workers_2[i][3] = day_current + 1 
    
    for i in range(len(Users_workers_2)):
        if ((Users_workers_2[i][3] == Users_workers_2[i][4]) and 
                                     (Users_workers_2[i][5] != UNDEF )):
            Users_workers_2[i][1] = 1
            Users_workers_2[i][8] = INFTOUS
            Users_workers_2[i][9] = Users_workers_2[i][3] + days_infectious
    
    for i in range(len(Users_workers_2)):
        if ((Users_workers_2[i][3] == Users_workers_2[i][9]) and 
                                     (Users_workers_2[i][8] == INFTOUS)):
            Users_workers_2[i][8] = IMMUNE
    
    for i in range(len(Users_workers_2)):
        if ((Users_workers_2[i][3] == Users_workers_2[i][11]) and 
         (Users_workers_2[i][10] == NO_SYMT) and (Users_workers_2[i][8] == INFTOUS)):
            Symto = random.random() < SYMT_PROB
            if Symto:
                Users_workers_2[i][10] = SYMP_Y 
            else:
                Users_workers_2[i][10] = SYMP_N   
    
    for i in range(len(Users_workers_2)):
        if ((Users_workers_2[i][10] == SYMP_Y) and (Users_workers_2[i][8] == INFTOUS)):
            Users_workers_2[i][8] = REPLACE
            Users_workers_2[i][1] = 0
            Users_workers_2[i][3] = 0
            Users_workers_2[i][4] = 0
            Users_workers_2[i][5] = UNDEF
            Users_workers_2[i][6] = 0
            Users_workers_2[i][9] = 0
            Users_workers_2[i][10] = UNDEF
            Users_workers_2[i][11] = 0
            
    for i in range(len(Users_workers_2)):
        if ((Users_workers_2[i][10] == SYMP_N) and (Users_workers_2[i][8] == IMMUNE)):
            Users_workers_2[i][1] = 0
    
    #-------------------------------------------------------------------------
    for i in range(len(Users_workers_3)):
        if (Users_workers_3[i][3] != 0) and (Users_workers_3[i][4] == 0):
            Users_workers_3[i][4] = Users_workers_3[i][3] + Infect_day
            Users_workers_3[i][8] = NO_INFE
            Users_workers_3[i][10] = NO_SYMT
            Users_workers_3[i][11] = Users_workers_3[i][3] + NO_symt_perd
    
    for i in range(len(Users_workers_3)):
        if (Users_workers_3[i][3] != 0) and (Users_workers_3[i][4] != 0):
            Users_workers_3[i][3] = day_current + 1 
    
    for i in range(len(Users_workers_3)):
        if ((Users_workers_3[i][3] == Users_workers_3[i][4]) and 
                                     (Users_workers_3[i][5] != UNDEF )):
            Users_workers_3[i][1] = 1
            Users_workers_3[i][8] = INFTOUS
            Users_workers_3[i][9] = Users_workers_3[i][3] + days_infectious
    
    for i in range(len(Users_workers_3)):
        if ((Users_workers_3[i][3] == Users_workers_3[i][9]) and 
                                     (Users_workers_3[i][8] == INFTOUS)):
            Users_workers_3[i][8] = IMMUNE
    
    for i in range(len(Users_workers_3)):
        if ((Users_workers_3[i][3] == Users_workers_3[i][11]) and 
         (Users_workers_3[i][10] == NO_SYMT) and (Users_workers_3[i][8] == INFTOUS)):
            Symto = random.random() < SYMT_PROB
            if Symto:
                Users_workers_3[i][10] = SYMP_Y 
            else:
                Users_workers_3[i][10] = SYMP_N   
    
    for i in range(len(Users_workers_3)):
        if ((Users_workers_3[i][10] == SYMP_Y) and (Users_workers_3[i][8] == INFTOUS)):
            Users_workers_3[i][8] = REPLACE
            Users_workers_3[i][1] = 0
            Users_workers_3[i][3] = 0
            Users_workers_3[i][4] = 0
            Users_workers_3[i][5] = UNDEF
            Users_workers_3[i][6] = 0
            Users_workers_3[i][9] = 0
            Users_workers_3[i][10] = UNDEF
            Users_workers_3[i][11] = 0
    
    for i in range(len(Users_workers_3)):
        if ((Users_workers_3[i][10] == SYMP_N) and (Users_workers_3[i][8] == IMMUNE)):
            Users_workers_3[i][1] = 0
    
    
    #-------------------------------------------------------------------------
    return Users_workers,Users_workers_2,Users_workers_3


"""                         Here
"""

def count_day_staff_rout(Users,day,staff_count):
    
    RECEP_from = staff_count[0]
    TRIAG_from = staff_count[1]
    TRIAG_U_from = staff_count[2]
    N_URG_from = staff_count[3]
    N_N_URG_from = staff_count[4]
    DR_URGE_from = staff_count[5]
    DR_N_URG_from = staff_count[6]
    IMAGI_from = staff_count[7]
    LABOR_from = staff_count[8]
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_1) and (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from.append([day,cont_day])    
    
#    TRIAG_FROM = []
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_1) and (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_1) and (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_1) and (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_1) and (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_1) and (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_1) and (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_1) and (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_1) and  (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from.append([day,cont_day])
    
    
    staff_count = [RECEP_from,TRIAG_from,TRIAG_U_from,N_URG_from,N_N_URG_from,
                   DR_URGE_from,DR_N_URG_from,IMAGI_from,LABOR_from]
    return staff_count


def count_day_staff_rout_2(Users,day,staff_count):
    
    RECEP_from = staff_count[0]
    TRIAG_from = staff_count[1]
    TRIAG_U_from = staff_count[2]
    N_URG_from = staff_count[3]
    N_N_URG_from = staff_count[4]
    DR_URGE_from = staff_count[5]
    DR_N_URG_from = staff_count[6]
    IMAGI_from = staff_count[7]
    LABOR_from = staff_count[8]
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_2) and (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from.append([day,cont_day])    
    
#    TRIAG_FROM = []
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_2) and (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_2) and (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_2) and (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_2) and (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_2) and (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_2) and (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_2) and (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_2) and  (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from.append([day,cont_day])
    
    
    staff_count = [RECEP_from,TRIAG_from,TRIAG_U_from,N_URG_from,N_N_URG_from,
                   DR_URGE_from,DR_N_URG_from,IMAGI_from,LABOR_from]
    return staff_count



def count_day_staff_rout_3(Users,day,staff_count):
    
    RECEP_from = staff_count[0]
    TRIAG_from = staff_count[1]
    TRIAG_U_from = staff_count[2]
    N_URG_from = staff_count[3]
    N_N_URG_from = staff_count[4]
    DR_URGE_from = staff_count[5]
    DR_N_URG_from = staff_count[6]
    IMAGI_from = staff_count[7]
    LABOR_from = staff_count[8]
    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_3) and (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from.append([day,cont_day])    
    
#    TRIAG_FROM = []
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_3) and (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                 (Users[i][11] == STAFF_3) and (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_3) and (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_3) and (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_3) and (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                   (Users[i][11] == STAFF_3) and (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                     (Users[i][11] == STAFF_3) and (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                    (Users[i][11] == STAFF_3) and  (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from.append([day,cont_day])
    
    
    staff_count = [RECEP_from,TRIAG_from,TRIAG_U_from,N_URG_from,N_N_URG_from,
                   DR_URGE_from,DR_N_URG_from,IMAGI_from,LABOR_from]
    return staff_count


def percent_staff_rout(conteo,staff_count,staff_count_2):
    
    
    cont_from_w = conteo
    RECEP_from = staff_count[0]
    TRIAG_from = staff_count[1]
    TRIAG_U_from = staff_count[2]
    N_URG_from = staff_count[3]
    N_N_URG_from = staff_count[4]
    DR_URGE_from = staff_count[5]
    DR_N_URG_from = staff_count[6]
    IMAGI_from = staff_count[7]
    LABOR_from = staff_count[8]
    
    port_RECEP_from = staff_count_2[0]
    port_TRIAG_from = staff_count_2[1]
    port_TRIAG_U_from = staff_count_2[2]
    port_N_URG_from = staff_count_2[3]
    port_N_N_URG_from = staff_count_2[4]
    port_DR_URGE_from = staff_count_2[5]
    port_DR_N_URG_from = staff_count_2[6]
    port_IMAGI_from = staff_count_2[7]
    port_LABOR_from = staff_count_2[8]
    
    
    count = 0
    for i in range(len(RECEP_from)):
        if RECEP_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (RECEP_from[i][1]*100) / cont_from_w[i][1]
            port_RECEP_from.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from.append([i,count])
            
    count = 0
    for i in range(len(TRIAG_from)):
        if TRIAG_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (TRIAG_from[i][1]*100) / cont_from_w[i][1]
            port_TRIAG_from.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from.append([i,count])
            
    count = 0
    for i in range(len(TRIAG_U_from)):
        if TRIAG_U_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (TRIAG_U_from[i][1]*100) / cont_from_w[i][1]
            port_TRIAG_U_from.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_U_from.append([i,count])
            
    count = 0
    for i in range(len(N_URG_from)):
        if N_URG_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (N_URG_from[i][1]*100) / cont_from_w[i][1]
            port_N_URG_from.append([i,count])
            count = 0
        else:
            count = 0
            port_N_URG_from.append([i,count])
    
    count = 0
    for i in range(len(N_N_URG_from)):
        if N_N_URG_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (N_N_URG_from[i][1]*100) / cont_from_w[i][1]
            port_N_N_URG_from.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from.append([i,count])
            
    
    count = 0
    for i in range(len(DR_URGE_from)):
        if DR_URGE_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (DR_URGE_from[i][1]*100) / cont_from_w[i][1]
            port_DR_URGE_from.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_URGE_from.append([i,count])
    

    count = 0
    for i in range(len(DR_N_URG_from)):
        if DR_N_URG_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (DR_N_URG_from[i][1]*100) / cont_from_w[i][1]
            port_DR_N_URG_from.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from.append([i,count])
            

    count = 0
    for i in range(len(IMAGI_from)):
        if IMAGI_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (IMAGI_from[i][1]*100) / cont_from_w[i][1]
            port_IMAGI_from.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from.append([i,count])
            
    
    count = 0
    for i in range(len(LABOR_from)):
        if LABOR_from[i][1] != 0 and cont_from_w[i][1] != 0:
            count = (LABOR_from[i][1]*100) / cont_from_w[i][1]
            port_LABOR_from.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from.append([i,count])
    
    
    staff_count_2 = [port_RECEP_from,port_TRIAG_from,port_TRIAG_U_from,
                      port_N_URG_from,port_N_N_URG_from,port_DR_URGE_from,
                      port_DR_N_URG_from,port_IMAGI_from,port_LABOR_from]
    
    return staff_count_2




def ED_year(anno):
    
    """---------------------------------------------------------------------------             
                        Users of emergency department 
                                 VARIABLES
                                  
    """
    global person_Tot, Users, V_recep, V_triag, V_triag_U, V_nurse_No_Urg, dr_No_Urg_V
    global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
    global invasiv_prob, neg_press_prob
    global PB_RECE, P_TRI_R, P_TRI_U, P_WAT_N, P_WAT_U, P_N_URE, PB_URGE, PB_LABO, PB_IMAG
    global ISOLA_R, SHOCK_R, INVASIV, NEGATIV
    global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
    global User_track_1, Seat_map, day_current, day
    
    global Isolation_room, Emergen_doct, Shock_room, roll_up_wall, Invasiv_room
    global negt_pres_room, emerg_doctor
    global ISOLA, RECEP, TRIAG, TRIAG_U, WAI_N, WAI_U, N_URG, U_URG, IMAGI, LABOR
    global EXIT_, AT_UR, At_NU, INVAS
    global Num_Aget
    global origin_path, Newfolder
    
    global recep_N, triag_N, triag_U_N, triag_U_N, nur_NU_N, nurs_U_N, Dr_NU_N
    global Dr_Ur_N, imagi_N, labor_N
    global M_D
    
    global INFEC, PATIEN, N_URGE, N_N_URG, DR_URGE, D_N_URG
    global STAFF_1, STAFF_2, STAFF_3, UNDEF, Medic_test
    
    global V_recep_2, V_triag_2, V_triag_U_2, V_nurse_No_Urg_2, dr_No_Urg_V_2
    global V_nurse_Urg_2, V_dr_Urg_2, V_imagin_2, V_labor_2
    
    global V_recep_3, V_triag_3, V_triag_U_3, V_nurse_No_Urg_3, dr_No_Urg_V_3
    global V_nurse_Urg_3, V_dr_Urg_3, V_imagin_3, V_labor_3
    
    global SYMP_Y, SYMP_N, NO_SYMT, INFTOUS, NO_INFE, IMMUNE, REPLACE
    
    global SYMT_PROB, Infect_day, Sympto_day, days_infectious, NO_symt_perd
    global Symto_perod
    

    # Here goes the complete code for 1 year ...
    med_test = 1
    actual_user = 0
    Time_var = 0
    N_days = 365
    Num_Aget = 250
    
    
    N_new_day_from_w = []
    N_new_day_work = []
    N_new_day = []
    N_waiting_H = []
    Result_user = []
    Result_worker = []
    
    N_day_fr_sta_1 = []
    N_day_fr_sta_2 = []
    N_day_fr_sta_3 = []
    
    RECEP_from = []
    TRIAG_from = []
    TRIAG_U_from = []
    N_URG_from = []
    N_N_URG_from = []
    IMAGI_from = []
    LABOR_from = []
    DR_URGE_from = []
    DR_N_URG_from = []
    
    RECEP_from_2 = []
    TRIAG_from_2 = []
    TRIAG_U_from_2 = []
    N_URG_from_2 = []
    N_N_URG_from_2 = []
    DR_URGE_from_2 = []
    DR_N_URG_from_2 = []
    IMAGI_from_2 = []
    LABOR_from_2 = []
    
    RECEP_from_3 = []
    TRIAG_from_3 = []
    TRIAG_U_from_3 = []
    N_URG_from_3 = []
    N_N_URG_from_3 = []
    DR_URGE_from_3 = []
    DR_N_URG_from_3 = []
    IMAGI_from_3 = []
    LABOR_from_3 = []
    
    
    port_RECEP_from = []
    port_TRIAG_from = []
    port_TRIAG_U_from = []
    port_N_URG_from = []
    port_N_N_URG_from = []
    port_IMAGI_from = []
    port_LABOR_from = []
    port_DR_URGE_from = []
    port_DR_N_URG_from = []
    
    port_RECEP_from_2 = []
    port_TRIAG_from_2 = []
    port_TRIAG_U_from_2 = []
    port_N_URG_from_2 = []
    port_N_N_URG_from_2 = []
    port_IMAGI_from_2 = []
    port_LABOR_from_2 = []
    port_DR_URGE_from_2 = []
    port_DR_N_URG_from_2 = []
    
    port_RECEP_from_3 = []
    port_TRIAG_from_3 = []
    port_TRIAG_U_from_3 = []
    port_N_URG_from_3 = []
    port_N_N_URG_from_3 = []
    port_IMAGI_from_3 = []
    port_LABOR_from_3 = []
    port_DR_URGE_from_3 = []
    port_DR_N_URG_from_3 = []
    
    
    #   FROM FUNCTIONS   ------------------------------------------------------
    
    prop_cycle = plt.rcParams['axes.prop_cycle'] #Colors
    colors = prop_cycle.by_key()['color']
    
    
    M_D = 100  #  100 cm
    
    RECEP = 'RECEPTION'
    # REGIS = 'REGISTRATION'
    TRIAG = 'TRIAGE'
    TRIAG_U = 'TRIAGE_URGENT'
    WAI_N = 'WAIT_NO_URGENT'
    WAI_U = 'WAIT_URGENT'
    N_URG = 'NOT_URGENT'
    U_URG = 'URGENT'
    IMAGI = 'IMAGING'
    LABOR = 'LABORATORY'
    EXIT_ = 'EXIT'
    AT_UR = 'ATTEN_URGE'
    At_NU = 'ATTE_N_URG'
    
    UNDEF = 'UNDEFINED'
    
    ISOLA = 'ISOLATION_ROOM'
    SHOCK = 'SHOCK_ROOM'
    INVAS = 'INVASIVE_INTERVENTION_ROOM'
    NEGAT = 'NEGATIVE_PRESSURE_ROOM'
    
    INFEC = 'INFECTED'
    PATIEN = 'PATIENT'
    N_URGE = 'N_URGENT'
    N_N_URG = 'N_N_URGE'
    DR_URGE = 'DR_URGEN'
    D_N_URG = 'DR_N_URGE'
    
    STAFF_1 = "STAFF_1"
    STAFF_2 = "STAFF_2"
    STAFF_3 = "STAFF_3"
    
    SYMP_Y = "SYMPTOMATIC"
    SYMP_N = "ASYMPTOMATIC"
    NO_SYMT = "NO_SYMPTOM"
    
    INFTOUS = "INFECTIOUS"
    NO_INFE = "NO_INFTOUS"
    IMMUNE = "IMMUNE"
    REPLACE = "REPLACED"
    
    SYMT_PROB = 0.5
    Infect_day = 3   # days
    Sympto_day = 5   # days
    days_infectious = 5  # days
    NO_symt_perd = 5  # days
    Symto_perod = 8  # days
    
    
    

    """--------------------------------------------------------------------------
                                 PATIENTS 
    """
    
    #day_current = 0
    #                  Time scaling, MINUTES
    Time_scale = 60*24*1*1*1 #  ->  minutes, hours, days, month, year
    # Active_Period = [60*5, 60*21] # ->  5 h, 21h 
    
    Active_Period = [60*2, 60*23] # ->  5 h, 21h 
    
    shift_1 = [60*6, 60*(6+8)] # ->  6 h, 14 h 
    shift_2 = [(60*(6+8))+1, 60*(6+8+8)]
    shift_3 = [(60*(6+8+8))+1, (60*6)-1]
    
    
    # shift_1 = [60*2, 60*(2+8)] # ->  6 h, 14 h 
    # shift_2 = [(60*(2+8))+1, 60*(2+8+8)]
    # shift_3 = [(60*(2+8+8))+1, (60*6)-1]
    
    
    time_arriv = []
    for i in range(Num_Aget):
        time_arriv.append(random.randint(Active_Period[0], Active_Period[1]))
    time_arriv.sort()
    
         # SET THE NUMBER OF USERS
    Users = []
    for i in range(Num_Aget):
    # User -> Agent_Number, Infection Status, Area, Area-Time, Area-time_count, arriv, 
    # interact_moment, side_time, side_label, area of getting infected?, day, staff_shift
        Users.append([i+1, 0, UNDEF, 0, 0, time_arriv[i],0, 0, UNDEF, UNDEF, 0, UNDEF])
    
    #Users[2][1] = 1
    #Users[8][1] = 1
    #Users[25][1] = 1
    #Users[32][1] = 1
        
    Users[2][1] = 1
    Users[80][1] = 1
    Users[150][1] = 1
    Users[200][1] = 1
    
    Users[2][9] = INFEC
    Users[80][9] = INFEC
    Users[150][9] = INFEC
    Users[200][9] = INFEC
        
        
    #Users[2][1] = 1
    #Users[10][1] = 1
    #Users[25][1] = 1
    #Users[40][1] = 1
    #
    #Users[2][9] = INFEC
    #Users[10][9] = INFEC
    #Users[25][9] = INFEC
    #Users[40][9] = INFEC    
    
    
    User_track_1 = []
    # for i in range(Num_Aget):
    # User -> Agent_Number, Infection Status, Area, Time in Area
    # User_track_1.append([1, 0, UNDEF, 0])
    
    """                            WORKERS 
                                   totals
    """
    #                 SET THE NUMBER OF WORKERS PER AREA
    recep_N = 1
    triag_N = 1
    triag_U_N = 1
    nur_NU_N = 2
    nurs_U_N = 2
    Dr_NU_N = 1
    Dr_Ur_N = 1
    imagi_N = 1
    labor_N = 1
    
    person_Tot = (recep_N + triag_N + nur_NU_N + nurs_U_N + Dr_NU_N + Dr_Ur_N +
                  imagi_N + labor_N + triag_U_N)
    
    N_interaction = 3
    
    
    """                  Worker RECEPTION
    """
    V_recep = []
    V_recep_2 = []
    V_recep_3 = []
    for i in range(recep_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
    #    from-whom, , work_shift, Symptomatic, day_infectious
        V_recep.append([i, 0, RECEP, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_recep_2.append([i, 0, RECEP, 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_recep_3.append([i, 0, RECEP, 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
        
    """                  Worker TRIAGE/REGIS
    """
    V_triag = []
    V_triag_2 = []
    V_triag_3 = []
    for i in range(triag_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_triag.append([i, 0, TRIAG, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_triag_2.append([i, 0, TRIAG, 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])  
        V_triag_3.append([i, 0, TRIAG, 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0]) 
    
        
    V_triag_U = []
    V_triag_U_2 = []
    V_triag_U_3 = []
    for i in range(triag_U_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_triag_U.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_triag_U_2.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_triag_U_3.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    
    """                  Worker NO URGENT
    """
    V_nurse_No_Urg = []
    V_nurse_No_Urg_2 = []
    V_nurse_No_Urg_3 = []
    for i in range(nur_NU_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_nurse_No_Urg.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_nurse_No_Urg_2.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_nurse_No_Urg_3.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    dr_No_Urg_V = []
    dr_No_Urg_V_2 = []
    dr_No_Urg_V_3 = []
    for i in range(Dr_NU_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        dr_No_Urg_V.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        dr_No_Urg_V_2.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        dr_No_Urg_V_3.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
        
    """                  Worker URGENT
    """
    V_nurse_Urg = []
    V_nurse_Urg_2 = []
    V_nurse_Urg_3 = []
    for i in range(nurs_U_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_nurse_Urg.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_nurse_Urg_2.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_nurse_Urg_3.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    V_dr_Urg = []
    V_dr_Urg_2 = []
    V_dr_Urg_3 = []
    for i in range(Dr_Ur_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_dr_Urg.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_dr_Urg_2.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_dr_Urg_3.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    """                  Worker IMAGING
    """
    V_imagin = []
    V_imagin_2 = []
    V_imagin_3 = []
    for i in range(imagi_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_imagin.append([i, 0, IMAGI, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_imagin_2.append([i, 0, IMAGI, 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_imagin_3.append([i, 0, IMAGI, 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    """                  Worker LABORATORY
    """
    V_labor = []
    V_labor_2 = []
    V_labor_3 = []
    for i in range(labor_N):
        #  WORKER -> worker_Number/Area, Infection Status, Area, worker_N_TOTAL
        V_labor.append([i, 0, LABOR, 0, 0, UNDEF, 0, 1, UNDEF, 0, UNDEF, 0])
        V_labor_2.append([i, 0, LABOR, 0, 0, UNDEF, 0, 2, UNDEF, 0, UNDEF, 0])
        V_labor_3.append([i, 0, LABOR, 0, 0, UNDEF, 0, 3, UNDEF, 0, UNDEF, 0])
        
    """---------------------------------------------------------------------------
    """    
    
    
    """---------------------------------------------------------------------------
                  
                      PATHOGEN TRANSMISSION PROBABILITY (RISK)
    """
    #           Probability based on risk and pathogen transmission
    low = 0.20          # 20% probability
    medium = 0.45       # 45% probability
    high = 0.75         # 75% probability
    very_high = 0.9     # 90% probability
    
    # Risk per ED area
    PB_RECE = low
    P_TRI_R = medium
    P_TRI_U = high
    P_WAT_N = high   # Outpatients
    P_WAT_U = high   # Urgent patients
    P_N_URE = medium
    PB_URGE = medium
    PB_LABO = low
    PB_IMAG = low
    
    # Risk on potential interventions
    ISOLA_R = very_high
    SHOCK_R = very_high
    INVASIV = very_high
    NEGATIV = medium
    
    
    
    """---------------------------------------------------------------------------
    """ 
    
    #               Probabiliies for desitions
    Own_Arrive = 0.8  
    Suspicion_of_infection = 0.2
    Isolation_needed = 0.2
    Medic_test = 0.25
    invasiv_prob = 0.15
    neg_press_prob = 0.15
    
    
    """------------------Seat Map Waiting Area  -----------------------------------
    """
    
    Seat_map = np.zeros((4,10))
    Seat_map = Seat_map.astype(int)
    """---------------------------------------------------------------------------
    """ 
    
    Isolation_room = 0            
    Emergen_doct = 1
    Shock_room = 0
    roll_up_wall = 0
    Invasiv_room = 0
    negt_pres_room = 0
    emerg_doctor = 0
    #   FROM FUNCTIONS END  ---------------------------------------------------
    
    
    for day in range(N_days):
        day_current = day
        while Time_var <= Time_scale:
                
    #------------------------------------------------------------------------------
            """                  Staff shift 1
            """
            if (Time_var >= shift_1[0]) and (Time_var <= shift_1[1]):
                entrance_routine(Time_var)
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF:
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:
                            # "DESITION TREE AREA"
                            area_desit_tree(Users[k],k)
                            #-------------------------------------------
                            # Set position matrix if Waiting area
                            #   1. position in Matrix, where availeable seat 
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1)
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1
            
                        elif Users[k][4] == Users[k][6]:
                            # Action desition tree
                            action_desit_tree(Users[k],k,day)    
                            wait_room_routine(k,day_current)
                        
                    restore_routine(k)
             #------------------------------------------------------------------------------
                     
               #------------------------------------------------------------------------------
            """                  Staff shift 2
            """
            if (Time_var >= shift_2[0]) and (Time_var <= shift_2[1]):
                entrance_routine(Time_var)
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF:
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:
                            # "DESITION TREE AREA"
                            area_desit_tree(Users[k],k)
                            #-------------------------------------------
                            # Set position matrix if Waiting area
                            #   1. position in Matrix, where availeable seat 
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1)
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1
            
                        elif Users[k][4] == Users[k][6]:
                            # Action desition tree
                            action_desit_tree_2(Users[k],k,day)    
                            wait_room_routine(k,day_current)
                        
                    restore_routine(k)
    #------------------------------------------------------------------------------
                    
    #------------------------------------------------------------------------------
            """                  Staff shift 3
            """  
            if (Time_var >= shift_3[0]):
                entrance_routine(Time_var)
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF:
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:
                            # "DESITION TREE AREA"
                            area_desit_tree(Users[k],k)
                            #-------------------------------------------
                            # Set position matrix if Waiting area
                            #   1. position in Matrix, where availeable seat 
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1)
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1
            
                        elif Users[k][4] == Users[k][6]:
                            # Action desition tree
                            action_desit_tree_3(Users[k],k,day)    
                            wait_room_routine(k,day_current)
                        
                    restore_routine(k)
                    
            if day_current >= 1:
                if (Time_var <= shift_3[1]):
                    entrance_routine(Time_var)
                    for k in range(Num_Aget):
                        if Users[k][2] != UNDEF:
                            Curr_time = Users[k][4]
                            Users[k][4] = Curr_time + 1
                            if Users[k][4] == Users[k][3]:
                                # "DESITION TREE AREA"
                                area_desit_tree(Users[k],k)
                                #-------------------------------------------
                                # Set position matrix if Waiting area
                                #   1. position in Matrix, where availeable seat 
                                if Users[k][2] == WAI_N:
                                    Seated = 0 
                                    while Seated == 0:
                                        indx_1 =  np.random.randint(0, high=4, size=1)
                                        indx_2 =  np.random.randint(0, high=10, size=1)
                                        if Seat_map[indx_1[0],indx_2[0]] == 0:
                                            Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                            Seated = 1
                
                            elif Users[k][4] == Users[k][6]:
                                # Action desition tree
                                action_desit_tree_3(Users[k],k,day)    
                                wait_room_routine(k,day_current)
                            
                        restore_routine(k)
    #------------------------------------------------------------------------------
                
            # time variable for minutes manager
            Time_var = Time_var + 1 
        
        # Day aligment
        print(day+1)
        
        
    #------------------------------------------------------------------------------
    #---------------------  Medical Staff  ----------------------------------------
        Users_workers = []
        Users_workers_2 = []
        Users_workers_3 = []
        
        staff_rot = worker_appe_rout(Users_workers,Users_workers_2,Users_workers_3)
        Users_workers = staff_rot[0]
        Users_workers_2 = staff_rot[1]
        Users_workers_3 = staff_rot[2]
        
        
        staff_ro_2 = work_statu_rout(Users_workers,Users_workers_2,
                                      Users_workers_3,day_current)
        Users_workers = staff_ro_2[0]
        Users_workers_2 = staff_ro_2[1]
        Users_workers_3 = staff_ro_2[2]
          
        # curr_worker = Users_workers
        # # Result_worker.extend(curr_worker)
        # cont_use_day_w = 0
        # for i in range(len(Users_workers)):
        #     if (Users_workers[i][6] == (day + 1)):
        #         cont_use_day_w = cont_use_day_w + 1
        # N_new_day_work.append([day,cont_use_day_w])
    #------------------------------------------------------------------------------   
     #--------------------------  From Waiting Area  ------------------------------   
        curr_user = Users
        Result_user.extend(curr_user)
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                                             (Users[i][9] == WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day + 1
        N_new_day.append([day,cont_use_day])
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                                             (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day + 1
        N_new_day_from_w.append([day,cont_use_day])
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
               (Users[i][11] == STAFF_1) and (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day + 1
        N_day_fr_sta_1.append([day,cont_use_day])
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
               (Users[i][11] == STAFF_2) and (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day + 1
        N_day_fr_sta_2.append([day,cont_use_day])
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
               (Users[i][11] == STAFF_3) and (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day + 1
        N_day_fr_sta_3.append([day,cont_use_day])
        
        
    #------------------------------------------------------------------------------    
    #------------------------  From staff  ----------------------------------------    
        
        staff_count = [RECEP_from,TRIAG_from,TRIAG_U_from,N_URG_from,N_N_URG_from,
                        DR_URGE_from,DR_N_URG_from,IMAGI_from,LABOR_from]
        staff_count = count_day_staff_rout(Users,day,staff_count)
        RECEP_from = staff_count[0]
        TRIAG_from = staff_count[1]
        TRIAG_U_from = staff_count[2]
        N_URG_from = staff_count[3]
        N_N_URG_from = staff_count[4]
        DR_URGE_from = staff_count[5]
        DR_N_URG_from = staff_count[6]
        IMAGI_from = staff_count[7]
        LABOR_from = staff_count[8]
        
        
        staff_cnt_2 = [RECEP_from_2,TRIAG_from_2,TRIAG_U_from_2,N_URG_from_2,
                        N_N_URG_from_2,
                        DR_URGE_from_2,DR_N_URG_from_2,IMAGI_from_2,LABOR_from_2]
        staff_cnt_2 = count_day_staff_rout_2(Users,day,staff_cnt_2)
        RECEP_from_2 = staff_cnt_2[0]
        TRIAG_from_2 = staff_cnt_2[1]
        TRIAG_U_from_2 = staff_cnt_2[2]
        N_URG_from_2 = staff_cnt_2[3]
        N_N_URG_from_2 = staff_cnt_2[4]
        DR_URGE_from_2 = staff_cnt_2[5]
        DR_N_URG_from_2 = staff_cnt_2[6]
        IMAGI_from_2 = staff_cnt_2[7]
        LABOR_from_2 = staff_cnt_2[8]
        
    
        staff_cnt_3 = [RECEP_from_3,TRIAG_from_3,TRIAG_U_from_3,N_URG_from_3,
                        N_N_URG_from_3,
                        DR_URGE_from_3,DR_N_URG_from_3,IMAGI_from_3,LABOR_from_3]
        staff_cnt_3 = count_day_staff_rout_3(Users,day,staff_cnt_3)
        RECEP_from_3 = staff_cnt_3[0]
        TRIAG_from_3 = staff_cnt_3[1]
        TRIAG_U_from_3 = staff_cnt_3[2]
        N_URG_from_3 = staff_cnt_3[3]
        N_N_URG_from_3 = staff_cnt_3[4]
        DR_URGE_from_3 = staff_cnt_3[5]
        DR_N_URG_from_3 = staff_cnt_3[6]
        IMAGI_from_3 = staff_cnt_3[7]
        LABOR_from_3 = staff_cnt_3[8]
    
    #------------------------------------------------------------------------------       
    #    var_zero()
    
        time_arriv = []
        for i in range(Num_Aget):
            time_arriv.append(random.randint(Active_Period[0], Active_Period[1]))
        time_arriv.sort()
    
        for i in range(Num_Aget):
            Users[i] = [i+1, 0, UNDEF, 0, 0, time_arriv[i],0, 0, UNDEF, UNDEF, 0, UNDEF]
    
        Users[2][1] = 1
        Users[80][1] = 1
        Users[150][1] = 1
        Users[200][1] = 1
        
        Users[2][9] = INFEC
        Users[80][9] = INFEC
        Users[150][9] = INFEC
        Users[200][9] = INFEC
    
        """------------------Seat Map Waiting Area  -------------------------------
        """
        for i in range(Seat_map.shape[0]):
            for j in range(Seat_map.shape[1]):
                Seat_map[i,j] = 0
    
        Time_var = 0


    
    cont_from_w = []
    cont_day = 0
    for i in range(len(LABOR_from)):
        cont_day = (RECEP_from[i][1] + TRIAG_from[i][1] 
                    + TRIAG_U_from[i][1]
                    + N_URG_from[i][1]
                    + N_N_URG_from[i][1]
                    + DR_URGE_from[i][1]
                    + DR_N_URG_from[i][1]
                    + IMAGI_from[i][1]
                    + LABOR_from[i][1])
        cont_from_w.append([i,cont_day])
        cont_day = 0
        
    cont_from_w_2 = []
    cont_day = 0
    for i in range(len(LABOR_from_2)):
        cont_day = (RECEP_from_2[i][1] + TRIAG_from_2[i][1] 
                    + TRIAG_U_from_2[i][1]
                    + N_URG_from_2[i][1]
                    + N_N_URG_from_2[i][1]
                    + DR_URGE_from_2[i][1]
                    + DR_N_URG_from_2[i][1]
                    + IMAGI_from_2[i][1]
                    + LABOR_from_2[i][1])
        cont_from_w_2.append([i,cont_day])
        cont_day = 0
    
    cont_from_w_3 = []
    cont_day = 0
    for i in range(len(LABOR_from_3)):
        cont_day = (RECEP_from_3[i][1] + TRIAG_from_3[i][1] 
                    + TRIAG_U_from_3[i][1]
                    + N_URG_from_3[i][1]
                    + N_N_URG_from_3[i][1]
                    + DR_URGE_from_3[i][1]
                    + DR_N_URG_from_3[i][1]
                    + IMAGI_from_3[i][1]
                    + LABOR_from_3[i][1])
        cont_from_w_3.append([i,cont_day])
        cont_day = 0
    
    
    
    cont_tot_w = []
    cont_day = 0
    for i in range(len(N_new_day)):
        cont_day = N_new_day[i][1] + N_new_day_from_w[i][1]
        cont_tot_w.append([i,cont_day])
        cont_day = 0
    
    #------------------------------------------------------------------------------    
    #----------------------  From staff  Percentage -------------------------------    
        
        staff_count_2 = [port_RECEP_from,port_TRIAG_from,port_TRIAG_U_from,
                        port_N_URG_from,port_N_N_URG_from,port_DR_URGE_from,
                        port_DR_N_URG_from,port_IMAGI_from,port_LABOR_from]
        staff_count_2 = percent_staff_rout(cont_from_w,staff_count,staff_count_2)
        port_RECEP_from = staff_count_2[0]
        port_TRIAG_from = staff_count_2[1]
        port_TRIAG_U_from = staff_count_2[2]
        port_N_URG_from = staff_count_2[3]
        port_N_N_URG_from = staff_count_2[4]
        port_DR_URGE_from = staff_count_2[5]
        port_DR_N_URG_from = staff_count_2[6]
        port_IMAGI_from = staff_count_2[7]
        port_LABOR_from = staff_count_2[8]
        
        
        staff_porcet_2 = [port_RECEP_from_2,port_TRIAG_from_2,port_TRIAG_U_from_2,
                        port_N_URG_from_2,port_N_N_URG_from_2,port_DR_URGE_from_2,
                        port_DR_N_URG_from_2,port_IMAGI_from_2,port_LABOR_from_2]
        staff_porcet_2 = percent_staff_rout(cont_from_w_2,staff_cnt_2,
                                                                staff_porcet_2)
        port_RECEP_from_2 = staff_porcet_2[0]
        port_TRIAG_from_2 = staff_porcet_2[1]
        port_TRIAG_U_from_2 = staff_porcet_2[2]
        port_N_URG_from_2 = staff_porcet_2[3]
        port_N_N_URG_from_2 = staff_porcet_2[4]
        port_DR_URGE_from_2 = staff_porcet_2[5]
        port_DR_N_URG_from_2 = staff_porcet_2[6]
        port_IMAGI_from_2 = staff_porcet_2[7]
        port_LABOR_from_2 = staff_porcet_2[8]
        
        
        staff_porcet_3 = [port_RECEP_from_3,port_TRIAG_from_3,port_TRIAG_U_from_3,
                        port_N_URG_from_3,port_N_N_URG_from_3,port_DR_URGE_from_3,
                        port_DR_N_URG_from_3,port_IMAGI_from_3,port_LABOR_from_3]
        staff_porcet_3 = percent_staff_rout(cont_from_w_3,staff_cnt_3,
                                                                staff_porcet_3)
        port_RECEP_from_3 = staff_porcet_3[0]
        port_TRIAG_from_3 = staff_porcet_3[1]
        port_TRIAG_U_from_3 = staff_porcet_3[2]
        port_N_URG_from_3 = staff_porcet_3[3]
        port_N_N_URG_from_3 = staff_porcet_3[4]
        port_DR_URGE_from_3 = staff_porcet_3[5]
        port_DR_N_URG_from_3 = staff_porcet_3[6]
        port_IMAGI_from_3 = staff_porcet_3[7]
        port_LABOR_from_3 = staff_porcet_3[8]
        
    #------------------------------------------------------------------------------   
    
    #-----------------------------------------------------------------------------
            #             plots
    pat_tot = []
    days_plot = []
    staff_plot = []
    
    porcent_recep = []
    porcent_triag = []
    porcent_tria_u = []
    porcent_N_urge = []
    porcent_N_N_ur = []
    porcent_dr_urg = []
    porcent_dr_n_u = []
    porcent_labora = []
    porcent_imagin = []
    for i in range(len(N_new_day)):
        pat_tot.append(N_new_day[i][1])
        staff_plot.append(N_new_day_from_w[i][1])
        days_plot.append(N_new_day[i][0]+1)
        porcent_recep.append(port_RECEP_from[i][1])
        porcent_triag.append(port_TRIAG_from[i][1])
        porcent_tria_u.append(port_TRIAG_U_from[i][1])
        porcent_N_urge.append(port_N_URG_from[i][1])
        porcent_N_N_ur.append(port_N_N_URG_from[i][1])
        porcent_dr_urg.append(port_DR_URGE_from[i][1])
        porcent_dr_n_u.append(port_DR_N_URG_from[i][1])
        porcent_labora.append(port_LABOR_from[i][1])
        porcent_imagin.append(port_IMAGI_from[i][1])
    
    
    origin_path = os.getcwd()
    N_dir = origin_path + '/'+ Newfolder
    os.chdir(N_dir)
    fil = open('Result_year_{}.txt'.format(anno),'w')
    fil.write('Results of year --- {}'.format(anno))
    fil.close()
    
    width = 0.5   
    ax=plt.figure(figsize=(9,5), facecolor='w', edgecolor='k')
    p1 = plt.bar(days_plot, staff_plot, width)
    p2 = plt.bar(days_plot, pat_tot, width,
                  bottom=staff_plot)
    #plt.ylabel('Newly infected')
    plt.title('Newly infected patients per day (numbers)', fontsize=14)
    plt.xticks(days_plot, fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(0, 255) 
    plt.legend((p1[0], p2[0]), ('By staff', 'By patients'), fontsize=12)
    #ax.savefig('new_infec_year_{}.pdf'.format(anno), format='pdf', dpi=1400)
    plt.show()
    
    
    
    # print(f'\nFinished in {((t2-t1)/60): .2f} minutes')
    # print(f' "   "   in {((t2-t1)): .2f} seconds')
    
    
    
    # time.sleep(yr)
    # origin_path = os.getcwd()
    # N_dir = origin_path + '\\'+ Newfolder
    # os.chdir(N_dir)
    # fil = open('Result_year_{}.txt'.format(anno),'w')
    # fil.write('Results of year --- {}'.format(anno))
    # fil.close()
    
    print(anno)
    yy = anno
    
    return f'Year:{yy}'

def ED_main(yr):
    global person_Tot, Users, V_recep, V_triag, V_nurse_No_Urg, dr_No_Urg_V
    global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
    global invasiv_prob, neg_press_prob
    global PB_RECE, P_TRI_R, P_WAT_N, P_WAT_U, P_N_URE, PB_URGE, PB_LABO, PB_IMAG
    global ISOLA_R, SHOCK_R, INVASIV, NEGATIV
    global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
    global User_track_1, Seat_map, day_current, day
    
    global Isolation_room, Emergen_doct, Shock_room, roll_up_wall, Invasiv_room
    global negt_pres_room, emerg_doctor
    global ISOLA, RECEP, TRIAG, TRIAG_U, WAI_N, WAI_U, N_URG, U_URG, IMAGI, LABOR
    global EXIT_, AT_UR, At_NU
    global Num_Aget
    global origin_path, Newfolder
    
    inter_init = time.perf_counter()
    res_yr = ED_year(yr)
    t2_in = time.perf_counter()
    time_ex = round(t2_in - inter_init, 2)
    return res_yr, time_ex


if __name__ == '__main__':
    # year = [1 ,2 ,3, 4]
    # year = [1,2,3,4,5]
    
    # global origin_path, Newfolder

    # detect the current working directory and print it
    origin_path = os.getcwd()
    os.chdir(origin_path)
    # Newfolder = 'Res_4'
    os.makedirs(Newfolder)
    year = list(range(1, 250 +1))

    with Pool(250) as p:

        result = p.map(ED_main, year)
        print("\np")
        print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
print(f'Finished in {round((finish-start)/60, 2)} min(s), 250 sim, N_3')

