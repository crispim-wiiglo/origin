import json, requests
url = 'https://geocoder.api.here.com/6.2/geocode.json'

def getlocation(inputString):
	data_input = inputString.replace(" ", "+")	
	#data_input = inputString
	
	parameters= dict(
		app_id = 'E5z0Y0Vq8dgBDYeQWcWx',
		app_code = 'd8y3wjou3xRI-Lzy-4SBHQ',
		searchtext = data_input
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
	data_input = input("Enter the address: ")
	data_output = getlocation(data_input)
	print(data_output)