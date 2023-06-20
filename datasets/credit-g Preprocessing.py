# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 12:43:16 2023

@author: zhuyf
"""

import pandas as pd

data = pd.read_csv("credit-g_quant_unprocessed.csv")
columns = data.columns.values #Attributes + "class"

print(data[:5])
print(len(data.axes[0]))
for instance in range(len(data.axes[0])):
    #checking status
    if data.at[instance,columns[0]]=="0<=X<200":
        data.loc[instance, columns[0]] = "100"
    elif data.at[instance,columns[0]]==">=200":
        data.loc[instance, columns[0]] = "200"
    else: 
        data.loc[instance, columns[0]] = "0"
    
    #savings_status
    if data.at[instance,columns[3]]=="100<=X<500":
        data.loc[instance, columns[3]] = "300"
    elif data.at[instance,columns[3]]=="500<=X<1000":
        data.loc[instance, columns[3]] = "750"
    elif data.at[instance,columns[3]]==">=1000":
        data.loc[instance, columns[3]] = "1000"
    else: 
        data.loc[instance, columns[3]] = "0"
    
    #employment
    if data.at[instance,columns[4]]=="1<=X<4":
        data.loc[instance, columns[4]] = "2.5"
    elif data.at[instance,columns[4]]=="4<=X<7":
        data.loc[instance, columns[4]] = "5.5"
    elif data.at[instance,columns[4]]==">=7":
        data.loc[instance, columns[4]] = "7"
    else: 
        data.loc[instance, columns[4]] = "0"
        
    #own telephone
    if data.at[instance,columns[10]]=="yes":
        data.loc[instance, columns[10]] = "1" 
    else: 
        data.loc[instance, columns[10]] = "0"
        
    #foreign worker
    if data.at[instance,columns[11]]=="yes":
        data.loc[instance, columns[11]] = "1" 
    else: 
        data.loc[instance, columns[11]] = "0"

data.to_csv("credit-g_quant_unprocessed_2.csv", index=False)
print("done")