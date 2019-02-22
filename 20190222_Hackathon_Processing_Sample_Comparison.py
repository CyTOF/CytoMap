from hal import HAL, plotting
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
import fcsparser
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

def main():
    cv = 0.85
    predict(cv)
    analyze(cv)
    #plot_mice_1()

def predict(cv):
    col_names=[line.split(',')[0] for line in open('/home/ubuntu/data/scRNAseq/mice/count.csv', 'r').readlines()][1:]
    model = HAL(warm_start=True, n_cluster_init=50, clf_type = 'rf')
    model.load()
    ypossible = model.possible_clusters(cv)
    X = np.genfromtxt('/home/ubuntu/data/scRNAseq/mice/count.csv', delimiter=',')
    X = X[1:, 1:].T
    ypred = model.predict(X, cv)
    col_names_all = list(col_names[:,1].flatten())
    df_median_expression=pd.DataFrame(np.array([np.median(X[ypred == yu],axis=0) for yu in ypossible]), index=list(ypossible),columns=col_names_all)
    df_frequency = pd.DataFrame([np.count_nonzero(ypred == yu)/len(ypred) for yu in ypossible], index=ypossible, columns=[f])
    df_frequency.to_csv('/home/ubuntu/data/scRNAseq/mice/Frequencies.csv')
    df_median_expression.to_csv('/home/ubuntu/data/scRNAseq/mice/Median_expression.csv')
    result[f] = [ypred, df_median_expression, df_frequency]
    pickle.dump(result, open('results.pkl','wb'))

if __name__ == "__main__":
    main()
