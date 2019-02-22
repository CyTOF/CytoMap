from hal import HAL, plotting
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import fcsparser
import numpy as np
import os
import pickle
from matplotlib import pyplot as plt

col_names=np.loadtxt('columns.txt', delimiter='\t',dtype=str)
#data = data[col[:,0]]
#data = data.rename(columns=dict(zip(col[:,0],col[:,1])))

def main():
    cv = 0.85
    predict(cv)
    analyze(cv)
    plot_mice_1()

def predict(cv):
    
    file_name_list = []

    for filename in os.listdir('/Users/mukherjeer2/Documents/Data/CyTOF/20190209_B6_IdU_Pilot/Live_Single_Cells/'):
        if filename.endswith(".fcs"):
            file_name_list.append(filename)
            continue
        else:
            continue
    
    col = np.loadtxt('columns.txt', delimiter='\t', dtype=str)
    result={}

    model = HAL(warm_start=True, n_cluster_init=50)
    

    model.load()

    ypossible = model.possible_clusters(cv)

    for f in file_name_list:
        print(f)
        data = load(f)

        data = data[col[:,0]]

        X = np.arcsinh(data)

        ypred = model.predict(X, cv)

        #Xtmp = model.preprocess(X)

        col_names_all = list(col_names[:,1].flatten())
        
        df_median_expression=pd.DataFrame(np.array([np.median(X[ypred == yu],axis=0) for yu in ypossible]), index=list(ypossible),columns=col_names_all)
       
        df_frequency = pd.DataFrame([np.count_nonzero(ypred == yu)/len(ypred) for yu in ypossible], index=ypossible, columns=[f])
        
        df_frequency.to_csv('/Users/mukherjeer2/Documents/Data/CyTOF/20190209_B6_IdU_Pilot/Live_Single_Cells/Frequencies.csv')
        
        df_median_expression.to_csv('/Users/mukherjeer2/Documents/Data/CyTOF/20190209_B6_IdU_Pilot/Live_Single_Cells/Median_expression.csv')

        #print(df_median_expression)
        #print(df_frequency)
        #exit()
        result[f] = [ypred, df_median_expression, df_frequency]

    pickle.dump(result, open('results.pkl','wb'))

def find_second_last(text, pattern):
    return text.rfind(pattern, 0, text.rfind(pattern))

def analyze(cv):

    results = pickle.load(open('results.pkl','rb'))
    model = HAL(warm_start=True, n_cluster_init=50)
    model.load()
    #exit()
    ypossible = model.possible_clusters(cv=cv)

    data = []
    idx = []
    #df = pd.DataFrame([], columns=[str(yu) for yu in ypossible])

    for k, v in results.items():
        _, _, df_freq = v
        data.append(df_freq.values.flatten())
        idx.append(k[:k.find('Singlets.fcs')-1][find_second_last(k[:k.find('Singlets.fcs')-1],'_')+1:])

    df=pd.DataFrame(np.array(data), index=idx, columns=results['c11_20190209_BoneMarrow_1-10_01_BM_1_Singlets.fcs'][2].index)
    
    ax = sns.clustermap(np.arcsinh(df*1000).T, xticklabels=df.index,cbar_kws={'label':'arcsinh(frequency*1000)'}, figsize = (15, 15))
    plt.setp(ax.ax_heatmap.xaxis.get_majorticklabels(), rotation=90,ha='right')
    plt.setp(ax.ax_heatmap.yaxis.get_majorticklabels(), rotation=00,ha='left')


    plt.show()

    pickle.dump(df,open('frequencies.pkl','wb'))

