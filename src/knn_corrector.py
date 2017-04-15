import pandas as pd
import numpy as np
from math import isnan, sqrt
from sklearn.neighbors import NearestNeighbors

def correct_knn_sgpa(dep, sgpa_list):
    yr = 5 if dep == 'MA' else 4
    data = len(sgpa_list)
    predict_series = pd.Series(sgpa_list)
    #DATA CLEANING
    load = 'src/data/cleaned_data/'  + dep  + '_sgpa.csv'
    default = pd.read_csv(load, header = None)
    for row in default.iterrows():
        for j in range(2*yr):
            if isnan(row[1].iloc[j]):
                row[1].iloc[j] = 0
    default.index = list(range(len(default)))
    train_range = []
    for a in range(data):
        train_range.append(a)
    print(train_range)
    diff_list=[]
    for sem in range(data,2*yr):                #prediction sem
        for i in range(len(default)):   # find first data to use
            if(default.iloc[i,sem]!=0):
                first = i
                break
        no_neighbors = 30
        neigh = NearestNeighbors(n_neighbors=no_neighbors + 1)
        X = default.iloc[first:,train_range]
        X.index = list(range(len(X)))
        mynparray = X.values
        mynparray = np.vstack((mynparray,predict_series))
        X = pd.DataFrame(mynparray)
        neigh.fit(X)
        distance, indices = neigh.kneighbors(X)
        diff=0
        for neigh_no in range(no_neighbors):
            for i in range(data):
                if(indices[-1][neigh_no] != len(X)-1):
                    diff += sgpa_list[i] - default.iloc[first + indices[-1][neigh_no],i]
                else:
                    diff += sgpa_list[i] - default.iloc[first + indices[-1][no_neighbors],i]
        diff_list.append(diff)
    return (sum(diff_list)/((2*yr-data) * no_neighbors * data))

def correct_knn_subject(dep, gradelist):
    yr = 5 if dep == 'MA' else 4
    data = len(gradelist)
    input_list = []
    for sem in gradelist:
        for grade in sem:
            input_list.append(grade)
    predict_series = pd.Series(input_list)
    #DATA CLEANING
    load = 'src/data/cleaned_data/' + dep  + '_subject.csv'
    default = pd.read_csv(load, header = None)
    for row in default.iterrows():
        for j in range(2*yr):
            if isnan(row[1].iloc[j]):
                row[1].iloc[j] = 0
    default.index = list(range(len(default)))
    sem_len = []
    sgpa_col = []
    j = 0
    for i in range(len(default.columns)):
        if (default.iloc[0,i]==-1):
            sem_len.append(list(range(j,i-1)))
            sgpa_col.append(i-1)
            j=i+1
    train_range = []
    for a in range(data):
        for b in sem_len[a]:
                train_range.append(b)
    print(train_range)
    diff_list=[]
    for sem in range(data,2*yr):                #prediction sem
        for i in range(len(default)):   # find first data to use
            if(default.iloc[i,sem_len[sem][0]]!=0):
                first = i
                break
        no_neighbors = 30
        neigh = NearestNeighbors(n_neighbors = no_neighbors + 1)
        X = default.iloc[first:,train_range]
        X.index = list(range(len(X)))
        mynparray = X.values  
        mynparray = np.vstack((mynparray,predict_series))
        X = pd.DataFrame(mynparray)
        neigh.fit(X)
        distance, indices = neigh.kneighbors(X)
        diff=0
        for neigh_no in range(no_neighbors):
            for i in range(len(train_range)):
                if(indices[-1][neigh_no] != len(X)-1):
                    diff += input_list[i] - default.iloc[first + indices[-1][neigh_no],train_range[i]]
                else:
                    diff += input_list[i] - default.iloc[first + indices[-1][no_neighbors],train_range[i]]
        diff_list.append(diff)
    return (sum(diff_list)/((2*yr-data) * no_neighbors * len(train_range)))