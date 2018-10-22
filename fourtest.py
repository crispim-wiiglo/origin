import json, requests

def getfood(food : str, coord : list):
	url = 'https://api.foursquare.com/v2/venues/explore'
	
	#coord = '22.912440,43.224322'

	params = dict(
	  client_id='UTR32LHD1YSUL4YI452QLQUZ1TP1VO4JTKFYKUOVD4QEQP5J',
	  client_secret='H4MP5KSOQTOTH1CYQTGI301SEEFPKK444PQGU1JAK5VUGVMS',
	  v='20180323',
	  ll=coord,
	  query = food,
	  radius = 2000,
	  limit=2
	)
	#print(params,'\n')

	resp = requests.get(url=url, params=params)
	data = json.loads(resp.text)
	try:

		text = data['response']['warning']['text']
		query = data['response']['query']
		name = data['response']['groups'][0]['items'][0]['venue']['name']
		location = data['response']['groups'][0]['items'][0]['venue']['location']
		street = location['address']
		distance = location['distance']

		print('\nFood: {}'.format(query))
		print('Street: {0}'.format(street))
		print('Name: {0}'.format(name))
	#	print('Distance: {0}'.format(distance))
	#	print('Warning: {0}'.format(text))


	except (KeyError, IndexError):
		try:
			name = data['response']['groups'][0]['items'][0]['venue']['name']
			location = data['response']['groups'][0]['items'][0]['venue']['location']
			street = location['address']
			print('Name: {0}'.format(name))
			print('Street: {0}'.format(street))
		except:
			print(data['response']['warning']['text'])

if __name__ == "__main__":
	food = input("Enter the food of the search: ")
	coord = input("Enter with the coordinates spaced by comma: ")
	getfood(food, coord)