from hal import HAL, plotting
import pandas as pd
from sklearn.preprocessing import StandardScaler
import fcsparser
import numpy as np
import os
import matplotlib.pyplot as plt

def main():
    data =  load()
    #np.savetxt('columns.txt',data.columns.values,fmt='%s')
    col = np.loadtxt('columns.txt', delimiter='\t', dtype=str)
    
    data = data[col[:,0]]

    X = np.arcsinh(data)

    model = HAL( n_cluster_init=50)

    model.fit(X)

    #xtsne = model.load('tsne')

    #y = model.predict(X, cv=0.8)
    
    #model.plot_tree(feature_name=col)

    #plotting.cluster_w_label(xtsne, y,psize=1)

    #plt.scatter(xtsne[:,0], xtsne[:,1])
    #plt.show()

    
    #y = model.predict(new_data)

    #plotting.cluster_w_label(xtsne,

def load():

    directory = '/Users/mukherjeer2/Documents/Data/CyTOF/20190209_B6_IdU_Pilot/Live_Single_Cells/'
    file_name = directory+'c11_20190209_BoneMarrow_1-10_01_BM_1_Singlets.fcs'
    #file = '/Users/alexandreday/Dropbox/CytofImmgen/FCS/84hr_r2_m36.fcs'
    _, data = fcsparser.parse(file_name)
    return data




if __name__ == "__main__":
    main()
