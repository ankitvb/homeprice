import os
import logging
import numpy as np

import theanets
from sklearn import preprocessing

def run_once(web_input=None):
    num_feat = 4
    
    npzfile = np.load('model/homeapp_preproc.npz')
    mean = npzfile['mean']
    std = npzfile['std']
    mean = np.reshape(mean, (1,mean.shape[0]))
    std = np.reshape(std, (1,std.shape[0]))
    
    # Reloading saved model
    model = theanets.Network.load("model/homeapp_model.pkl") 
    
    # Actual: 275,000 Predicted: 362,177 
    #web_input = np.array([51.2246169879,-1.48577399748,223.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0])
    # Actual 185,000 Predicted: 244,526
    #web_input = np.array([51.4395375168,-1.07174234072,5.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0])
    # Actual 231,500 Predicted 281,053
    #web_input = np.array([52.2010084131,-2.18181259148,218.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0])
    web_input = np.reshape(web_input, (1,web_input.shape[0]))
    
    web_input[:,:num_feat-1] -= mean[:,1:num_feat]
    web_input[:,:num_feat-1] /= std[:,1:num_feat]
    
    web_output = model.predict(web_input)
    
    #Rescale the output
    web_output *= std[:,0]
    web_output += mean[:,0]
    
    return int(web_output[0][0])
