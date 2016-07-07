import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def read_save_recent_data():
	filename = "data/csv/pp-recent.csv" 
	datadf = pd.read_csv(filename)
	
	# Throw out extreme outliers
	datadf = datadf[datadf['Price']>10000.0]
	datadf = datadf[datadf['Price']<2000000.0]
	
	transDate = pd.to_datetime(datadf['Date'])
	datadf['TransDate'] = transDate
	
	# Delete unwanted columns
	#datadf[y].drop('TransactionId', axis=1, inplace=True)
	datadf.drop('PAON', axis=1, inplace=True)
	datadf.drop('SAON', axis=1, inplace=True)
	datadf.drop('Street', axis=1, inplace=True)
	datadf.drop('Locality', axis=1, inplace=True)
	datadf.drop('Town', axis=1, inplace=True)
	datadf.drop('District', axis=1, inplace=True)
	datadf.drop('County', axis=1, inplace=True)
	datadf.drop('TransCategory', axis=1, inplace=True)
	datadf.drop('RecStatus', axis=1, inplace=True)

	#print datadf_2015['Price'].describe()
	filename = "data/pkl/pp-recent.pkl"
	datadf.to_pickle(filename)


def get_lat_long(df, zips):
	#zips.set_index('postcode', inplace=True)
	return df.merge(zips,left_on='Zip',right_on='postcode',how='inner',sort=False)

if __name__ == '__main__':
	"""
	Main driver routine for generating the data sets for the training routines to consume.
	"""
	# Read saved data
	print "Reading saved data"
	#data = pd.read_pickle("data/pkl/pp-recent.pkl")
	data = pd.read_pickle("data/pkl/pp-recent.pkl")

	zips = pd.read_pickle("data/pkl/ukpostcodes.pkl")
	print "Done"
	
	print data.groupby(data['Zip']).count()
