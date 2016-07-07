import os
import urlparse
import psycopg2

def connect_db():
  urlparse.uses_netloc.append("postgres")
  url = urlparse.urlparse(os.environ["DATABASE_URL"])
  #Connect to the homeprice postgres database on Heroku
  conn = psycopg2.connect( \
       database=url.path[1:], \
       user=url.username, \
       password=url.password, \
       host=url.hostname, \
       port=url.port \
       )
  # Above sadly doesn't work on localhost, so need to use local copy
  # conn = psycopg2.connect(
  #   database="homeapp-db" \
  #   )

  # Get cursor
  cur = conn.cursor()

  return cur

def run_query(input_args):
  '''Takes in Zip code and home type
     Returns:
     1. Mean home price for a full zip (out+in) per year for past 5 years
     2. Mean home price for outer zip per year for past 5 years
     3. Mean home price over all years for each home time in the full zip
     4. Mean home price over all years for each home in out zip
     5. Top 5 comparables (most recent)
  '''

  # Connect to db
  cursor = connect_db()

  zip = input_args['zip'].upper() #Works
  type = input_args['type']
  outzip = zip.split(' ')[0]

  mean_year_out = {}
  mean_year_inout = {}
  mean_type_out = {}
  mean_type_inout = {}
  vol_year_inout = {}
  vol_year_out = {}

  # Get data for histogram
  histogram_data = {}
  for type_ in ['F','T','D','S']:
      cursor.execute("SELECT price \
                      FROM home_price \
                      WHERE zip LIKE \'"+outzip+"%\' \
                      AND type = \'"+type_+"\';" \
                     )

      type_data = []
      temp = cursor.fetchall()
      for item in temp:
          if int(item[0]) < 1500000:
              type_data.append(item[0])

      histogram_data[type_] = type_data

  #print histogram_data

  # Get data for comparables
  cursor.execute("SELECT price,date,zip,type,newbuild,estatetype,PAON,SAON,street,town \
                  FROM home_price \
                  WHERE zip LIKE \'"+outzip+"%\' \
                  ORDER BY DATE(Date) \
                  DESC \
                  LIMIT 25;")

  temp = cursor.fetchall()
  comparables = temp

  cursor.execute("SELECT AVG(price), EXTRACT(year FROM DATE(Date)) AS YR, COUNT(*) \
                  FROM home_price \
                  WHERE zip LIKE \'"+outzip+"%\' \
                  GROUP BY YR \
                  ORDER BY YR;" \
                  )

  temp = cursor.fetchall()
  for elem in temp:
      mean_year_out[int(elem[1])] = int(elem[0]) - int(elem[0])%100
      vol_year_out[int(elem[1])] = int(elem[2])

  #print mean_year_out

  cursor.execute("SELECT AVG(price), EXTRACT(year FROM DATE(Date)) AS YR, COUNT(*) \
                  FROM home_price \
                  WHERE zip=\'"+zip+"\' \
                  GROUP BY YR \
                  ORDER BY YR;" \
                  )

  temp = cursor.fetchall()
  for elem in temp:
      mean_year_inout[int(elem[1])] = int(elem[0]) - int(elem[0])%100
      vol_year_inout[int(elem[1])] = int(elem[2])

  #print mean_year_inout

  cursor.execute("SELECT AVG(price),type \
                  FROM home_price \
                  WHERE zip=\'"+zip+"\' \
                  GROUP BY type \
                  ORDER BY type;" \
                  )

  temp = cursor.fetchall() #works
  for elem in temp:
      mean_type_inout[elem[1]] = int(elem[0]) - int(elem[0])%100
  #print mean_type_inout

  cursor.execute("SELECT AVG(price),type \
                  FROM home_price \
                  WHERE zip LIKE \'"+outzip+"%\' \
                  GROUP BY type \
                  ORDER BY type;" \
                  )

  temp = cursor.fetchall() #works
  for elem in temp:
      mean_type_out[elem[1]] = int(elem[0]) - int(elem[0])%100

  #print mean_type_out

  result = (mean_year_inout,mean_year_out,
            mean_type_inout,mean_type_out,
            vol_year_inout,vol_year_out,
            comparables,
            histogram_data)

  return result

if __name__ == '__main__':
  # For unit testing with local db
  input_args = {
                'zip':'WC2N 5RJ',
                'type':'T',
                'newbuild':'N',
                'esttype':'F',
  }
  res = run_query(input_args)
