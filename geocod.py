import json, requests
url = 'https://geocoder.api.here.com/6.2/geocode.json'

def getlocation(city:str, country:str):
	#data_input = arg.split(",")	
	parameters= dict(
		app_id = 'E5z0Y0Vq8dgBDYeQWcWx',
		app_code = 'd8y3wjou3xRI-Lzy-4SBHQ',
		City = city,
		Country = country
	)

	resp = requests.get(url=url, params=parameters)

	data = json.loads(resp.text)
	try:
		latitude = data['Response']['View'][0]['Result'][2]['Location']['DisplayPosition']['Latitude']
		longitude = data['Response']['View'][0]['Result'][2]['Location']['DisplayPosition']['Longitude']
		return latitude, longitude
	except :
		latitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
		longitude = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
		return latitude, longitude


if __name__ == "__main__":
	city = input("Enter the city: ")
	country = input("Enter the country: ")
	getlocation(city,country)