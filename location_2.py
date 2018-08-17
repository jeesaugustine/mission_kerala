#|/usr/bin/python

import requests
from geopy.geocoders import Nominatim

def get_address(lat, lon):
	geolocator = Nominatim()
	loc = lat + "," + lon
	location = geolocator.reverse(loc)
	return(location.address)

def get_lat_long(Address_1, Address_2):
	Address_1 = Address_1.replace(" ","+")
	Address_2 = Address_2.replace(" ","+")
	search_address = Address_1+","+Address_2
	api_link = "https://maps.googleapis.com/maps/api/geocode/json?address="+search_address
	response = requests.get(api_link)
	resp_json_payload = response.json()
	return(resp_json_payload['results'][0]['geometry']['location'])