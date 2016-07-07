#!/usr/bin/env python

import os
import logging
import csv
import os
import pandas as pd
import numpy as np

import theano
import theano.tensor as T

import theanets

from sklearn import preprocessing

logging.basicConfig(level=logging.INFO)

def train_mlp():
	"""
	Train data and save scaling and network weights and biases to file
	to be used by forward prop phase on test data
	"""
	#preprocessor
	std_scale = preprocessing.StandardScaler(with_mean=True,with_std=True)
	#std_scale = feature_scaler(type='Standardizer',with_mean=True,with_std=True)
	
	#number of non one-hot encoded features, including ground truth
	num_feat = 4
	
	# split into train and tests sets
	#load data from csv-files and rescale
	#training
	traindf = pd.DataFrame.from_csv('../data/csv/train.csv')
	ncols = traindf.shape[1]
	
	#tmpmat=std_scale.fit_transform(traindf.as_matrix())
	#print std_scale.scale_
	#print std_scale.mean_
	
	tmpmat = traindf.as_matrix()
	#print tmpmat[:,1:num_feat]
	
	tmpmat[:,:num_feat] = std_scale.fit_transform(tmpmat[:,:num_feat])
	X_train = tmpmat[:,1:]
	y_train = np.reshape(tmpmat[:,0],(tmpmat[:,0].shape[0],1))
	
	train_set = tuple([X_train, y_train])

	#validation
	validdf = pd.DataFrame.from_csv('../data/csv/validate.csv')
	ncols = validdf.shape[1]
	tmpmat = validdf.as_matrix()
	tmpmat[:,:num_feat] = std_scale.transform(tmpmat[:,:num_feat])
	X_valid = tmpmat[:,1:]
	y_valid = np.reshape(tmpmat[:,0],(tmpmat[:,0].shape[0],1))
	
	valid_set = tuple([X_valid, y_valid])

	#test
	testdf = pd.DataFrame.from_csv('../data/csv/test.csv')
	ncols = testdf.shape[1]
	tmpmat = testdf.as_matrix()
	tmpmat[:,:num_feat] = std_scale.transform(tmpmat[:,:num_feat])
	X_test = tmpmat[:,1:]
	y_test = np.reshape(tmpmat[:,0],(tmpmat[:,0].shape[0],1))

	test_set = tuple([X_test, y_test])	

	model = theanets.Regressor([12, 24, 24, 1], loss='MeanAbsoluteError') 

	model.train(train_set,
				valid_set,
				hidden_dropout=0.5,
				algo='adam',
				learning_rate=1e-4,
				momentum=0.0,
				batch_size=1000                
				)

	# Saving the model
	print 'Saving model parameters!'
	model.save("model/homeapp_model.pkl")
	
	# Reloading saved model
	# save the preprocessor vectors:
	np.savez("model/homeapp_preproc.npz", mean=std_scale.mean_, std=std_scale.scale_)

	return

if __name__ == '__main__':
    train_mlp() 
