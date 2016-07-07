import os
import logging
import numpy as np
import pandas as pd

import theanets
from sklearn import preprocessing
import matplotlib.pyplot as plt

def run_once(web_input=None):
    """
    Run forward pass for a single input. Receives input vector from the web form.
    """
    num_feat = 4
    
    npzfile = np.load('model/homeapp_preproc.npz')
    mean = npzfile['mean']
    std = npzfile['std']
    mean = np.reshape(mean, (1,mean.shape[0]))
    std = np.reshape(std, (1,std.shape[0]))
   
    #test with 2016 data
    print "Reading test data"
    testdf = pd.DataFrame.from_csv('../data/csv/test.csv')
    print "Reading test data"
    ncols = testdf.shape[1]
    tmpmat = testdf.as_matrix()
    tmpmat[:,:num_feat] -= mean[:,:num_feat]
    tmpmat[:,:num_feat] /= std[:,:num_feat]
    X_test = tmpmat[:,1:]
    y_test = np.reshape(tmpmat[:,0],(tmpmat[:,0].shape[0],1))

    # Actual: 275,000 Predicted: 362,177 (Neon) 265,193 (theanets)
    # Actual: 231,500 Predicted: 281,053 (Neon) 214,855 (theanets)
    # Actual: 185,000 Predicted: 244,526 (Neon) 177,827 (theanets)    
    #web_input = np.array([[51.2246169879,-1.48577399748,223.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0],
    #                      [52.2010084131,-2.18181259148,218.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0],
    #                      [51.4395375168,-1.07174234072,5.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0]])
    # Actual: 182,500 Predicted: 247,500   (CART) 194,475 (theanets)
    # Actual: 320,000 Predicted: 225,000   (CART) 276,544 (theanets)
    # Actual: 410,000 Predicted: 544,000   (CART) 236,208 (theanets)
    # Actual: 745,000 Predicted: 1,325,000 (CART) 283,279 (theanets)
    web_input = np.array([[53.4744303498,-2.24354950012,225.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0],
                          [50.73853242,-1.803590697,119.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0],    
                          [51.4567582132,-0.195305164704,203.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,1.0,0.0],
                          [51.4466827727,-0.0572314416537,308.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0]])
    
    web_input[:,:num_feat-1] -= mean[:,1:num_feat]
    web_input[:,:num_feat-1] /= std[:,1:num_feat]
    
    # Reloading saved model
    model = theanets.Network.load("model/homeapp_model.pkl")

    #weights = model.find('hid1', 'w') 
    #print weights.get_value().T
    #visualize_wts(weights)

    #web_output = model.predict(web_input)
    web_output = model.predict(X_test)    

    #Rescale the output
    web_output *= std[:,0]
    web_output += mean[:,0]

    y_test *= std[:,0]
    y_test += mean[:,0]

    error = abs(web_output-y_test)/y_test

    print np.mean(error)
    print np.min(error)
    print np.max(error)
    #print web_output

    return web_output#[0][0]

def visualize_wts(weights):
    img = np.zeros((12, 12), dtype='f')
    img = weights.get_value().T

    plt.imshow(img, cmap=plt.cm.gray)
    plt.show()

    return

if __name__ == '__main__':
	price = run_once()
	#print price
