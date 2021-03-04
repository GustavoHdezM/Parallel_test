# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4  2021

@author: Gustavo Hernandez-Mejia
"""

import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from multiprocessing import Pool
# from funct_parall_main_ED_1 import *

start = time.perf_counter()
global sleep_sec

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


def ED_year(anno):
    
    """---------------------------------------------------------------------------             
                        Users of emergency department 
                                 VARIABLES
                                  
    """
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
    
    # Here goes the complete code for 1 year ...
    med_test = 1
    actual_user = 0
    Time_var = 0
    N_days = 15
    
    
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
    Num_Aget = 250
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
            
                    #     elif Users[k][4] == Users[k][6]:
                    #         # Action desition tree
                    #         action_desit_tree(Users[k],k,day)    
                    #         wait_room_routine(k,day_current)
                        
                    # restore_routine(k)
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
            
                    #     elif Users[k][4] == Users[k][6]:
                    #         # Action desition tree
                    #         action_desit_tree_2(Users[k],k,day)    
                    #         wait_room_routine(k,day_current)
                        
                    # restore_routine(k)
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
            
                    #     elif Users[k][4] == Users[k][6]:
                    #         # Action desition tree
                    #         action_desit_tree_3(Users[k],k,day)    
                    #         wait_room_routine(k,day_current)
                        
                    # restore_routine(k)
                    
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
                
                        #     elif Users[k][4] == Users[k][6]:
                        #         # Action desition tree
                        #         action_desit_tree_3(Users[k],k,day)    
                        #         wait_room_routine(k,day_current)
                            
                        # restore_routine(k)
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
        
        # staff_rot = worker_appe_rout(Users_workers,Users_workers_2,Users_workers_3)
        # Users_workers = staff_rot[0]
        # Users_workers_2 = staff_rot[1]
        # Users_workers_3 = staff_rot[2]
        
        
        # staff_ro_2 = work_statu_rout(Users_workers,Users_workers_2,
        #                              Users_workers_3,day_current)
        # Users_workers = staff_ro_2[0]
        # Users_workers_2 = staff_ro_2[1]
        # Users_workers_3 = staff_ro_2[2]
          
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
        
        # staff_count = [RECEP_from,TRIAG_from,TRIAG_U_from,N_URG_from,N_N_URG_from,
        #                DR_URGE_from,DR_N_URG_from,IMAGI_from,LABOR_from]
        # staff_count = count_day_staff_rout(Users,day,staff_count)
        # RECEP_from = staff_count[0]
        # TRIAG_from = staff_count[1]
        # TRIAG_U_from = staff_count[2]
        # N_URG_from = staff_count[3]
        # N_N_URG_from = staff_count[4]
        # DR_URGE_from = staff_count[5]
        # DR_N_URG_from = staff_count[6]
        # IMAGI_from = staff_count[7]
        # LABOR_from = staff_count[8]
        
        
        # staff_cnt_2 = [RECEP_from_2,TRIAG_from_2,TRIAG_U_from_2,N_URG_from_2,
        #                 N_N_URG_from_2,
        #                 DR_URGE_from_2,DR_N_URG_from_2,IMAGI_from_2,LABOR_from_2]
        # staff_cnt_2 = count_day_staff_rout_2(Users,day,staff_cnt_2)
        # RECEP_from_2 = staff_cnt_2[0]
        # TRIAG_from_2 = staff_cnt_2[1]
        # TRIAG_U_from_2 = staff_cnt_2[2]
        # N_URG_from_2 = staff_cnt_2[3]
        # N_N_URG_from_2 = staff_cnt_2[4]
        # DR_URGE_from_2 = staff_cnt_2[5]
        # DR_N_URG_from_2 = staff_cnt_2[6]
        # IMAGI_from_2 = staff_cnt_2[7]
        # LABOR_from_2 = staff_cnt_2[8]
        
    
        # staff_cnt_3 = [RECEP_from_3,TRIAG_from_3,TRIAG_U_from_3,N_URG_from_3,
        #                 N_N_URG_from_3,
        #                 DR_URGE_from_3,DR_N_URG_from_3,IMAGI_from_3,LABOR_from_3]
        # staff_cnt_3 = count_day_staff_rout_3(Users,day,staff_cnt_3)
        # RECEP_from_3 = staff_cnt_3[0]
        # TRIAG_from_3 = staff_cnt_3[1]
        # TRIAG_U_from_3 = staff_cnt_3[2]
        # N_URG_from_3 = staff_cnt_3[3]
        # N_N_URG_from_3 = staff_cnt_3[4]
        # DR_URGE_from_3 = staff_cnt_3[5]
        # DR_N_URG_from_3 = staff_cnt_3[6]
        # IMAGI_from_3 = staff_cnt_3[7]
        # LABOR_from_3 = staff_cnt_3[8]
    
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
        
        # staff_count_2 = [port_RECEP_from,port_TRIAG_from,port_TRIAG_U_from,
        #                 port_N_URG_from,port_N_N_URG_from,port_DR_URGE_from,
        #                 port_DR_N_URG_from,port_IMAGI_from,port_LABOR_from]
        # staff_count_2 = percent_staff_rout(cont_from_w,staff_count,staff_count_2)
        # port_RECEP_from = staff_count_2[0]
        # port_TRIAG_from = staff_count_2[1]
        # port_TRIAG_U_from = staff_count_2[2]
        # port_N_URG_from = staff_count_2[3]
        # port_N_N_URG_from = staff_count_2[4]
        # port_DR_URGE_from = staff_count_2[5]
        # port_DR_N_URG_from = staff_count_2[6]
        # port_IMAGI_from = staff_count_2[7]
        # port_LABOR_from = staff_count_2[8]
        
        
        # staff_porcet_2 = [port_RECEP_from_2,port_TRIAG_from_2,port_TRIAG_U_from_2,
        #                 port_N_URG_from_2,port_N_N_URG_from_2,port_DR_URGE_from_2,
        #                 port_DR_N_URG_from_2,port_IMAGI_from_2,port_LABOR_from_2]
        # staff_porcet_2 = percent_staff_rout(cont_from_w_2,staff_cnt_2,
        #                                                        staff_porcet_2)
        # port_RECEP_from_2 = staff_porcet_2[0]
        # port_TRIAG_from_2 = staff_porcet_2[1]
        # port_TRIAG_U_from_2 = staff_porcet_2[2]
        # port_N_URG_from_2 = staff_porcet_2[3]
        # port_N_N_URG_from_2 = staff_porcet_2[4]
        # port_DR_URGE_from_2 = staff_porcet_2[5]
        # port_DR_N_URG_from_2 = staff_porcet_2[6]
        # port_IMAGI_from_2 = staff_porcet_2[7]
        # port_LABOR_from_2 = staff_porcet_2[8]
        
        
        # staff_porcet_3 = [port_RECEP_from_3,port_TRIAG_from_3,port_TRIAG_U_from_3,
        #                 port_N_URG_from_3,port_N_N_URG_from_3,port_DR_URGE_from_3,
        #                 port_DR_N_URG_from_3,port_IMAGI_from_3,port_LABOR_from_3]
        # staff_porcet_3 = percent_staff_rout(cont_from_w_3,staff_cnt_3,
        #                                                        staff_porcet_3)
        # port_RECEP_from_3 = staff_porcet_3[0]
        # port_TRIAG_from_3 = staff_porcet_3[1]
        # port_TRIAG_U_from_3 = staff_porcet_3[2]
        # port_N_URG_from_3 = staff_porcet_3[3]
        # port_N_N_URG_from_3 = staff_porcet_3[4]
        # port_DR_URGE_from_3 = staff_porcet_3[5]
        # port_DR_N_URG_from_3 = staff_porcet_3[6]
        # port_IMAGI_from_3 = staff_porcet_3[7]
        # port_LABOR_from_3 = staff_porcet_3[8]
        
    #------------------------------------------------------------------------------   
    
    #-----------------------------------------------------------------------------
            #             plots
    # pat_tot = []
    # days_plot = []
    # staff_plot = []
    
    # porcent_recep = []
    # porcent_triag = []
    # porcent_tria_u = []
    # porcent_N_urge = []
    # porcent_N_N_ur = []
    # porcent_dr_urg = []
    # porcent_dr_n_u = []
    # porcent_labora = []
    # porcent_imagin = []
    # for i in range(len(N_new_day)):
    #     pat_tot.append(N_new_day[i][1])
    #     staff_plot.append(N_new_day_from_w[i][1])
    #     days_plot.append(N_new_day[i][0]+1)
    #     porcent_recep.append(port_RECEP_from[i][1])
    #     porcent_triag.append(port_TRIAG_from[i][1])
    #     porcent_tria_u.append(port_TRIAG_U_from[i][1])
    #     porcent_N_urge.append(port_N_URG_from[i][1])
    #     porcent_N_N_ur.append(port_N_N_URG_from[i][1])
    #     porcent_dr_urg.append(port_DR_URGE_from[i][1])
    #     porcent_dr_n_u.append(port_DR_N_URG_from[i][1])
    #     porcent_labora.append(port_LABOR_from[i][1])
    #     porcent_imagin.append(port_IMAGI_from[i][1])
    
    
    # width = 0.5   
    # ax=plt.figure(figsize=(9,5), facecolor='w', edgecolor='k')
    # p1 = plt.bar(days_plot, staff_plot, width)
    # p2 = plt.bar(days_plot, pat_tot, width,
    #               bottom=staff_plot)
    # #plt.ylabel('Newly infected')
    # plt.title('Newly infected patients per day (numbers)', fontsize=14)
    # plt.xticks(days_plot, fontsize=12)
    # plt.yticks(fontsize=12)
    # plt.ylim(0, 255) 
    # plt.legend((p1[0], p2[0]), ('By staff', 'By patients'), fontsize=12)
    # #ax.savefig('new_infec_by_p_2.pdf', format='pdf', dpi=1400)
    # plt.show()
    
    
    
    # print(f'\nFinished in {((t2-t1)/60): .2f} minutes')
    # print(f' "   "   in {((t2-t1)): .2f} seconds')
    
    
    
    # time.sleep(yr)
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
    inter_init = time.perf_counter()
    res_yr = ED_year(yr)
    t2_in = time.perf_counter()
    time_ex = round(t2_in - inter_init, 2)
    return res_yr, time_ex


if __name__ == '__main__':
    # year = [1 ,2 ,3, 4]
    year = [1,2,3,4,5]

    with Pool(5) as p:

        result = p.map(ED_main, year)
        print("\np")
        print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')