def plot_mice_1():

    results = pickle.load(open('results.pkl','rb'))
    ypred, df_median_expression, df_frequency= results['c11_20190209_BoneMarrow_1-10_01_BM_1_Singlets.fcs']
    

    

    """  model = HAL(warm_start=True, n_cluster_init=50)
    model.load()
    #exit()
    ypossible = model.possible_clusters(cv=cv)

    data = []
    idx = []
    #df = pd.DataFrame([], columns=[str(yu) for yu in ypossible])

    for k, v in results.items():
        _, _, df_freq = v
        data.append(df_freq.values.flatten())
        idx.append(k.split('_')[1])

    df=pd.DataFrame(data, index=idx, columns=ypossible) """
    
    ax = sns.clustermap(df_median_expression,  xticklabels=1, figsize = (15, 15))

    plt.setp(ax.ax_heatmap.xaxis.get_majorticklabels(), rotation=90, ha='right')

    plt.setp(ax.ax_heatmap.yaxis.get_majorticklabels(), rotation=00, ha='left')
    plt.show()

    model = HAL(warm_start=True, n_cluster_init=50)

    xtsne = model.load('tsne')
    
    model.cluster_w_label(xtsne, ypred, psize=1)

    #emphasis_plot(xtsne, ypred, 36)
    
    #plotting.plotly_plot(xtsne, ypred)

    exit()
    #plotting.cluster_w_label(xtsne, ypred, psize=1)

def emphasis_plot(x, y, yemph):
    pos_emph = (y==yemph)
    (pos_emph == False)
    plt.scatter(x[(pos_emph == False),0], x[(pos_emph == False),1], c='blue', s=1)
    plt.scatter(x[pos_emph,0], x[pos_emph,1], c='red', s=3)
    plt.show()

def load(file_name):

    directory = '/Users/mukherjeer2/Documents/Data/CyTOF/20190209_B6_IdU_Pilot/Live_Single_Cells/'

    _, data = fcsparser.parse(directory+file_name)
    return data

def plot_histogram_expression(cluster_idx=0, column_file='columns_all.txt'):
    
    from colour import Color
    col = np.loadtxt(column_file, dtype=str)[:,0]
    marker = np.loadtxt(column_file, dtype=str)[:,1]
    results = pickle.load(open('results.pkl','rb'))
    fig, ax = plt.subplots(nrows=6, ncols=6, figsize=(12,8))
    palette = ["#30a2da","#fc4f30",Color('orange').get_rgb(),Color('lightgreen').get_rgb(),"magenta","cyan", "#886F4C","#34362D", "#B4A8BD", "#00A6AA", "#452C2C","#636375", "#A3C8C9", "#FF913F"]
    #palette = ["#30a2da","#fc4f30","#e5ae38","#6d904f","#8b8b8b","#006FA6", "#A30059","#af8dc3","#922329","#1E6E00"]
    
    #print(results)
    idx_file = 0
    for k, v in results.items():
        print(k)
        sample_name = k.split('_')[1]
        data = np.arcsinh(load(k))
        ypred, df_median_expression, df_frequency, _ = v
        for i, c in enumerate(col):
            #print(c)
            x = data[c].iloc[ypred == cluster_idx]
            i1, i2 = np.unravel_index(i, (6,6))
            #print(i1, i2)
            y,x = np.histogram(x, bins=50)#, log=True)
            #ysmooth = savitzky_golay(y, 9, 1)
            x=0.5*(x[:-1]+x[1:])
            ax[i1, i2].plot(x, y, c=palette[idx_file])
            ax[i1, i2].set_yscale('log')
            ax[i1, i2].set_title(marker[i],fontsize=8)
            ax[i1,i2].tick_params(axis='both', which='major', labelsize=7)
        #ax[i1, i2].set_xticks(fontsize=8)
        #ax[i1, i2].set_yticks(fontsize=8)
        #plt.hist(
        #plt.plot(x, y)
        #plt.show()
        #print(x)
        
        ax[5,5].scatter([0], [0], label=sample_name, c=palette[idx_file])
        legend = ax[5,5].legend(loc='best', fontsize=8, ncol=2, framealpha=1.0, facecolor='white')
        #ax.set_xticks(fontsize=8)
        #plt.yticks(fontsize=4)
        idx_file += 1
        print(idx_file)
    #legend = plt.legend(frameon = 1)
    #frame = legend.get_frame()
    #frame.set_facecolor('green', alpha=1.0)
    #print(ret)
    #exit()
    #ax[i1, i2].hist(x, c=palette[idx_file])
    #idx_file+=1
    plt.tight_layout(h_pad=0., w_pad=0.)
    plt.show()


if __name__ == "__main__":
    main()
