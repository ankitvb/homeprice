import os
import logging
import csv
import os
import pandas as pd
import numpy as np
from time import time
from matplotlib import pyplot as plt

from sklearn import preprocessing
from sklearn import manifold, datasets
from sklearn.cluster import AgglomerativeClustering

# Visualize the clustering
def plot_clustering(X_red, X, labels, title=None):
	"""
	Create nice scatter plot with 2D embedding
	"""
	x_min, x_max = np.min(X_red, axis=0), np.max(X_red, axis=0)
    X_red = (X_red - x_min) / (x_max - x_min)
    
    plt.figure(figsize=(6, 4))
    for i in range(X_red.shape[0]):
        plt.text(X_red[i, 0], X_red[i, 1], 'o',
        color=plt.cm.spectral(labels[i] / 10.),
        fontdict={'weight': 'bold', 'size': 9})
        
        plt.xticks([])
        plt.yticks([])
        title = "Agglomerative clustering with Ward linkage"
        if title is not None:
            plt.title(title, size=17)
            plt.axis('off')
            plt.tight_layout()



if __name__ == '__main__':
    #preprocessor
    std_scale = preprocessing.StandardScaler(with_mean=True,with_std=True)
    
    #number of non one-hot encoded features, including ground truth
    num_feat = 4
    
    print("Importing data")
    traindf = pd.DataFrame.from_csv('data/part_test.csv')
    ncols = traindf.shape[1]
    tmpmat = traindf.as_matrix()
    
    tmpmat[:,:num_feat] = std_scale.fit_transform(tmpmat[:,:num_feat])
    X_train = tmpmat[:,1:]
    #y_train = np.reshape(tmpmat[:,0],(tmpmat[:,0].shape[0],1))
    print("Done.")

    # 2D embedding of the digits dataset
    print("Computing embedding")
    X_red = manifold.SpectralEmbedding(n_components=2).fit_transform(X_train)
    print("Done.")
    
    print("Applying clustering")
    linkage = 'ward'
    clustering = AgglomerativeClustering(n_clusters=7)
    t0 = time()
    clustering.fit(X_red)
    print("%s : %.2fs" % (linkage, time() - t0))
    
    plot_clustering(X_red, X_train, clustering.labels_, "%s linkage" % linkage)
   
    plt.show()
