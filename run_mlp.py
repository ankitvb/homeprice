import os
import logging
import numpy as np

from neon import NervanaObject
from neon.callbacks.callbacks import Callbacks
from neon.models import Model
from neon.util.argparser import NeonArgparser
from neon.data.dataiterator import ArrayIterator
from sklearn import preprocessing

def run_once(web_input):
    """
    Run forward pass for a single input. Receives input vector from the web form.
    """

    parser = NeonArgparser(__doc__)
    
    args = parser.parse_args()
    
    num_feat = 4
    
    npzfile = np.load('./model/homeapp_preproc.npz')
    mean = npzfile['mean']
    std = npzfile['std']
    mean = np.reshape(mean, (1,mean.shape[0]))
    std = np.reshape(std, (1,std.shape[0]))
    
    # Reloading saved model
    mlp=Model("./model/homeapp_model.prm")
    
    # Horrible terrible hack that should never be needed :-(
    NervanaObject.be.bsz = 1
    
    # Actual: 275,000 Predicted: 362,177 
    #web_input = np.array([51.2246169879,-1.48577399748,223.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0])
    # Actual 185,000 Predicted: 244,526
    #web_input = np.array([51.4395375168,-1.07174234072,5.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0])
    # Actual 231,500 Predicted 281,053
    web_input = np.array([52.2010084131,-2.18181259148,218.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,1.0])
    web_input = np.reshape(web_input, (1,web_input.shape[0]))
    
    web_input[:,:num_feat-1] -= mean[:,1:num_feat]
    web_input[:,:num_feat-1] /= std[:,1:num_feat]
    
    web_test_set = ArrayIterator(X=web_input, make_onehot=False)
    
    web_output = mlp.get_outputs(web_test_set)
    
    #Rescale the output
    web_output *= std[:,0]
    web_output += mean[:,0]
    
    return web_output[0]
