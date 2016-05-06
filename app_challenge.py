import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def read_save_data():
	data = {}
	
	for y in ['2015', '2016']:
		filename = "pp-"+y+".csv"	
		data[y] = pd.read_csv(filename)

		# Throw out extreme outliers
		data[y] = data[y][data[y]['Price']>10000.0]
		data[y] = data[y][data[y]['Price']<2000000.0]

		transDate = pd.to_datetime(data[y]['Date'])
		data[y]['TransDate'] = transDate	

	#print data_2015['Price'].describe()
		filename = "pp-"+y+".pkl"
		data[y].to_pickle(filename)


if __name__ == '__main__':
	#print 'Reading data'
	#read_save_data()
	#print 'Done'

	data = {}
	# Read saved data
	print "Reading saved data"
	data['2015'] = pd.read_pickle("pp-2015.pkl")
	data['2016'] = pd.read_pickle("pp-2016.pkl")

	#print data['Price'].describe()
	#print data['Price'].groupby(data['District']).describe()
	distData1 = {}
	distData2 = {}
	distData3 = {}

	distData1['2015'] = data['2015'][(data['2015'].Type == 'T') & (data['2015'].Town == 'OXFORD')]
	distData2['2015'] = data['2015'][(data['2015'].Type == 'D') & (data['2015'].NewBuild == 'N') & (data['2015'].Town == 'LONDON')]
	distData3['2015'] = data['2015'][(data['2015'].Type == 'S') & (data['2015'].NewBuild == 'Y') & (data['2015'].District == 'CORNWALL')]

	#print distData[['Price','District']]

	fig, axes = plt.subplots(2, 2, figsize=(12, 12))
	plt.subplots_adjust(wspace=0.5, hspace=0.5)
		    
	data['2015']['Price'].hist(bins=50,ax=axes[0,0], color='g', alpha=0.3, normed=True)
	data['2015']['Price'].plot(ax=axes[0,0], kind='kde', style='k--', linewidth=2, xlim=(0,2000000))
	axes[0,0].set_title('U.K. overall')
	axes[0,0].set_xlabel('Price in GBP')

	distData1['2015']['Price'].hist(ax=axes[0,1], color='g', alpha=0.3, normed=True)
	distData1['2015']['Price'].plot(ax=axes[0,1], kind='kde', style='k--', linewidth=2, xlim=(0,2000000))
	axes[0,1].set_title('Terrace style homes in Oxford')
	axes[0,1].set_xlabel('Price in GBP')

	distData2['2015']['Price'].hist(ax=axes[1,0], color='g', alpha=0.3, normed=True)
	distData2['2015']['Price'].plot(x='Price in GBP', ax=axes[1,0], kind='kde', style='k--', linewidth=2, xlim=(0,2000000))
	axes[1,0].set_title('Existing Detached homes in London')
	axes[1,0].set_xlabel('Price in GBP')

	distData3['2015']['Price'].hist(ax=axes[1,1], color='g', alpha=0.3, normed=True)
	distData3['2015']['Price'].plot(x='Price in GBP', ax=axes[1,1], kind='kde', style='k--', linewidth=2, xlim=(0,2000000))
	axes[1,1].set_title('New semi-detached homes in Cornwall')
	axes[1,1].set_xlabel('Price in GBP')

	plt.show()

	janData = {}
	for y in ['2015','2016']:
		janData[y] = data[y][data[y]['TransDate'].dt.month == 1]
				

	countyMedians = {}
	for y in ['2015','2016']:
		 countyMedians[y] = janData[y]['Price'].groupby(janData[y]['County']).median()

	yoyChange = {}
	for k in countyMedians['2015'].index:
		yoyChange[k] = float(countyMedians['2016'][k] - countyMedians['2015'][k])/float(countyMedians['2015'][k])  

	yoyValueList = []
	yoyCountyList = []

	for k in sorted(yoyChange, key=yoyChange.get, reverse=True):
		#print k, yoyChange[k]*100.0
		yoyCountyList.append(k)
		yoyValueList.append(yoyChange[k]*100.0)

	myCountyList = yoyCountyList[0:4] + yoyCountyList[len(yoyCountyList)-5:len(yoyCountyList)-1]
	myValueList  = yoyValueList[0:4] + yoyValueList[len(yoyValueList)-5:len(yoyValueList)-1]

	pos = np.arange(len(myValueList))
	plt.barh(pos,myValueList,0.5,color='g')
	ax = plt.gca()
	ax.get_yaxis().set_tick_params(direction='in')
	plt.yticks(pos, myCountyList)
	plt.xlabel('Percentage change')
	plt.title('Counties with the largest rises/drops in YoY median home prices in January from 2015 to 2016')
	plt.show()

