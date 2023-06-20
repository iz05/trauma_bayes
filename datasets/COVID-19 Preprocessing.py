# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:49:33 2023

@author: zhuyf
"""

import pandas as pd

data = pd.read_csv("Covid Data 2.csv")
columns = data.columns.values #Attributes + "class"

for instance in range(len(data.axes[0])):
    value = data.at[instance,columns[-1]]
    if value=="9999-99-99": 
        data.loc[instance, columns[-1]] = "N"
    else: 
        data.loc[instance, columns[-1]] = "Y"

data.to_csv("Covid Data 3.csv", index=False)
print("done")