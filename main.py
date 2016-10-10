import requests
import json
import os
import uuid
from decimal import Decimal, getcontext
from os.path import join, dirname
from dotenv import load_dotenv
from db import insert_data

#load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def transform_data(data):
	transformed_data = []
	for row in data:
		formatted_row = {
			"Place_Name": row['properties']['name'],
			"ID": str(uuid.uuid4()),
			"details": {
				"lat": round(Decimal.from_float(row['geometry']['coordinates'][1]), 7),
				"lon": round(Decimal.from_float(row['geometry']['coordinates'][0]),7),
				"source": row['properties']['source']
			}
		}
		transformed_data.append(formatted_row)
	return transformed_data

def fetch_data(url_params):
	''' Fetch data from the given API and return it as json '''
	r = requests.get(url_params['url'], params=url_params['params'])
	return r.json()

def run():
	''' Entry point for the application '''
	place_table = 'Places'
	mapzen_search = {'url': "https://search.mapzen.com/v1/nearby",
					'params': {
						'layers': 'venue',
						'key': os.environ.get("MAPZEN_API_KEY"),
						'size': '30',
						'point.lon': '-122.44674682617188',
						'point.lat': '37.75280111220671',
						'boundary.circle.radius': '12',
						'sources': 'gn'}
					}
	mapzen_json = fetch_data(mapzen_search)
	mapzen_data_to_load = transform_data(mapzen_json['features'])
	insert_data(place_table, mapzen_data_to_load)


if __name__ == '__main__':
	run()