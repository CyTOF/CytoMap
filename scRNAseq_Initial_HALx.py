from hal import HAL, plotting
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

def main():
    X = np.genfromtxt('/home/ubuntu/data/scRNAseq/TabulaMuris/FACS/Marrow-counts.csv', delimiter=',')
    X = X[1:, 1:].T
    model = HAL(n_cluster_init=50, clf_type = 'rf')  
    model.fit(X)

if __name__ == "__main__":
    main()
