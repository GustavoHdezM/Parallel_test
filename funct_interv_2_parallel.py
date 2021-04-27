# -*- coding: utf-8 -*-
"""
Model Agents for Emergency department

Shared with Victoria Tomori 03.02.2021

Functions

@author: Gustavo
"""




import random
import matplotlib.pyplot as plt
import math  
import time
import numpy as np
import pandas as pd
import csv

prop_cycle = plt.rcParams['axes.prop_cycle'] #Colors
colors = prop_cycle.by_key()['color']


M_D = 100  #  100 cm


RECEP = 'RECEPTION'
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
ARE_test= 'Area_test'

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

SYMP_YES = 'SYMPTOM_YES'
SYMP_NO = 'SYMPTOM_NO'
REPLACE= 'ALREADY REPLACED'
DAY_SPECIFIC = "Day_spec_infec"


"""---------------------------------------------------------------------------             
                    Users of emergency department 
                             VARIABLES
                              
"""


global person_Tot, Users, V_recep, V_triag, V_nurse_No_Urg, dr_No_Urg_V
global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
global invasiv_prob, neg_press_prob
global PB_RECE, P_TRI_R, P_WAT_N, P_WAT_U, P_N_URE, PB_URGE, PB_LABO, PB_IMAG,PB_ARE_test,PB_SYMPTOMS
global ISOLA_R, SHOCK_R, INVASIV, NEGATIV
global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
global User_track_1, Seat_map, day_current, day
global N_new_day_from_shift_1,N_new_day_from_shift_2, N_new_day_from_shift_3
"""--------------------------------------------------------------------------
 


                            PATIENTS 
"""
Num_Aget = 250 
day_current = 0
#                  Time scaling, MINUTES
Time_scale = 60*24*1*1*1 #  ->  minutes, hours, days, month, year
Active_Period = [60*1, 60*24] # ->  5 h, 21h 



Time_var = 0
med_test = 1
N_days = 15
actual_user = 0

shift_1 =  [1, 480]  #on minutes bases, min 1 to 480 minutes (60*8) 
shift_2 =  [481, 960]
shift_3 =  [961, 1440]

time_arriv = []
for i in range(Num_Aget):
    time_arriv.append(random.randint(Active_Period[0], Active_Period[1]))
time_arriv.sort()

     # SET THE NUMBER OF USERS
Users = []
for i in range(Num_Aget):
# User -> Agent_Number, Infection Status, Area, Area-Time, Area-time_count, arriv, 
# interact_moment, side_time, side_label, area of getting infected?, day, symptom, indicate staff on shift
    Users.append([i+1, 0, UNDEF, 0, 0, time_arriv[i],0, 0, UNDEF, UNDEF, 0, UNDEF])

    
Users[2][1] = 1
Users[80][1] = 1
Users[150][1] = 1
Users[200][1] = 1

Users[2][9] = INFEC
Users[80][9] = INFEC
Users[150][9] = INFEC
Users[200][9] = INFEC
    
     


User_track_1 = []



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
ARE_test_N = 1
person_Tot = (recep_N + triag_N + nur_NU_N + nurs_U_N + Dr_NU_N + Dr_Ur_N +
              imagi_N + labor_N + triag_U_N+ARE_test_N)

#N_interaction = 3


"""                  Worker RECEPTION
"""
V_recep_1 = []
V_recep_2 = []
V_recep_3 = []
for i in range(recep_N):
    V_recep_1.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_recep_2.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_recep_3.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
"""                  Worker TRIAGE/REGIS
"""
V_triag_1 = []
V_triag_2 = []
V_triag_3 = []
for i in range(triag_N):
    V_triag_1.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_triag_2.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_triag_3.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
