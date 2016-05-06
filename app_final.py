import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def read_save_data():
	data = {}
	
	for y in ['2015', '2016']:
		filename = "data/" + "pp-"+y+".csv"	
		data[y] = pd.read_csv(filename)

		# Throw out extreme outliers
		data[y] = data[y][data[y]['Price']>10000.0]
		data[y] = data[y][data[y]['Price']<2000000.0]

		transDate = pd.to_datetime(data[y]['Date'])
		data[y]['TransDate'] = transDate	

		# Delete unwanted columns
		#data[y].drop('TransactionId', axis=1, inplace=True)
		data[y].drop('PAON', axis=1, inplace=True)
		data[y].drop('SAON', axis=1, inplace=True)
		data[y].drop('Street', axis=1, inplace=True)
		data[y].drop('Locality', axis=1, inplace=True)
		data[y].drop('Town', axis=1, inplace=True)
		data[y].drop('District', axis=1, inplace=True)
		data[y].drop('County', axis=1, inplace=True)
		data[y].drop('TransCategory', axis=1, inplace=True)
		data[y].drop('RecStatus', axis=1, inplace=True)

		#print data_2015['Price'].describe()
		filename = "data/" + "pp-"+y+".pkl"
		data[y].to_pickle(filename)

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
		shuffledf[:train_stop].to_csv('data/train.csv',header=True)
	else:
		train_stop = 0
	#validation set
	if validation_fraction > 0.0:
		validation_stop = int(np.floor(validation_fraction*numrows))+train_stop
		shuffledf[train_stop:validation_stop].to_csv('data/validate.csv',header=True)
	else:
		validation_stop = train_stop
	#test set:
	if test_fraction > 0.0:
		shuffledf[validation_stop:].to_csv('data/test.csv',header=True)


if __name__ == '__main__':
	"""
	Main driver routine for generating the data sets for the training routines to consume.
	"""
	print 'Reading data'
	read_save_data()
	print 'Done'

	data = {}
	# Read saved data
	print "Reading saved data"
	data['2015'] = pd.read_pickle("data/pp-2015.pkl")
	data['2016'] = pd.read_pickle("data/pp-2016.pkl")

	zips = pd.read_pickle("data/ukpostcodes.pkl")
	print "Done"
	
	zipdf = zips.loc[zips['postcode'] == 'AB21 0TF']
	print zipdf.iloc[0]['latitude']
	print zipdf.iloc[0]['longitude']

	#print data['2015']['Zip'].value_counts()
	data_ll = get_lat_long(data['2015'], zips)
	data_ll.drop('id',axis=1,inplace=True)
	data_ll.drop('postcode',axis=1,inplace=True)
	data_ll.drop('Zip',axis=1,inplace=True)
	data_ll.drop('TransDate',axis=1,inplace=True)

	date_ = pd.to_datetime(data_ll['Date'])
	date_start = pd.to_datetime("2015-01-01 00:00")

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
	house_types = list(set(data_ll['Type']))
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

	traindf = hotdf[:600000]
	testdf  = hotdf[600000:]

	create_all_sets(traindf,0.8, 0.2, 0.0)


