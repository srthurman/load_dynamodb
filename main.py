import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def fetch_data(url_params):
	''' Fetch data from the given API and return it as json '''
	r = requests.get(url_params['url'], params=url_params['params'])
	return r.json()

def run():
	''' Entry point for the application '''
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

if __name__ == '__main__':
	run()