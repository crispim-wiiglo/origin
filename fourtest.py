import json, requests

def getfood(food : str, coord : list):
	url = 'https://api.foursquare.com/v2/venues/search'
	
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

	if data['response']['venues']:
		#Grab the first restaurant
		restaurant = data['response']['venues'][0]
		venue_id = restaurant['id'] 
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		#Format the Restaurant Address into one string
		address = ""
		for i in restaurant_address:
		    address += i + " "
		restaurant_address = address

		#restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address}
		return restaurantInfo

	else:
		#print "No Restaurants Found for %s" % location
		return "No Restaurants Found"

################################################
if(3>5):
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
		#return query,name,street


	except (KeyError, IndexError):
		try:
			query = data['response']['query']
			name = data['response']['groups'][0]['items'][0]['venue']['name']
			location = data['response']['groups'][0]['items'][0]['venue']['location']
			street = location['address']
			print('Name: {0}'.format(name))
			print('Street: {0}'.format(street))

		#	return '{0}, {1}, {2}'.format(query,name,street)
		except:
			print(data['response']['warning']['text'])
		#	return data['response']['warning']['text']

if __name__ == "__main__":
	food = input("Enter the food of the search: ")
	coord = input("Enter with the coordinates spaced by comma: ")
	output_data = getfood(food, coord)
	print(output_data)