V_triag_U_1 = []
V_triag_U_2 = []
V_triag_U_3 = []
for i in range(triag_U_N):
    V_triag_U_1.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_triag_U_2.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_triag_U_3.append([i, 0, TRIAG_U, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    

"""                  Worker NO URGENT
"""
V_nurse_No_Urg_1 = []
V_nurse_No_Urg_2 = []
V_nurse_No_Urg_3 = []
for i in range(nur_NU_N):
    V_nurse_No_Urg_1.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_nurse_No_Urg_2.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_nurse_No_Urg_3.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
dr_No_Urg_V_1 = []
dr_No_Urg_V_2 = []
dr_No_Urg_V_3 = []
for i in range(Dr_NU_N):
    dr_No_Urg_V_1.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    dr_No_Urg_V_2.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    dr_No_Urg_V_3.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
"""                  Worker URGENT
"""
V_nurse_Urg_1 = []
V_nurse_Urg_2 = []
V_nurse_Urg_3 = []
for i in range(nurs_U_N):
    V_nurse_Urg_1.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_nurse_Urg_2.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_nurse_Urg_3.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
V_dr_Urg_1 = []
V_dr_Urg_2 = []
V_dr_Urg_3 = []
for i in range(Dr_Ur_N):
    V_dr_Urg_1.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_dr_Urg_2.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_dr_Urg_3.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
"""                  Worker IMAGING
"""
V_imagin_1 = []
V_imagin_2 = []
V_imagin_3 = []
for i in range(imagi_N):
    V_imagin_1.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_imagin_2.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_imagin_3.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
"""                  Worker LABORATORY
"""
V_labor_1 = []
V_labor_2 = []
V_labor_3 = []
for i in range(labor_N):
    V_labor_1.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_labor_2.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_labor_3.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
"""                    ARE_test (created by Victoria)
"""
V_ARE_test_1 = []
V_ARE_test_2 = []
V_ARE_test_3 = []
for i in range(ARE_test_N):
    V_ARE_test_1.append([i, 0, ARE_test, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_ARE_test_2.append([i, 0, ARE_test, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    V_ARE_test_3.append([i, 0, ARE_test, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    

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
PB_ARE_test = medium
PB_SYMPTOMS = high

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


Isolation_room = 0            
Emergen_doct = 1
Shock_room = 0
roll_up_wall = 0
Invasiv_room = 0
negt_pres_room = 0
emerg_doctor = 0

"""------------------Seat Map Waiting Area  -----------------------------------
"""

Seat_map = np.zeros((4,10))
Seat_map = Seat_map.astype(int)
"""---------------------------------------------------------------------------
""" 



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




def arrival_method(time):
    Time_var = time
    for j in range(Num_Aget):
        if Time_var == Users[j][5]:
            Own = random.random() < Own_Arrive
            if Own:
                if Isolation_room:
                    funct_isolat(Users[j],j)
                    
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
        
    if  TRIAG == Curr_Area:
        Next_Area = ARE_test
        Users[i][2] = Next_Area
        t_ARE_test = random.randint(15, 30)
        Users[i][3] = t_ARE_test
        Users[i][4] = 0
        Users[i][6] = random.randint(1, t_ARE_test)        
    
    if  ARE_test == Curr_Area:
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

              
def action_desit_tree_shift_1(agent,i, da):    
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
                    if V_recep_1[i][1] == 0 and V_recep_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_recep_1[i][3] = day_current + 1 
                        V_recep_1[i][5] = PATIEN
                        V_recep_1[i][6] = day_current + 1 
                        
            elif V_recep_1[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"
    
    if TRIAG == Curr_Area:
        for i in range(triag_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if V_triag_1[i][1] == 0 and V_triag_1[i][6] == 0:
#                        V_triag[i][1] = 1        # Worker potential infection
                        V_triag_1[i][3] = day_current + 1 
                        V_triag_1[i][5] = PATIEN
                        V_triag_1[i][6] = day_current + 1 

            elif V_triag_1[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"

    if ARE_test == Curr_Area:
        for i in range(ARE_test_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if V_ARE_test_1[i][1] == 0 and V_ARE_test_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_ARE_test_1[i][3] = day_current + 1 
                        V_ARE_test_1[i][5] = PATIEN
                        V_ARE_test_1[i][6] = day_current + 1 
                        
            elif V_ARE_test_1[i][1] == 1:
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"
    
    if TRIAG_U == Curr_Area:
        for i in range(triag_U_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if V_triag_U_1[i][1] == 0 and V_triag_U_1[i][6] == 0:
#                        V_triag_U[i][1] = 1        # Worker potential infection
                        V_triag_U_1[i][3] = day_current + 1 
                        V_triag_U_1[i][5] = PATIEN
                        V_triag_U_1[i][6] = day_current + 1 

            elif V_triag_U_1[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"

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
                    if V_nurse_Urg_1[i][1] == 0  and V_nurse_Urg_1[i][6] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
                        V_nurse_Urg_1[i][3] = day_current + 1 
                        V_nurse_Urg_1[i][5] = PATIEN
                        V_nurse_Urg_1[i][6] = day_current + 1 
            elif V_nurse_Urg_1[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"
                Dt_urge = random.randint(20, 80)
                Trnasmiss = random.random() < PB_URGE # Risk per area
                if Trnasmiss and Dt_urge < M_D and V_dr_Urg_1[0][5] == UNDEF: 
                    if V_dr_Urg_1[0][1] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_1[0][3] = day_current + 1    
                        V_dr_Urg_1[0][5] = N_URGE
                        V_dr_Urg_1[0][6] = day_current + 1 
                        
                    
        #    physician Urgent Area
        for i in range(Dr_Ur_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if V_dr_Urg_1[i][1] == 0 and V_dr_Urg_1[i][6] == 0:
#                        V_dr_Urg[i][1] = 1        # Worker potential infection
                        V_dr_Urg_1[i][3] = day_current + 1 
                        V_dr_Urg_1[i][5] = PATIEN
                        V_dr_Urg_1[i][6] = day_current + 1 
            elif V_dr_Urg_1[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1
                        agent[11] = "Staff1"
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < PB_URGE # Risk per area
                    Dt_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_urge < M_D and V_nurse_Urg_1[j][5] == UNDEF:
                        if V_nurse_Urg_1[j][1] == 0:
                            V_nurse_Urg_1[j][3] = day_current + 1     
                            V_nurse_Urg_1[j][5] = DR_URGE
                            V_nurse_Urg_1[i][6] = day_current + 1 

                        
        med_test = random.random() < Medic_test
        if med_test:
            med_test_funct_shift_1(agent,i, da)

        
    if At_NU == Curr_Area:  
        #    Nurses Non-Urgent Area
        for i in range(nur_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
                        V_nurse_No_Urg_1[i][3] = day_current + 1
                        V_nurse_No_Urg_1[i][5] = PATIEN
                        V_nurse_No_Urg_1[i][6] = day_current + 1 
                        
            elif V_nurse_No_Urg_1[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"

                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D and dr_No_Urg_V_1[0][5] == UNDEF:
                    if dr_No_Urg_V_1[0][1] == 0:
                        dr_No_Urg_V_1[0][3] = day_current + 1
                        dr_No_Urg_V_1[0][5] = N_N_URG
                        dr_No_Urg_V_1[0][6] = day_current + 1 
                        
                        
        #    physician Non-Urgent Area
        for i in range(Dr_NU_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
#                        dr_No_Urg_V[i][1] = 1        # Worker potential infection
                        dr_No_Urg_V_1[i][3] = day_current + 1 
                        dr_No_Urg_V_1[i][5] = PATIEN
                        dr_No_Urg_V_1[i][6] = day_current + 1 

            elif dr_No_Urg_V_1[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < P_N_URE # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if V_nurse_No_Urg_1[j][1] == 0 and V_nurse_No_Urg_1[j][5] == UNDEF:
                            V_nurse_No_Urg_1[j][3] = day_current + 1     
                            V_nurse_No_Urg_1[j][5] = D_N_URG
                            V_nurse_No_Urg_1[j][6] = day_current + 1 
            
            med_test = random.random() < Medic_test
            if med_test:
                med_test_funct_shift_1(agent,i, da)

    return agent


     



def action_desit_tree_shift_2(agent,i, da):    
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
                    if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_recep_2[i][3] = day_current + 1 
                        V_recep_2[i][5] = PATIEN
                        V_recep_2[i][6] = day_current + 1 
                        
            elif V_recep_2[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"
    
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

            elif V_triag_2[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"

    if ARE_test == Curr_Area:
        for i in range(ARE_test_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if V_ARE_test_2[i][1] == 0 and V_ARE_test_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_ARE_test_2[i][3] = day_current + 1 
                        V_ARE_test_2[i][5] = PATIEN
                        V_ARE_test_2[i][6] = day_current + 1 
                        
            elif V_ARE_test_2[i][1] == 1:
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"
    
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

            elif V_triag_U_2[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"

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
            elif V_nurse_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"
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
            elif V_dr_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1
                        agent[11] = "Staff2"
                
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
            med_test_funct_shift_2(agent,i, da)

        
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
                        
            elif V_nurse_No_Urg_2[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"

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

            elif dr_No_Urg_V_2[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"
                
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
                med_test_funct_shift_2(agent,i, da)

    return agent



def action_desit_tree_shift_3(agent,i, da):    
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
                        
            elif V_recep_3[i][1] == 1:
                Trnasmiss = random.random() < PB_RECE # Risk per area
                Dt_regi = random.randint(70, 120)
                if Trnasmiss and Dt_regi < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"
    
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

            elif V_triag_3[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_R # Risk per area
                Dt_tria = random.randint(70, 120)
                if Trnasmiss and Dt_tria < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"

    if ARE_test == Curr_Area:
        for i in range(ARE_test_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if V_ARE_test_3[i][1] == 0 and V_ARE_test_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                        V_ARE_test_3[i][3] = day_current + 1 
                        V_ARE_test_3[i][5] = PATIEN
                        V_ARE_test_3[i][6] = day_current + 1 
                        
            elif V_ARE_test_3[i][1] == 1:
                Trnasmiss = random.random() < PB_ARE_test # Risk per area
                Dt_area_test = random.randint(70, 120)
                if Trnasmiss and Dt_area_test < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"
    
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

            elif V_triag_U_3[i][1] == 1:
                Trnasmiss = random.random() < P_TRI_U # Risk per area
                Dt_tria_U = random.randint(50, 120)
                if Trnasmiss and Dt_tria_U < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"

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
                    if V_nurse_Urg_3[i][1] == 0  and V_nurse_Urg_3[i][6] == 0:
#                        V_nurse_Urg[i][1] = 1        # Worker potential infection
                        V_nurse_Urg_3[i][3] = day_current + 1 
                        V_nurse_Urg_3[i][5] = PATIEN
                        V_nurse_Urg_3[i][6] = day_current + 1 
            elif V_nurse_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = N_URGE
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"
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
            elif V_dr_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < PB_URGE # Risk per area
                Dt_urge = random.randint(20, 80)
                if Trnasmiss and Dt_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = DR_URGE
                        agent[10] = day_current + 1
                        agent[11] = "Staff3"
                
                for j in range(nur_NU_N):
                    Trnasmiss = random.random() < PB_URGE # Risk per area
                    Dt_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_urge < M_D and V_nurse_Urg_3[j][5] == UNDEF:
                        if V_nurse_Urg_3[j][1] == 0:
                            V_nurse_Urg_3[j][3] = day_current + 1     
                            V_nurse_Urg_3[j][5] = DR_URGE
                            V_nurse_Urg_3[i][6] = day_current + 1 

                        
        med_test = random.random() < Medic_test
        if med_test:
            med_test_funct_shift_3(agent,i, da)

        
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
                        
            elif V_nurse_No_Urg_3[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
#                        agent[9] = Curr_Area
                        agent[9] = N_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"

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

            elif dr_No_Urg_V_3[i][1] == 1:
                Trnasmiss = random.random() < P_N_URE # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2
                        agent[9] = D_N_URG
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"
                
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
                med_test_funct_shift_3(agent,i, da)

    return agent


     

def med_test_funct_shift_1(agent,i, day):
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
                    if Trnasmiss and Dt_n_urge < M_D and V_imagin_1[i][6] == 0:
                        if V_imagin_1[i][1] == 0:
#                            V_imagin[i][1] = 1        # Worker potential infection
                            V_imagin_1[i][3] = day_current + 1
                            V_imagin_1[i][5] = PATIEN
                            V_imagin_1[i][6] = day_current + 1 

                elif V_imagin_1[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = "Staff1"
    else:    
        agent[2] = LABOR 
        User_track_1.append([i+1, agent[1], agent[2], t_med_test ])
        for i in range(labor_N):
            if (agent[1] == 1):                       # Agent infected
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if V_labor_1[i][1] == 0 and V_labor_1[i][6] == 0:
#                        V_labor[i][1] = 1        # Worker potential infection
                        V_labor_1[i][3] = day_current + 1 
                        V_labor_1[i][5] = PATIEN
                        V_labor_1[i][6] = day_current + 1 

            elif V_labor_1[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2

                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1"       
    return



def med_test_funct_shift_2(agent,i, day):
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

                elif V_imagin_2[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = "Staff2"
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

            elif V_labor_2[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2

                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2"       
    return


def med_test_funct_shift_3(agent,i, day):
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

                elif V_imagin_3[i][1] == 1:
                    Trnasmiss = random.random() < PB_IMAG # Risk per area
                    Dt_n_urge = random.randint(20, 80)
                    if Trnasmiss and Dt_n_urge < M_D:
                        if agent[1] == 0:
                            agent[1] = 2
                            agent[9] = agent[2]
                            agent[10] = day_current + 1 
                            agent[11] = "Staff3"
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

            elif V_labor_3[i][1] == 1:
                Trnasmiss = random.random() < PB_LABO # Risk per area
                Dt_n_urge = random.randint(20, 80)
                if Trnasmiss and Dt_n_urge < M_D:
                    if agent[1] == 0:
                        agent[1] = 2

                        agent[9] = agent[2]
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3"       
    return


def sitting_arrangement(k, days):
    day_current = days
    if Users[k][2] == WAI_N:
        if Users[k][1] == 1:
            for i in range(Seat_map.shape[0]):
                for j in range(Seat_map.shape[1]):
                    if (Seat_map[i,j]!= 0):
                        ind = np.where(Seat_map == Users[k][0])
                        row_1 = ind[0][0] + 1  # infected row, plus 1 is adayed to index python from 1
                        col_1 = ind[1][0] + 1  # infected col
                        row_2 = (i+1)          # suscept row
                        col_2 = (j+1)          # suscept col
                        Row = abs(row_1-row_2)*1
                        if (col_1 <= 5 and col_2 <= 5)or (col_1 >= 6 and col_2 >= 6):
                            Col = abs(col_1-col_2)*0.7 #diffrence between column is 0.7
                            within = 1 #mirror of transmission prob
                                            
                        if (col_1 <= 5 and col_2 >= 6) or (col_1>= 6 and col_2 <= 5):
                            within = 0.7
                                            
                            if (col_1 <= 5 and col_2 >= 6):
                                coll = abs(5 - col_1)*0.7 + abs(col_2 - 6)*0.7
                                Col = coll + 2 # 2 meteres seperating the two groups
                            if (col_1 >= 6 and col_2 <= 5):
                                coll = abs(5 - col_2)*0.7 + abs(col_1 - 6)*0.7
                                Col = coll + 2
                                        
                                        
                        if ((row_1 <= 2 and row_2 <= 2) or  (row_1 >= 3 and row_2 >= 3)):
                            Row = abs(row_1-row_2)*1
                            within = 1 #sucesptible and infected are in thseame group
                            
                        if ((row_1 <= 2 and row_2 >= 3) or (row_1 >= 3 and row_2 <= 2)):
                            within = 0.7 #sucesptible and infected are in different group
                            
                            if (row_1 <= 2 and row_2 >= 3):
                                Row = abs(2 - row_1)*1 + abs(row_2 - 3)
                                Row = Row + 2
                                
                            if (row_1 >= 3 and row_2 <= 2):
                                Row = abs(2 - row_2)*1 + abs(row_1 - 3)
                                Row = Row + 2


                        eucl = math.sqrt((Row)**2 + (Col)**2)
                        if eucl < 2:
                            Trnasmiss = random.random() < P_WAT_N * within # Risk per area
                            if (Trnasmiss and Users[(Seat_map[i,j]) -1][9] != INFEC):
                                Users[(Seat_map[i,j])-1][1] = 2
                                Users[(Seat_map[i,j])-1][9] = WAI_N+' -PATIENT'
                                Users[(Seat_map[i,j])-1][10] = day_current + 1 
                  
    
                if (Users[k][2] == IMAGI) or (Users[k][2] == LABOR):
                    if Users[k][4] == Users[k][7]:
                        Users[k][2] = Users[k][8]

                if (Users[k][2] == INVAS):
                    if Users[k][4] == Users[k][7]:
                        Users[k][2] = Users[k][8]
    return                        
           


def workers_settings(worker1, worker2, worker3):
        
        Users_workers_shift_1 = worker1
        Users_workers_shift_2 = worker2
        Users_workers_shift_3 = worker3
        
        
        for i in range(recep_N):
            Users_workers_shift_1.append(V_recep_1[i])
            Users_workers_shift_2.append(V_recep_2[i])
            Users_workers_shift_3.append(V_recep_3[i])
    
        for i in range(triag_N):
            Users_workers_shift_1.append(V_triag_1[i])
            Users_workers_shift_2.append(V_triag_2[i])
            Users_workers_shift_3.append(V_triag_3[i])
        
        for i in range(triag_U_N):
            Users_workers_shift_1.append(V_triag_U_1[i])
            Users_workers_shift_2.append(V_triag_U_2[i])
            Users_workers_shift_3.append(V_triag_U_3[i])
        
        for i in range(nur_NU_N):
            Users_workers_shift_1.append(V_nurse_No_Urg_1[i])
            Users_workers_shift_2.append(V_nurse_No_Urg_2[i])
            Users_workers_shift_3.append(V_nurse_No_Urg_3[i])
        
        for i in range(Dr_NU_N):
            Users_workers_shift_1.append(dr_No_Urg_V_1[i])
            Users_workers_shift_2.append(dr_No_Urg_V_2[i])
            Users_workers_shift_3.append(dr_No_Urg_V_3[i])
        
        for i in range(ARE_test_N):
            Users_workers_shift_1.append(V_ARE_test_1[i])
            Users_workers_shift_2.append(V_ARE_test_2[i])
            Users_workers_shift_3.append(V_ARE_test_3[i])
            
        for i in range(nurs_U_N):
            Users_workers_shift_1.append(V_nurse_Urg_1[i])
            Users_workers_shift_2.append(V_nurse_Urg_2[i])
            Users_workers_shift_3.append(V_nurse_Urg_3[i])

        for i in range(Dr_Ur_N):
            Users_workers_shift_1.append(V_dr_Urg_1[i])
            Users_workers_shift_2.append(V_dr_Urg_2[i])
            Users_workers_shift_3.append(V_dr_Urg_3[i])

        for i in range(imagi_N):
            Users_workers_shift_1.append(V_imagin_1[i])
            Users_workers_shift_2.append(V_imagin_2[i])
            Users_workers_shift_3.append(V_imagin_3[i])
        
        for i in range(labor_N):
            Users_workers_shift_1.append(V_labor_1[i])
            Users_workers_shift_2.append(V_labor_2[i])
            Users_workers_shift_3.append(V_labor_3[i])
    
    
        return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3
    
def workers_settings_status(worker1, worker2, worker3, days):
    day_current = days
    Users_workers_shift_1 = worker1
    Users_workers_shift_2 = worker2
    Users_workers_shift_3 = worker3
    
    #shift 1
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] == 0):
            Users_workers_shift_1[i][4] = Users_workers_shift_1[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_1[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_1[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_1[i][11] = Users_workers_shift_1[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_1[i][11] != 0)and (Users_workers_shift_1[i][10] == UNDEF): 
         #   Users_workers_shift_1[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] != 0):
            Users_workers_shift_1[i][3] = day_current + 1 #reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_1)):
        if ((Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and 
                                     (Users_workers_shift_1[i][5] != UNDEF )):
            Users_workers_shift_1[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and (Users_workers_shift_1[i][1] == 1) :
            Users_workers_shift_1[i][12] = Users_workers_shift_1[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_1[i][9] = 'infectious'
            
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][12])and (Users_workers_shift_1[i][9] == 'infectious') :
            #Users_workers_shift_1[i][13] = Users_workers_shift_1[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_1[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_1)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][11]) and  (Users_workers_shift_1[i][10] =='No symptom') and (Users_workers_shift_1[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_1[i][7] = SYMP_YES
            else:
                Users_workers_shift_1[i][7] = SYMP_NO            
    
                
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][7] == SYMP_YES) and (Users_workers_shift_1[i][9] == 'infectious') :
            Users_workers_shift_1[i][8] = REPLACE
            Users_workers_shift_1[i][1] = 0
            Users_workers_shift_1[i][4] = 0
            Users_workers_shift_1[i][5] = UNDEF
            Users_workers_shift_1[i][6] = 0
            Users_workers_shift_1[i][7] = UNDEF
            Users_workers_shift_1[i][9] = UNDEF
            Users_workers_shift_1[i][10] = UNDEF
            Users_workers_shift_1[i][11] = 0
            Users_workers_shift_1[i][12] = 0
            #Users_workers_shift_1[i][13] = 0
            Users_workers_shift_1[i][14] = UNDEF
            
        if (Users_workers_shift_1[i][10] == SYMP_NO)and (Users_workers_shift_1[i][14] == 'immune') : 
            Users_workers_shift_1[i][1] = 0 
            Users_workers_shift_1[i][9] = UNDEF
            
            #shift 2
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] == 0):
            Users_workers_shift_2[i][4] = Users_workers_shift_2[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_2[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_2[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_2[i][11] = Users_workers_shift_2[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_2[i][11] != 0)and (Users_workers_shift_2[i][10] == UNDEF): 
         #   Users_workers_shift_2[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] != 0):
            Users_workers_shift_2[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
     
    for i in range(len(Users_workers_shift_2)):
        if ((Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and 
                                     (Users_workers_shift_2[i][5] != UNDEF )):
            Users_workers_shift_2[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and (Users_workers_shift_2[i][1] == 1) :
            Users_workers_shift_2[i][12] = Users_workers_shift_2[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_2[i][9] = 'infectious'
            
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][12])and (Users_workers_shift_2[i][9] == 'infectious') :
            #Users_workers_shift_2[i][13] = Users_workers_shift_2[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_2[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_2)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][11]) and  (Users_workers_shift_2[i][10] =='No symptom') and (Users_workers_shift_2[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_2[i][7] = SYMP_YES
            else:
                Users_workers_shift_2[i][7] = SYMP_NO            
    

                
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][7] == SYMP_YES) and (Users_workers_shift_2[i][9] == 'infectious') :
            Users_workers_shift_2[i][8] = REPLACE
            Users_workers_shift_2[i][1] = 0
            Users_workers_shift_2[i][4] = 0
            Users_workers_shift_2[i][5] = UNDEF
            Users_workers_shift_2[i][6] = 0
            Users_workers_shift_2[i][7] = UNDEF
            Users_workers_shift_2[i][9] = UNDEF
            Users_workers_shift_2[i][10] = UNDEF
            Users_workers_shift_2[i][11] = 0
            Users_workers_shift_2[i][12] = 0
            #Users_workers_shift_2[i][13] = 0
            Users_workers_shift_2[i][14] = UNDEF
            
        if (Users_workers_shift_2[i][10] == SYMP_NO)and (Users_workers_shift_2[i][14] == 'immune') : 
            Users_workers_shift_2[i][1] = 0 
            Users_workers_shift_2[i][9] = UNDEF
            
            #shift 3
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] == 0):
            Users_workers_shift_3[i][4] = Users_workers_shift_3[i][3] + 3 #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_3[i][9] = 'Not_Infectious'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_3[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_3[i][11] = Users_workers_shift_3[i][3] + 5 #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_3[i][11] != 0)and (Users_workers_shift_3[i][10] == UNDEF): 
         #   Users_workers_shift_3[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] != 0):
            Users_workers_shift_3[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_3)):
        if ((Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and 
                                     (Users_workers_shift_3[i][5] != UNDEF )):
            Users_workers_shift_3[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and (Users_workers_shift_3[i][1] == 1) :
            Users_workers_shift_3[i][12] = Users_workers_shift_3[i][3] + 5 #infectious , can spread infections after 5 days
            Users_workers_shift_3[i][9] = 'infectious'
            
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][12])and (Users_workers_shift_3[i][9] == 'infectious') :
            #Users_workers_shift_3[i][13] = Users_workers_shift_3[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_3[i][14] = 'immune'
                      
        
    for i in range(len(Users_workers_shift_3)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][11]) and  (Users_workers_shift_3[i][10] =='No symptom') and (Users_workers_shift_3[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_3[i][7] = SYMP_YES
            else:
                Users_workers_shift_3[i][7] = SYMP_NO            
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][7] == SYMP_YES) and (Users_workers_shift_3[i][9] == 'infectious') :
            Users_workers_shift_3[i][8] = REPLACE
            Users_workers_shift_3[i][1] = 0
            Users_workers_shift_3[i][4] = 0
            Users_workers_shift_3[i][5] = UNDEF
            Users_workers_shift_3[i][6] = 0
            Users_workers_shift_3[i][7] = UNDEF
            Users_workers_shift_3[i][9] = UNDEF
            Users_workers_shift_3[i][10] = UNDEF
            Users_workers_shift_3[i][11] = 0
            Users_workers_shift_3[i][12] = 0
            #Users_workers_shift_3[i][13] = 0
            Users_workers_shift_3[i][14] = UNDEF
            
                                                
        if (Users_workers_shift_3[i][10] == SYMP_NO)and (Users_workers_shift_3[i][14] == 'immune') : 
            Users_workers_shift_3[i][1] = 0 
            Users_workers_shift_3[i][9] = UNDEF
    
    return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3


def workers_count_shift_1(User, day, count):
    RECEP_from_shift_1 = count[0]
    TRIAG_from_shift_1 = count[1]
    TRIAG_U_from_shift_1 = count[2]
    N_URG_from_shift_1 = count[3]
    N_N_URG_from_shift_1 = count[4]
    DR_URGE_from_shift_1 = count[5]
    DR_N_URG_from_shift_1= count[6]
    IMAGI_from_shift_1=  count[7]
    LABOR_from_shift_1= count[8]
    ARE_test_from_shift_1 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from_shift_1.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from_shift_1.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from_shift_1.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and
                                            (Users[i][9] == ARE_test)):
            cont_day = cont_day + 1
    ARE_test_from_shift_1.append([day,cont_day]) 
    
    count= [RECEP_from_shift_1, TRIAG_from_shift_1,TRIAG_U_from_shift_1, 
                     N_URG_from_shift_1, N_N_URG_from_shift_1,DR_URGE_from_shift_1,
                     DR_N_URG_from_shift_1, IMAGI_from_shift_1, LABOR_from_shift_1,ARE_test_from_shift_1 ]
    
    return count




def workers_count_shift_2(User, day, count):
    RECEP_from_shift_2 = count[0]
    TRIAG_from_shift_2 = count[1]
    TRIAG_U_from_shift_2 = count[2]
    N_URG_from_shift_2 = count[3]
    N_N_URG_from_shift_2 = count[4]
    DR_URGE_from_shift_2 = count[5]
    DR_N_URG_from_shift_2= count[6]
    IMAGI_from_shift_2=  count[7]
    LABOR_from_shift_2= count[8]
    ARE_test_from_shift_2 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from_shift_2.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from_shift_2.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from_shift_2.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                            (Users[i][9] == ARE_test)):
            cont_day = cont_day + 1
    ARE_test_from_shift_2.append([day,cont_day]) 
    
    count= [RECEP_from_shift_2, TRIAG_from_shift_2,TRIAG_U_from_shift_2, 
                     N_URG_from_shift_2, N_N_URG_from_shift_2,DR_URGE_from_shift_2,
                     DR_N_URG_from_shift_2, IMAGI_from_shift_2, LABOR_from_shift_2,ARE_test_from_shift_2 ]
    
    return count




def workers_count_shift_3(User, day, count):
    RECEP_from_shift_3 = count[0]
    TRIAG_from_shift_3 = count[1]
    TRIAG_U_from_shift_3 = count[2]
    N_URG_from_shift_3 = count[3]
    N_N_URG_from_shift_3 = count[4]
    DR_URGE_from_shift_3 = count[5]
    DR_N_URG_from_shift_3= count[6]
    IMAGI_from_shift_3=  count[7]
    LABOR_from_shift_3= count[8]
    ARE_test_from_shift_3 = count[9]
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == RECEP)):
            cont_day = cont_day + 1
    RECEP_from_shift_3.append([day,cont_day])    
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == TRIAG)):
            cont_day = cont_day + 1
    TRIAG_from_shift_3.append([day,cont_day])   
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == TRIAG_U)):
            cont_day = cont_day + 1
    TRIAG_U_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == N_URGE)):
            cont_day = cont_day + 1
    N_URG_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == N_N_URG)):
            cont_day = cont_day + 1
    N_N_URG_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == DR_URGE)):
            cont_day = cont_day + 1
    DR_URGE_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == D_N_URG)):
            cont_day = cont_day + 1
    DR_N_URG_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == IMAGI)):
            cont_day = cont_day + 1
    IMAGI_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == LABOR)):
            cont_day = cont_day + 1
    LABOR_from_shift_3.append([day,cont_day])
    
    cont_day = 0
    for i in range(len(Users)):
        if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                            (Users[i][9] == ARE_test)):
            cont_day = cont_day + 1
    ARE_test_from_shift_3.append([day,cont_day]) 
    
    count= [RECEP_from_shift_3, TRIAG_from_shift_3,TRIAG_U_from_shift_3, 
                     N_URG_from_shift_3, N_N_URG_from_shift_3,DR_URGE_from_shift_3,
                     DR_N_URG_from_shift_3, IMAGI_from_shift_3, LABOR_from_shift_3,ARE_test_from_shift_3 ]
    
    return count


def percent_staff_shift_1(worker_1, workers_count_1, count_from):
    cont_from_w_shift_1 = count_from
    RECEP_from_shift_1 = workers_count_1[0]
    TRIAG_from_shift_1 = workers_count_1[1]
    TRIAG_U_from_shift_1 = workers_count_1[2]
    N_URG_from_shift_1 = workers_count_1[3]
    N_N_URG_from_shift_1 = workers_count_1[4]
    DR_URGE_from_shift_1 = workers_count_1[5]
    DR_N_URG_from_shift_1= workers_count_1[6]
    IMAGI_from_shift_1=  workers_count_1[7]
    LABOR_from_shift_1= workers_count_1[8]
    ARE_test_from_shift_1 = workers_count_1[9]
    
    
    port_RECEP_from_shift_1 = worker_1[0]
    port_TRIAG_from_shift_1 = worker_1[1]
    port_TRIAG_U_from_shift_1 = worker_1[2]
    port_N_URG_from_shift_1 = worker_1[3]
    port_N_N_URG_from_shift_1 = worker_1[4]
    port_DR_URGE_from_shift_1 = worker_1[5]
    port_DR_N_URG_from_shift_1= worker_1[6]
    port_IMAGI_from_shift_1=  worker_1[7]
    port_LABOR_from_shift_1= worker_1[8]
    port_ARE_test_from_shift_1 = worker_1[9]

    

    count = 0
    for i in range(len(RECEP_from_shift_1)):
        if  RECEP_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (RECEP_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_RECEP_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_1.append([i,count])


    count = 0
    for i in range(len(TRIAG_from_shift_1)):
        if TRIAG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (TRIAG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_TRIAG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_1.append([i,count])
        

    count = 0
    for i in range(len(TRIAG_U_from_shift_1)):
        if TRIAG_U_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (TRIAG_U_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_TRIAG_U_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_U_from_shift_1.append([i,count])



    count = 0
    for i in range(len(N_URG_from_shift_1)):
        if N_URG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (N_URG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_N_URG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_N_URG_from_shift_1.append([i,count])



    count = 0
    for i in range(len(N_N_URG_from_shift_1)):
        if N_N_URG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (N_N_URG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_N_N_URG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_1.append([i,count])
        


    count = 0
    for i in range(len(DR_URGE_from_shift_1)):
        if DR_URGE_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (DR_URGE_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_DR_URGE_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_URGE_from_shift_1.append([i,count])


    count = 0
    for i in range(len(DR_N_URG_from_shift_1)):
        if DR_N_URG_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (DR_N_URG_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_DR_N_URG_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_1.append([i,count])
        

    count = 0
    for i in range(len(IMAGI_from_shift_1)):
        if IMAGI_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (IMAGI_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_IMAGI_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_1.append([i,count])
        
    count = 0
    for i in range(len(LABOR_from_shift_1)):
        if LABOR_from_shift_1[i][1] != 0 and cont_from_w_shift_1[i][1] != 0:
            count = (LABOR_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_LABOR_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_1.append([i,count])
        

    count = 0
    for i in range(len(ARE_test_from_shift_1)):
        if ARE_test_from_shift_1[i][1] != 0 and ARE_test_from_shift_1[i][1] != 0:
            count = (ARE_test_from_shift_1[i][1]*100) / cont_from_w_shift_1[i][1]
            port_ARE_test_from_shift_1.append([i,count])
            count = 0
        else:
            count = 0
            port_ARE_test_from_shift_1.append([i,count])

            
    worker_1 =  [port_RECEP_from_shift_1, port_TRIAG_from_shift_1,port_TRIAG_U_from_shift_1, 
                     port_N_URG_from_shift_1, port_N_N_URG_from_shift_1,port_DR_URGE_from_shift_1,
                     port_DR_N_URG_from_shift_1, port_IMAGI_from_shift_1, port_LABOR_from_shift_1,
                     port_ARE_test_from_shift_1 ]
            
    
    return worker_1


def percent_staff_shift_2(worker_2,workers_count_2,count_from):
    cont_from_w_shift_2 = count_from
    RECEP_from_shift_2 = workers_count_2[0]
    TRIAG_from_shift_2 = workers_count_2[1]
    TRIAG_U_from_shift_2 = workers_count_2[2]
    N_URG_from_shift_2 = workers_count_2[3]
    N_N_URG_from_shift_2 = workers_count_2[4]
    DR_URGE_from_shift_2 = workers_count_2[5]
    DR_N_URG_from_shift_2= workers_count_2[6]
    IMAGI_from_shift_2=  workers_count_2[7]
    LABOR_from_shift_2= workers_count_2[8]
    ARE_test_from_shift_2 = workers_count_2[9]
    
    port_RECEP_from_shift_2 = worker_2[0]
    port_TRIAG_from_shift_2 = worker_2[1]
    port_TRIAG_U_from_shift_2 = worker_2[2]
    port_N_URG_from_shift_2 = worker_2[3]
    port_N_N_URG_from_shift_2 = worker_2[4]
    port_DR_URGE_from_shift_2 = worker_2[5]
    port_DR_N_URG_from_shift_2= worker_2[6]
    port_IMAGI_from_shift_2=  worker_2[7]
    port_LABOR_from_shift_2= worker_2[8]
    port_ARE_test_from_shift_2 = worker_2[9]

    count = 0
    for i in range(len(RECEP_from_shift_2)):
        if RECEP_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (RECEP_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_RECEP_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_2.append([i,count])



    count = 0
    for i in range(len(TRIAG_from_shift_2)):
        if TRIAG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (TRIAG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_TRIAG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_2.append([i,count])
        

    count = 0
    for i in range(len(TRIAG_U_from_shift_2)):
        if TRIAG_U_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (TRIAG_U_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_TRIAG_U_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_U_from_shift_2.append([i,count])



    count = 0
    for i in range(len(N_URG_from_shift_2)):
        if N_URG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (N_URG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_N_URG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_N_URG_from_shift_2.append([i,count])


    count = 0
    for i in range(len(N_N_URG_from_shift_2)):
        if N_N_URG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (N_N_URG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_N_N_URG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_2.append([i,count])
        

    count = 0
    for i in range(len(DR_URGE_from_shift_2)):
        if DR_URGE_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (DR_URGE_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_DR_URGE_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_URGE_from_shift_2.append([i,count])



    count = 0
    for i in range(len(DR_N_URG_from_shift_2)):
        if DR_N_URG_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (DR_N_URG_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_DR_N_URG_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_2.append([i,count])
        

    count = 0
    for i in range(len(IMAGI_from_shift_2)):
        if IMAGI_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (IMAGI_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_IMAGI_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_2.append([i,count])
        


    count = 0
    for i in range(len(LABOR_from_shift_2)):
        if LABOR_from_shift_2[i][1] != 0 and cont_from_w_shift_2[i][1] != 0:
            count = (LABOR_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_LABOR_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_2.append([i,count])
        
        

    count = 0
    for i in range(len(ARE_test_from_shift_2)):
        if ARE_test_from_shift_2[i][1] != 0 and ARE_test_from_shift_2[i][1] != 0:
            count = (ARE_test_from_shift_2[i][1]*100) / cont_from_w_shift_2[i][1]
            port_ARE_test_from_shift_2.append([i,count])
            count = 0
        else:
            count = 0
            port_ARE_test_from_shift_2.append([i,count])

            
    worker_2 =  [port_RECEP_from_shift_2, port_TRIAG_from_shift_2,port_TRIAG_U_from_shift_2, 
                     port_N_URG_from_shift_2, port_N_N_URG_from_shift_2,port_DR_URGE_from_shift_2,
                     port_DR_N_URG_from_shift_2, port_IMAGI_from_shift_2, port_LABOR_from_shift_2,
                     port_ARE_test_from_shift_2 ]
            
    
    return worker_2



def percent_staff_shift_3(worker_3,workers_count_3,count_from):
    cont_from_w_shift_3 = count_from
    RECEP_from_shift_3 = workers_count_3[0]
    TRIAG_from_shift_3 = workers_count_3[1]
    TRIAG_U_from_shift_3 = workers_count_3[2]
    N_URG_from_shift_3 = workers_count_3[3]
    N_N_URG_from_shift_3 = workers_count_3[4]
    DR_URGE_from_shift_3 = workers_count_3[5]
    DR_N_URG_from_shift_3= workers_count_3[6]
    IMAGI_from_shift_3=  workers_count_3[7]
    LABOR_from_shift_3= workers_count_3[8]
    ARE_test_from_shift_3 = workers_count_3[9]
    
    port_RECEP_from_shift_3 = worker_3[0]
    port_TRIAG_from_shift_3 = worker_3[1]
    port_TRIAG_U_from_shift_3 = worker_3[2]
    port_N_URG_from_shift_3 = worker_3[3]
    port_N_N_URG_from_shift_3 = worker_3[4]
    port_DR_URGE_from_shift_3 = worker_3[5]
    port_DR_N_URG_from_shift_3= worker_3[6]
    port_IMAGI_from_shift_3=  worker_3[7]
    port_LABOR_from_shift_3= worker_3[8]
    port_ARE_test_from_shift_3 = worker_3[9]


    count = 0
    for i in range(len(RECEP_from_shift_3)):
        if RECEP_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (RECEP_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_RECEP_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_RECEP_from_shift_3.append([i,count])

    count = 0
    for i in range(len(TRIAG_from_shift_3)):
        if TRIAG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (TRIAG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_TRIAG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_from_shift_3.append([i,count])
        

    count = 0
    for i in range(len(TRIAG_U_from_shift_3)):
        if TRIAG_U_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (TRIAG_U_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_TRIAG_U_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_TRIAG_U_from_shift_3.append([i,count])

    count = 0
    for i in range(len(N_URG_from_shift_3)):
        if N_URG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (N_URG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_N_URG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_N_URG_from_shift_3.append([i,count])


    count = 0
    for i in range(len(N_N_URG_from_shift_3)):
        if N_N_URG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (N_N_URG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_N_N_URG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_N_N_URG_from_shift_3.append([i,count])
        
    count = 0
    for i in range(len(DR_URGE_from_shift_3)):
        if DR_URGE_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (DR_URGE_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_DR_URGE_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_URGE_from_shift_3.append([i,count])

    count = 0
    for i in range(len(DR_N_URG_from_shift_3)):
        if DR_N_URG_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (DR_N_URG_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_DR_N_URG_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_DR_N_URG_from_shift_3.append([i,count])

    count = 0
    for i in range(len(IMAGI_from_shift_3)):
        if IMAGI_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (IMAGI_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_IMAGI_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_IMAGI_from_shift_3.append([i,count])
        


    count = 0
    for i in range(len(LABOR_from_shift_3)):
        if LABOR_from_shift_3[i][1] != 0 and cont_from_w_shift_3[i][1] != 0:
            count = (LABOR_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_LABOR_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_LABOR_from_shift_3.append([i,count])
        
        
    count = 0
    for i in range(len(ARE_test_from_shift_3)):
        if ARE_test_from_shift_3[i][1] != 0 and ARE_test_from_shift_3[i][1] != 0:
            count = (ARE_test_from_shift_3[i][1]*100) / cont_from_w_shift_3[i][1]
            port_ARE_test_from_shift_3.append([i,count])
            count = 0
        else:
            count = 0
            port_ARE_test_from_shift_3.append([i,count])

            
    worker_3 =  [port_RECEP_from_shift_3, port_TRIAG_from_shift_3,port_TRIAG_U_from_shift_3, 
                     port_N_URG_from_shift_3, port_N_N_URG_from_shift_3,port_DR_URGE_from_shift_3,
                     port_DR_N_URG_from_shift_3, port_IMAGI_from_shift_3, port_LABOR_from_shift_3,
                     port_ARE_test_from_shift_3 ]
            
    
    return worker_3








def big_func():
    global Time_var
    N_new_day_from_w = []
    N_new_day_work = []
    N_new_day = []
    N_waiting_H = []
    
    Result_worker = []
    
    N_new_day_from_shift_1 = []
    N_new_day_from_shift_2 = []
    N_new_day_from_shift_3 = []
    
    port_RECEP_from_shift_1  =[]
    port_TRIAG_from_shift_1 =[]
    port_TRIAG_U_from_shift_1  =[]
    port_N_URG_from_shift_1 =[]
    port_N_N_URG_from_shift_1  =[]
    port_DR_URGE_from_shift_1  =[]
    port_DR_N_URG_from_shift_1 =[]
    port_IMAGI_from_shift_1 =[]
    port_LABOR_from_shift_1 =[]
    port_ARE_test_from_shift_1 =[]
    
    port_RECEP_from_shift_2  =[]
    port_TRIAG_from_shift_2 =[]
    port_TRIAG_U_from_shift_2  =[]
    port_N_URG_from_shift_2 =[]
    port_N_N_URG_from_shift_2  =[]
    port_DR_URGE_from_shift_2  =[]
    port_DR_N_URG_from_shift_2 =[]
    port_IMAGI_from_shift_2 =[]
    port_LABOR_from_shift_2 =[]
    port_ARE_test_from_shift_2 =[]
    
    port_RECEP_from_shift_3  =[]
    port_TRIAG_from_shift_3 =[]
    port_TRIAG_U_from_shift_3  =[]
    port_N_URG_from_shift_3 =[]
    port_N_N_URG_from_shift_3  =[]
    port_DR_URGE_from_shift_3  =[]
    port_DR_N_URG_from_shift_3 =[]
    port_IMAGI_from_shift_3 =[]
    port_LABOR_from_shift_3 =[]
    port_ARE_test_from_shift_3 =[]
    
    
    
    RECEP_from_shift_1 = []
    TRIAG_from_shift_1 = []
    TRIAG_U_from_shift_1 = []
    N_URG_from_shift_1 = []
    N_N_URG_from_shift_1 = []
    IMAGI_from_shift_1 = []
    LABOR_from_shift_1 = []
    DR_URGE_from_shift_1 = []
    DR_N_URG_from_shift_1 = []
    ARE_test_from_shift_1 = []
                           
    RECEP_from_shift_2 = []
    TRIAG_from_shift_2 = []
    TRIAG_U_from_shift_2 = []
    N_URG_from_shift_2 = []
    N_N_URG_from_shift_2 = []
    IMAGI_from_shift_2 = []
    LABOR_from_shift_2 = []
    DR_URGE_from_shift_2 = []
    DR_N_URG_from_shift_2 = []
    ARE_test_from_shift_2 = []
    
    RECEP_from_shift_3 = []
    TRIAG_from_shift_3 = []
    TRIAG_U_from_shift_3 = []
    N_URG_from_shift_3 = []
    N_N_URG_from_shift_3 = []
    IMAGI_from_shift_3 = []
    LABOR_from_shift_3 = []
    DR_URGE_from_shift_3 = []
    DR_N_URG_from_shift_3 = []
    ARE_test_from_shift_3 = []
     
    Result_user = []
    

    nday  = N_days
    for day in range(nday):
        day_current = day
        while Time_var < Time_scale:
            if (Time_var >= shift_1[0]) and (Time_var <= shift_1[1]):
                arrival_method(Time_var)
                
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF: 
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:#area time counter = area time
                            area_desit_tree(Users[k],k)
       
                        # Set position matrix if Waiting area
                        #   1. position in Matrix, where availeable seat 
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1) #10 by 4 matrix
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1 #current user k is in the position of seat map
        #------------------------------------------------------------------------------    
             
                            
                        elif Users[k][4] == Users[k][6]: #area time = interact moment
                            action_desit_tree_shift_1(Users[k],k,day)                  
                            sitting_arrangement(k, day)
    
           
                    #second shift
    
            if (Time_var >= shift_2[0]) and (Time_var <= shift_2[1]):
                arrival_method(Time_var)
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF: 
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:#area time counter = area time
                            area_desit_tree(Users[k],k)
       
                        # Set position matrix if Waiting area
                        #   1. position in Matrix, where availeable seat 
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1) #10 by 4 matrix
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1 #current user k is in the position of seat map
        #------------------------------------------------------------------------------    
             
                            
                        elif Users[k][4] == Users[k][6]: #area time = interact moment
                            action_desit_tree_shift_2(Users[k],k,day)                  
                            sitting_arrangement(k, day)
                    
            
            
                                     #third shift
    
            if (Time_var >= shift_3[0]) and (Time_var <= shift_3[1]):
                arrival_method(Time_var)
                for k in range(Num_Aget):
                    if Users[k][2] != UNDEF: 
                        Curr_time = Users[k][4]
                        Users[k][4] = Curr_time + 1
                        if Users[k][4] == Users[k][3]:#area time counter = area time
                            area_desit_tree(Users[k],k)
       
                            if Users[k][2] == WAI_N:
                                Seated = 0 
                                while Seated == 0:
                                    indx_1 =  np.random.randint(0, high=4, size=1) #10 by 4 matrix
                                    indx_2 =  np.random.randint(0, high=10, size=1)
                                    if Seat_map[indx_1[0],indx_2[0]] == 0:
                                        Seat_map[indx_1[0],indx_2[0]] = Users[k][0]
                                        Seated = 1 #current user k is in the position of seat map
        #------------------------------------------------------------------------------    
             
                            
                        elif Users[k][4] == Users[k][6]: #area time = interact moment
                            action_desit_tree_shift_3(Users[k],k,day)                  
                            sitting_arrangement(k, day)
            
            
            Time_var = Time_var + 1
        
        print(day+1)
        
        
        
        Users_workers_shift_1 = []
        Users_workers_shift_2= []
        Users_workers_shift_3= []
       
        staff_shift  = workers_settings(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3)
        Users_workers_shift_1 = staff_shift[0]
        Users_workers_shift_2 = staff_shift[1]
        Users_workers_shift_3 = staff_shift[2]
    
        staff_shift_status = workers_settings_status(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3, day_current)
        Users_workers_shift_1 = staff_shift_status[0]
        Users_workers_shift_2 = staff_shift_status[1]
        Users_workers_shift_3 = staff_shift_status[2]
    
        curr_user = Users
        Result_user.extend(curr_user)
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                                                (Users[i][9] == WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day +1
        N_new_day.append([day,cont_use_day])
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and 
                                                (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day +1
        N_new_day_from_w.append([day,cont_use_day])
        
        
        ##staff 1
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff1") and (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day +1
        N_new_day_from_shift_1.append([day,cont_use_day])
        ##staff 2
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff2") and
                                                (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day +1
        N_new_day_from_shift_2.append([day,cont_use_day])    
        
        ##staff 3
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (Users[i][11] == "Staff3") and
                                                (Users[i][9] != WAI_N+' -PATIENT')):
                cont_use_day = cont_use_day +1
        N_new_day_from_shift_3.append([day,cont_use_day])   
    
        workers_count_1 = [RECEP_from_shift_1, TRIAG_from_shift_1,TRIAG_U_from_shift_1, 
                         N_URG_from_shift_1, N_N_URG_from_shift_1,DR_URGE_from_shift_1,
                         DR_N_URG_from_shift_1, IMAGI_from_shift_1, LABOR_from_shift_1,ARE_test_from_shift_1 ]
    
        workers_count_1 = workers_count_shift_1(Users, day_current, workers_count_1)
        RECEP_from_shift_1 = workers_count_1[0]
        TRIAG_from_shift_1 = workers_count_1[1]
        TRIAG_U_from_shift_1 = workers_count_1[2]
        N_URG_from_shift_1 = workers_count_1[3]
        N_N_URG_from_shift_1 = workers_count_1[4]
        DR_URGE_from_shift_1 = workers_count_1[5]
        DR_N_URG_from_shift_1= workers_count_1[6]
        IMAGI_from_shift_1=  workers_count_1[7]
        LABOR_from_shift_1= workers_count_1[8]
        ARE_test_from_shift_1 = workers_count_1[9]
        
        workers_count_2 = [RECEP_from_shift_2, TRIAG_from_shift_2,TRIAG_U_from_shift_2, 
                         N_URG_from_shift_2, N_N_URG_from_shift_2,DR_URGE_from_shift_2,
                         DR_N_URG_from_shift_2, IMAGI_from_shift_2, LABOR_from_shift_2,ARE_test_from_shift_2 ]
    
        workers_count_2 = workers_count_shift_2(Users, day_current, workers_count_2)
        RECEP_from_shift_2 = workers_count_2[0]
        TRIAG_from_shift_2 = workers_count_2[1]
        TRIAG_U_from_shift_2 = workers_count_2[2]
        N_URG_from_shift_2 = workers_count_2[3]
        N_N_URG_from_shift_2 = workers_count_2[4]
        DR_URGE_from_shift_2 = workers_count_2[5]
        DR_N_URG_from_shift_2= workers_count_2[6]
        IMAGI_from_shift_2=  workers_count_2[7]
        LABOR_from_shift_2= workers_count_2[8]
        ARE_test_from_shift_2 = workers_count_2[9]
        
        workers_count_3 = [RECEP_from_shift_3, TRIAG_from_shift_3,TRIAG_U_from_shift_3, 
                         N_URG_from_shift_3, N_N_URG_from_shift_3,DR_URGE_from_shift_3,
                         DR_N_URG_from_shift_3, IMAGI_from_shift_3, LABOR_from_shift_3,ARE_test_from_shift_3 ]
    
        workers_count_3 = workers_count_shift_3(Users, day_current, workers_count_3)
        RECEP_from_shift_3 = workers_count_3[0]
        TRIAG_from_shift_3 = workers_count_3[1]
        TRIAG_U_from_shift_3 = workers_count_3[2]
        N_URG_from_shift_3 = workers_count_3[3]
        N_N_URG_from_shift_3 = workers_count_3[4]
        DR_URGE_from_shift_3 = workers_count_3[5]
        DR_N_URG_from_shift_3= workers_count_3[6]
        IMAGI_from_shift_3=  workers_count_3[7]
        LABOR_from_shift_3= workers_count_3[8]
        ARE_test_from_shift_3 = workers_count_3[9]
        
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
    
    
    cont_from_w_shift_1 = []
    cont_day = 0
    for i in range(len(LABOR_from_shift_1)):
        cont_day = (cont_day + RECEP_from_shift_1[i][1] + TRIAG_from_shift_1[i][1] + TRIAG_U_from_shift_1[i][1]
                    + N_URG_from_shift_1[i][1]
                    + N_N_URG_from_shift_1[i][1]
                    + DR_URGE_from_shift_1[i][1]
                    + DR_N_URG_from_shift_1[i][1]
                    + IMAGI_from_shift_1[i][1]
                    + LABOR_from_shift_1[i][1]
                    + ARE_test_from_shift_1[i][1])
        cont_from_w_shift_1.append([i,cont_day])
        cont_day = 0
        
    cont_from_w_shift_2 = []
    cont_day = 0
    for i in range(len(LABOR_from_shift_2)):
        cont_day = (cont_day + RECEP_from_shift_2[i][1] + TRIAG_from_shift_2[i][1] + TRIAG_U_from_shift_2[i][1]
                    + N_URG_from_shift_2[i][1]
                    + N_N_URG_from_shift_2[i][1]
                    + DR_URGE_from_shift_2[i][1]
                    + DR_N_URG_from_shift_2[i][1]
                    + IMAGI_from_shift_2[i][1]
                    + LABOR_from_shift_2[i][1]
                    + ARE_test_from_shift_2[i][1])
        cont_from_w_shift_2.append([i,cont_day])
        cont_day = 0
        
    cont_from_w_shift_3 = []
    cont_day = 0
    for i in range(len(LABOR_from_shift_3)):
        cont_day = (cont_day + RECEP_from_shift_3[i][1] + TRIAG_from_shift_3[i][1] + TRIAG_U_from_shift_3[i][1]
                    + N_URG_from_shift_3[i][1]
                    + N_N_URG_from_shift_3[i][1]
                    + DR_URGE_from_shift_3[i][1]
                    + DR_N_URG_from_shift_3[i][1]
                    + IMAGI_from_shift_3[i][1]
                    + LABOR_from_shift_3[i][1]
                    + ARE_test_from_shift_3[i][1])
        cont_from_w_shift_3.append([i,cont_day])
        cont_day = 0
            
    cont_tot_w = []
    cont_day = 0
    for i in range(len(N_new_day)):
        cont_day = N_new_day[i][1] + N_new_day_from_w[i][1]
        cont_tot_w.append([i,cont_day])
        cont_day = 0
    
    
    
    worker_1 =  [port_RECEP_from_shift_1, port_TRIAG_from_shift_1,port_TRIAG_U_from_shift_1, 
                         port_N_URG_from_shift_1, port_N_N_URG_from_shift_1,port_DR_URGE_from_shift_1,
                         port_DR_N_URG_from_shift_1, port_IMAGI_from_shift_1, port_LABOR_from_shift_1,
                         port_ARE_test_from_shift_1 ]
                
                        
    per_staff_count_1 = percent_staff_shift_1(worker_1,workers_count_1,cont_from_w_shift_1)
    port_RECEP_from_shift_1 = per_staff_count_1[0]
    port_TRIAG_from_shift_1 = per_staff_count_1[1]
    port_TRIAG_U_from_shift_1 = per_staff_count_1[2]
    port_N_URG_from_shift_1 = per_staff_count_1[3]
    port_N_N_URG_from_shift_1 = per_staff_count_1[4]
    port_DR_URGE_from_shift_1 = per_staff_count_1[5]
    port_DR_N_URG_from_shift_1= per_staff_count_1[6]
    port_IMAGI_from_shift_1=  per_staff_count_1[7]
    port_LABOR_from_shift_1= per_staff_count_1[8]
    port_ARE_test_from_shift_1 = per_staff_count_1[9]
        
        
    worker_2 =  [port_RECEP_from_shift_2, port_TRIAG_from_shift_2,port_TRIAG_U_from_shift_2, 
                         port_N_URG_from_shift_2, port_N_N_URG_from_shift_2,port_DR_URGE_from_shift_2,
                         port_DR_N_URG_from_shift_2, port_IMAGI_from_shift_2, port_LABOR_from_shift_2,
                         port_ARE_test_from_shift_2 ]
    
    per_staff_count_2 = percent_staff_shift_2(worker_2,workers_count_2,cont_from_w_shift_2)
    port_RECEP_from_shift_2 = per_staff_count_2[0]
    port_TRIAG_from_shift_2 = per_staff_count_2[1]
    port_TRIAG_U_from_shift_2 = per_staff_count_2[2]
    port_N_URG_from_shift_2 = per_staff_count_2[3]
    port_N_N_URG_from_shift_2 = per_staff_count_2[4]
    port_DR_URGE_from_shift_2 = per_staff_count_2[5]
    port_DR_N_URG_from_shift_2= per_staff_count_2[6]
    port_IMAGI_from_shift_2=  per_staff_count_2[7]
    port_LABOR_from_shift_2= per_staff_count_2[8]
    port_ARE_test_from_shift_2 = per_staff_count_2[9]
    
        
    worker_3 =  [port_RECEP_from_shift_3, port_TRIAG_from_shift_3,port_TRIAG_U_from_shift_3, 
                         port_N_URG_from_shift_3, port_N_N_URG_from_shift_3,port_DR_URGE_from_shift_3,
                         port_DR_N_URG_from_shift_3, port_IMAGI_from_shift_3, port_LABOR_from_shift_3,
                         port_ARE_test_from_shift_3 ]  
    
    per_staff_count_3 = percent_staff_shift_3(worker_3,workers_count_3,cont_from_w_shift_3)
    port_RECEP_from_shift_3 = per_staff_count_3[0]
    port_TRIAG_from_shift_3 = per_staff_count_3[1]
    port_TRIAG_U_from_shift_3 = per_staff_count_3[2]
    port_N_URG_from_shift_3 = per_staff_count_3[3]
    port_N_N_URG_from_shift_3 = per_staff_count_3[4]
    port_DR_URGE_from_shift_3 = per_staff_count_3[5]
    port_DR_N_URG_from_shift_3= per_staff_count_3[6]
    port_IMAGI_from_shift_3=  per_staff_count_3[7]
    port_LABOR_from_shift_3= per_staff_count_3[8]
    port_ARE_test_from_shift_3 = per_staff_count_3[9]
    
    #-----------------------------------------------------------------------------
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
    porcent_are_test = []


    for i in range(len(N_new_day_from_shift_1)):
        pat_tot.append(N_new_day_from_shift_1[i][1])##number of infected patient
        staff_plot.append(N_new_day_from_shift_1[i][1])#number of infected staff
        days_plot.append(N_new_day_from_shift_1[i][0]+1) #number of day
        porcent_recep.append(port_RECEP_from_shift_1[i][1])
        porcent_triag.append(port_TRIAG_from_shift_1[i][1])
        porcent_tria_u.append(port_TRIAG_U_from_shift_1[i][1])
        porcent_N_urge.append(port_N_URG_from_shift_1[i][1])
        porcent_N_N_ur.append(port_N_N_URG_from_shift_1[i][1])
        porcent_dr_urg.append(port_DR_URGE_from_shift_1[i][1])
        porcent_dr_n_u.append(port_DR_N_URG_from_shift_1[i][1])
        porcent_labora.append(port_LABOR_from_shift_1[i][1])
        porcent_imagin.append(port_IMAGI_from_shift_1[i][1])
        porcent_are_test.append(port_ARE_test_from_shift_1[i][1])
    

    
        result_list =   {"Number of infected patient": pat_tot,
                      "Number of infected staff":staff_plot,
                      "Number of days":days_plot,
                      "Users workers shift 1":Users_workers_shift_1,
                      "Users workers shift 2":Users_workers_shift_2,
                      "Users workers shift 3":Users_workers_shift_3,
                      "workers_count_1" : workers_count_1,
                      "workers_count_2" : workers_count_2,
                      "workers_count_3" : workers_count_3,
                      "workers_count_1, percentage prop" : worker_1,
                      "workers_count_2, percentage prop" : worker_2,
                      "workers_count_3, percentage prop" : worker_3,
                      "cont_from_w_shift_1" : cont_from_w_shift_1,
                      "cont_from_w_shift_2" : cont_from_w_shift_2,
                      "cont_from_w_shift_3" : cont_from_w_shift_3}


    return result_list


