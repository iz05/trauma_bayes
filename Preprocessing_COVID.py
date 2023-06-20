# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:49:33 2023

@author: zhuyf
"""

import pandas as pd

data = pd.read_csv("datasets/Covid Data.csv")
columns = data.columns.values #Attributes + "class"

for instance in range(len(data.axes[0])):
    value = data.at[instance,columns[4]]
    if value=="9999-99-99": 
        data.loc[instance, columns[4]] = "1"
    else: 
        data.loc[instance, columns[4]] = "0"

data.to_csv("Covid Data postprocessing.csv")
print("done")