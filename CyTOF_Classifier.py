#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 09:33:01 2019

@author: anibaljt
"""

def classifier_expression(controlData,testData,decisions):
    
   
   from sklearn.svm import OneClassSVM
   
   #### defines classifier
   clf = OneClassSVM(kernel = 'linear')
   
   ### Fits on controlData
   clf.fit(controlData.values)
   
   ### Predicts on test data - should be all -1
   clf.predict(testData.values)

   ### How definite the deicison was; feature importance metric
   decisions = decisions + clf.decision_function(testData.values)
   
   
   return decisions
   

def testByGroup(data,groups):
    
    import pandas as pd 
    
    testDone = []
    var_dict = {}

    ### Splits data for comparison by SVM
    for category in groups:
        if category not in testDone:
            group = pd.DataFrame()
            for ind in data.index:
                if ind == category:
                    group = group.append(data.iloc[ind])
            var_dict[ind] = group
    
    ### returns dictionary of data
    return var_dict



### Runs the control data on the OneClassSVM 
#### implements decision function by group
    
def expression_Test(var_dict,control,numClassifiers):
    
    import numpy as np 
    
    allDecisions = {}
    
    for group in var_dict:
        
      if group != control:
          
        decisions = np.zeroes(len(group))
        
        for num in range(len(numClassifiers)):
            
           decisions =classifier_expression(var_dict[control],var_dict[group],decisions)
           
        decisions = decisions/numClassifiers
        allDecisions[group] = decisions
        
    return allDecisions
        
        
   
     
def feature_eval(var_dict,allDecisions):
  
    import numpy as np
    
    decisionStats = {}
    
    for group in allDecisions.keys():
          decisionStats[np.mean(allDecisions[group])] = var_dict[group]
    
    return decisionStats
    


def agglomerate(stats):
    
    import numpy as np
    
    keyList = []
    
    for key in stats.keys():
            keyList.append(np.abs(int(key)))
            
    keyList = keyList.sort()
        
        ###Need to improve runtime here
        #### Feature importance generator based on SVM
        ### decision function
        
    for key in stats.keys():
        if np.abs(int(key)) < max(keyList)*0.5:
            stats.pop(key)
                
    
    return stats
                
        

def driver(data,control,groups):
    
    allDict = {}

    for col in data.columns:
        
        
        var_dict = testByGroup(data[col],groups)
        allDecisions = expression_Test(var_dict,control,1000)
        allDecisions = agglomerate(allDecisions)
        
        decisionStats = feature_eval(var_dict,allDecisions)
        print(decisionStats)
        
 
        for key in decisionStats.keys():
            allDict[col + "_" + key] = decisionStats[key]
            
    return allDict


def main(argv):
    
    import pickle 
    clusterMeans  = argv[0]

    
    groups = []
    
    for i in range(len(argv)):
        
        if i != 0 and i != 1:
            groups.append(argv[i])
            
    
    
    data = driver(clusterMeans,argv[1],groups)
    
    pickle.dump(data,open("CyTOF_PipelineResults","wb"))
    
    
            
    
    
    
        
        
    
    
    
    
    









