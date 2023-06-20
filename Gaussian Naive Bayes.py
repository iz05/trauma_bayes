# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 09:50:09 2023

@author: zhuyf
"""

import pandas as pd
import math
from scipy.stats import ttest_ind_from_stats

train = pd.read_csv("Iris_train_quant.csv")
test = pd.read_csv("Iris_test_quant.csv")

columns = train.columns.values #Attributes + "class"
classes = train['class'].unique()
reverseclasses = {}
for a in range(len(classes)): 
    reverseclasses[classes[a]]=a
    
#Count how much of each class there is
classdensity = {}
total = 0 #total number of instances
for instance in range(len(train.axes[0])): 
    clas = train.at[instance,columns[-1]]
    if clas not in classdensity.keys(): 
        classdensity[clas]=0
    classdensity[clas]+=1
    total+=1

initials = [] #Initial guess
for a in classes: 
    initials.append(classdensity[a]/total)

#Find mean of each class
means = [] #class first, attribute second
#e.g. [[sepallength:3, petalwidth: 2], [sepallength:2,]]

for a in classes: 
    templist = []
    for attribute in range(len(columns)-1): 
        templist.append(train[train['class'] == a][columns[attribute]].mean())
    means.append(templist)
    
standarddev = []
for a in classes: 
    templist = []
    for attribute in range(len(columns)-1): 
        templist.append(train[train['class'] == a][columns[attribute]].std())
    standarddev.append(templist)

#Model is finished building
#Below is the testing
results = [[0 for x in range(len(classes))] for y in range(len(classes))]
for instance in range(len(test.axes[0])): 
    actual = test.at[instance,columns[-1]] #actual class
    probs = [math.log(initials[a]) for a in range(len(initials))]
    for attribute in range(len(columns)-1): 
        value = test.at[instance,columns[attribute]] #Value of attribute
        for clas in range(len(classes)): 
            zvalue = (value-means[clas][attribute])/standarddev[clas][attribute]
            pvalue = ttest_ind_from_stats(mean1=zvalue, std1=1, nobs1=1,
                     mean2=0, std2=1, nobs2=classdensity[classes[0]])
            probs[clas]+=math.log(pvalue[1])
    
    maxval = -99999
    predicted = 0 #Predicted class
    for a in range(len(classes)): 
        if probs[a]>maxval: 
            maxval = probs[a]
            predicted = a
    results[reverseclasses[actual]][predicted]+=1

print("Confusion Matrix") 
print("\t\t\t\t"+str(classes))
for a in range(len(results)): 
    print(classes[a]+"\t"+str(results[a]))

correct = 0
for a in range(len(results)): 
    correct+=results[a][a]
print("Accuracy: "+str(correct/len(test.axes[0])))
    