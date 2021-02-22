# -*- coding: utf-8 -*-
"""
Created 20.01.2021

@author: Gustavo Hernandez-Mejia
"""

from funct_shifts_sympt_wall import *
import matplotlib.pyplot as plt
# import math   
# from pylab import *
# from mpl_toolkits.mplot3d import axes3d
import numpy as np
import pandas as pd
import random
# from matplotlib.font_manager import FontProperties
# import csv
# import shelve
import time
# from io import StringIO
# import matplotlib.patches as patches

t1 = time.perf_counter()


global person_Tot, Users, V_recep, V_triag, V_nurse_No_Urg, dr_No_Urg_V
global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
global invasiv_prob, neg_press_prob
global User_track_1, Seat_map, day_current, day


#               Presence of potential intervention
# Isolation_room = 0            
# Emergen_doct = 1
# Shock_room = 0
# roll_up_wall = 0
# Invasiv_room = 0
# negt_pres_room = 0
# emerg_doctor = 0



med_test = 1

actual_user = 0
Time_var = 0
N_days = 18


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
#ax.savefig('new_infec_by_p_2.pdf', format='pdf', dpi=1400)
plt.show()


ax=plt.figure(figsize=(9,5), facecolor='w', edgecolor='k')
p1 = plt.bar(days_plot, pat_tot, width)
#plt.ylabel('Newly infected')
plt.title('Infected users by patients per day (numbers)', fontsize=14)
plt.xticks(days_plot, fontsize=12)
plt.yticks(fontsize=12)
#plt.legend((p1[0]), ('By patients'), fontsize=12)
#ax.savefig('new_infec_patients_2.pdf', format='pdf', dpi=1400)
plt.show()


width = 0.65
ax=plt.figure(figsize=(9,6), facecolor='w', edgecolor='k')
plt.bar(days_plot, porcent_N_N_ur, width, label='Non-urgt. nurse')
plt.bar(days_plot, porcent_triag,width, bottom =porcent_N_N_ur, label='Triage')
plt.bar(days_plot, porcent_tria_u, width, label='Triage-urgt', 
                bottom = [sum(x) for x in zip(porcent_N_N_ur, porcent_triag)])
plt.bar(days_plot, porcent_recep, width, label='Reception', 
bottom = [sum(x) for x in zip(porcent_N_N_ur, porcent_tria_u,porcent_triag)])
plt.bar(days_plot, porcent_dr_n_u, width, label='Non-urgt. Dr', 
bottom = [sum(x) for x in 
            zip(porcent_N_N_ur, porcent_tria_u,porcent_triag,porcent_recep)])
plt.bar(days_plot, porcent_N_urge, width, label='Urgt. Nurse', 
bottom = [sum(x) for x in 
zip(porcent_N_N_ur,porcent_tria_u,porcent_triag,porcent_recep,porcent_dr_n_u)])
plt.bar(days_plot, porcent_dr_urg, width, label='Urgt. Dr', 
bottom = [sum(x) for x in 
zip(porcent_N_N_ur, porcent_tria_u,porcent_triag,porcent_recep, 
    porcent_N_urge, porcent_dr_n_u)])
plt.bar(days_plot, porcent_labora, width, label='Laboratory', 
bottom = [sum(x) for x in 
zip(porcent_N_N_ur, porcent_tria_u,porcent_triag,porcent_recep, 
    porcent_N_urge, porcent_dr_n_u,porcent_dr_urg)])
plt.bar(days_plot, porcent_imagin, width, label='Imaging', 
bottom = [sum(x) for x in 
zip(porcent_N_N_ur, porcent_tria_u,porcent_triag,porcent_recep, 
    porcent_N_urge, porcent_dr_n_u,porcent_dr_urg,porcent_labora)])

#plt.bar(days_plot, porcent_dr_urg, width, bottom = porcent_imagin)
#p4 = plt.bar(days_plot, porcent_dr_n_u, width)
#p5 = plt.bar(days_plot, porcent_recep, width)
#p6 = plt.bar(days_plot, porcent_triag, width)
#p7 = plt.bar(days_plot, porcent_tria_u, width)
#plt.ylabel('Newly infected')
plt.title('Proportion of infected patients by medical staff/area (%)',fontsize=14)
plt.xticks(days_plot, fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, 105) 
#plt.legend((p1[0], p2[0]), ('Non-urgt. nurse', 'By patients'), fontsize=12)
plt.legend(loc='upper left',fontsize=12)
#ax.savefig('new_infec_by_staff_2.pdf', format='pdf', dpi=1400)
plt.show()

t2 = time.perf_counter()

print(f'\nFinished in {((t2-t1)/60): .2f} minutes')
print(f' "   "   in {((t2-t1)): .2f} seconds')


