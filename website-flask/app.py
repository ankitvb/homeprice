from flask import Flask, jsonify, render_template, request, redirect
from sklearn import preprocessing

import numpy as np
import pandas as pd
import theanets
import run_mlp
import database

# Preload zip code lookup
zips = pd.read_pickle("data/ukpostcodes.pkl")
zips.drop('id',axis=1,inplace=True)

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():

  return render_template('index.html')

@app.route('/get_estimate', methods=['GET','POST'])
def get_estimate():
  global zips

  house_types = ['S', 'F', 'T', 'O', 'D']
  build_types = ['Y', 'N']
  est_types = ['L', 'F']
  type_offset = 3
  build_offset = 8
  est_offset = 10

  try:
    if request.method == 'GET':
      if request.args is not None:
        home_args = dict(request.args.to_dict().items())

        # Run db query
        result_db = database.run_query(input_args=home_args)

        zipcode = home_args['zip']
        type_   = home_args['type']
        newbuild = home_args['newbuild']
        estatetype = home_args['esttype']

        day = 365.0*6.5
        #zips = pd.read_pickle("data/ukpostcodes.pkl")
        #zips.drop('id',axis=1,inplace=True)
        try:
            zipdf = zips.loc[zips['postcode'] == str(zipcode).upper()]
            lat = zipdf.iloc[0]['latitude']
            long_ = zipdf.iloc[0]['longitude']
        except (KeyError, IndexError):
            return jsonify(result=0);
        # One hot encoding for type newbuild and estatetype
        # List indices as follows
        inputs = np.zeros(12)
        inputs[0] = lat
        inputs[1] = long_
        inputs[2] = day
        type_idx = house_types.index(type_)
        build_idx = build_types.index(newbuild)
        est_idx = est_types.index(estatetype)

        inputs[type_offset+type_idx] = 1.0
        inputs[build_offset+build_idx] = 1.0
        inputs[est_offset+est_idx] = 1.0

        # Run ML part
        tmp_price = run_mlp.run_once(web_input=inputs)
      else:
        print "Args not found"
  except:
    pass


  # Pack up ML results
  result_ml = {}
  result_ml['latitude'] = lat
  result_ml['longitude'] = long_
  #tmp_price = run_mlp.run_once(web_input=inputs)
  result_ml['price'] = int(tmp_price) - int(tmp_price)%100

  # Pack up DB results
  # Get data from result tuple
  #myio, myo, mtio, mto, vyio, vyo = result_db[0], result_db[1], result_db[2], result_db[3], result_db[4], result_db[5]
  comps = result_db[6]
  comps_ll = []

  hist_data = result_db[7]

  try:
    for address in comps:
      zipdf = zips.loc[zips['postcode'] == str(address[2]).strip()]
      lat = zipdf.iloc[0]['latitude']
      long_ = zipdf.iloc[0]['longitude']
      tmplist = list(address)
      tmplist.append(lat)
      tmplist.append(long_)
      comps_ll.append(tuple(tmplist))
  except:
    pass

  result_full = (result_db[0], result_db[1], result_db[2], result_db[3], result_db[4], result_db[5], comps_ll, hist_data, result_ml)

  return jsonify(result=result_full)

if __name__ == '__main__':
  app.run(port=33507)
