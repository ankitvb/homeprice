import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def read_save_data():
	datadf = {}
	
	for y in ['2016']:
		filename = "data/csv/" + "pp-"+y+".csv"	
		datadf[y] = pd.read_csv(filename)

		# Throw out extreme outliers
		datadf[y] = datadf[y][datadf[y]['Price']>10000.0]
		datadf[y] = datadf[y][datadf[y]['Price']<2000000.0]

		transDate = pd.to_datetime(datadf[y]['Date'])
		datadf[y]['TransDate'] = transDate	

		# Delete unwanted columns
		#datadf[y].drop('TransactionId', axis=1, inplace=True)
		datadf[y].drop('PAON', axis=1, inplace=True)
		datadf[y].drop('SAON', axis=1, inplace=True)
		datadf[y].drop('Street', axis=1, inplace=True)
		datadf[y].drop('Locality', axis=1, inplace=True)
		datadf[y].drop('Town', axis=1, inplace=True)
		datadf[y].drop('District', axis=1, inplace=True)
		datadf[y].drop('County', axis=1, inplace=True)
		datadf[y].drop('TransCategory', axis=1, inplace=True)
		datadf[y].drop('RecStatus', axis=1, inplace=True)

		#print datadf_2015['Price'].describe()
		filename = "data/pkl/" + "pp-"+y+".pkl"
		datadf[y].to_pickle(filename)

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


def create_all_sets(hotdf, train_fraction, validation_fraction, test_fraction):
	numrows = hotdf.shape[0]
	rows    = np.arange(numrows)
	    
	np.random.shuffle(rows)
	shuffledf = hotdf[hotdf.columns].iloc[rows].reset_index(drop=True)
	
	#training set
	if train_fraction > 0.0:
		train_stop = int(np.floor(train_fraction*numrows))
		shuffledf[:train_stop].to_csv('data/csv/train.csv',header=True)
	else:
		train_stop = 0
	#validation set
	if validation_fraction > 0.0:
		validation_stop = int(np.floor(validation_fraction*numrows))+train_stop
		shuffledf[train_stop:validation_stop].to_csv('data/csv/validate.csv',header=True)
	else:
		validation_stop = train_stop
	#test set:
	if test_fraction > 0.0:
		shuffledf[validation_stop:].to_csv('data/csv/test.csv',header=True)


if __name__ == '__main__':
	"""
	Main driver routine for generating the data sets for the training routines to consume.
	"""
	print 'Reading data'
	read_save_data()
	#read_save_recent_data()
	print 'Done'

	# Read saved data
	print "Reading saved data"
	#data = pd.read_pickle("data/pkl/pp-recent.pkl")
	data = pd.read_pickle("data/pkl/pp-2016.pkl")

	zips = pd.read_pickle("data/pkl/ukpostcodes.pkl")
	print "Done"
	
	# Testing postcode lookup
	#zipdf = zips.loc[zips['postcode'] == 'AB21 0TF']
	#print zipdf.iloc[0]['latitude']
	#print zipdf.iloc[0]['longitude']

	#print data['2015']['Zip'].value_counts()
	data_ll = get_lat_long(data, zips)
	data_ll.drop('id',axis=1,inplace=True)
	data_ll.drop('postcode',axis=1,inplace=True)
	data_ll.drop('Zip',axis=1,inplace=True)
	data_ll.drop('TransDate',axis=1,inplace=True)

	date_ = pd.to_datetime(data_ll['Date'])
	date_start = pd.to_datetime("2010-01-01 00:00")

	month_create = date_.dt.month
	year_create = date_.dt.year

	Day = (date_-date_start).astype('timedelta64[D]')
	
	#data_ll['Month'] = month_create
	#data_ll['Year'] = year_create
	data_ll['Day'] = Day

	data_ll.drop('Date',axis=1,inplace=True)

	#only take values where partition is specified
	data_ll.dropna(axis=0,how='any',inplace=True)
	data_ll.reset_index(drop=True,inplace=True)

	# One hot encoding for non-numeric types
    # Hard coding house types to make sure order is consistent between training and test
	house_types = ['S', 'F', 'T', 'O', 'D'] #list(set(data_ll['Type']))
	build_types = list(set(data_ll['NewBuild']))
	est_types = list(set(data_ll['EstateType']))

	print "The following features will be encoded"
	print house_types
	print build_types
	print est_types

	hotdf = data_ll.copy()

	hotdf['Type'] = data_ll.apply(lambda x: house_types.index(x['Type']),axis=1)
	hotdf['NewBuild'] = data_ll.apply(lambda x: build_types.index(x['NewBuild']),axis=1)
	hotdf['EstateType'] = data_ll.apply(lambda x: est_types.index(x['EstateType']),axis=1)

	print 'Encoding features in one hot form'
	#print hotdf
	onehotcols = ['Type', 'NewBuild', 'EstateType']
	for feature in onehotcols:
		# Get number of categories in each feature	
		num_cat = np.max(hotdf[feature])+1
		hotcols = [feature+str(c) for c in range(num_cat)]
		tmpcols = ['TransactionId']+hotcols
		tmpdf = pd.DataFrame(columns=tmpcols)
		tmpdf[['TransactionId']] = hotdf[['TransactionId']].copy()
		tmpdf[hotcols] = 0.
		hotdf=pd.merge(hotdf,tmpdf,how='inner',on='TransactionId').copy()
		#set the hotcols to the correct values
		for i in range(num_cat):
			hotdf.loc[hotdf[feature]==i,feature+str(i)] = 1.

	#Drop original columns
	hotdf.drop('TransactionId',axis=1,inplace=True)
	hotdf.drop('Type',axis=1,inplace=True)
	hotdf.drop('NewBuild',axis=1,inplace=True)
	hotdf.drop('EstateType',axis=1,inplace=True)

	#traindf = hotdf[:600000]
	#testdf  = hotdf[600000:]

	print "Creating training, validation and test sets"
	#create_all_sets9(hotdf,0.8, 0.2, 0.0)
	create_all_sets(hotdf,0.0,0.0,1.0)


