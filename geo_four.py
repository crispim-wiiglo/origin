import json, requests

#############################
geo_id = 'E5z0Y0Vq8dgBDYeQWcWx'
geo_code = 'd8y3wjou3xRI-Lzy-4SBHQ'
four_id = 'UTR32LHD1YSUL4YI452QLQUZ1TP1VO4JTKFYKUOVD4QEQP5J'
four_secret = 'H4MP5KSOQTOTH1CYQTGI301SEEFPKK444PQGU1JAK5VUGVMS'

def getGeocodeLocation(inputString):
	#Replace Spaces with '+' in URL
	locationString = inputString.replace(" ", "+")
	# url = ('https://geocoder.api.here.com/6.2/geocode.json?app_id=%sapp_code=%ssearchtext=%s'% (geo_id, geo_code,locationString))
	# data = requests.get(url)
	url = 'https://geocoder.api.here.com/6.2/geocode.json'
	parameters= dict(
		app_id = geo_id,
		app_code = geo_code,
		searchtext = locationString
	)
	data = requests.get(url = url, params = parameters)
	result = json.loads(data.text)
	#print response
	try:
		latitude = result['Response']['View'][0]['Result'][2]['Location']['DisplayPosition']['Latitude']
		longitude = result['Response']['View'][0]['Result'][2]['Location']['DisplayPosition']['Longitude']
		return (latitude, longitude)
	except:
		latitude = result['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
		longitude = result['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
		return (latitude, longitude)

#This function takes in a string representation of a location and cuisine type, geocodes the location, and then pass in the latitude and longitude coordinates to the Foursquare API
def findARestaurant(food, location):
	latitude, longitude = getGeocodeLocation(location)
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (four_id, four_secret,latitude,longitude,food))
	parameters= dict(
		client_id = four_id,
		client_code = four_secret	,
		v = 20130815,
		ll = '{0},{1}'.format(latitude,longitude),
		query = food
	)
	data = requests.get(url = url, params = parameters)
	result = json.loads(data.text)
	if result['response']['venues']:
		#Grab the first restaurant
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id'] 
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		#Format the Restaurant Address into one string
		address = ""
		for i in restaurant_address:
			address += i + " "
			restaurant_address = address

		#Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,four_id,four_secret)))
		data = requests.get(url = url)
		result = json.loads(data.text)
		#Grab the first image
		#if no image available, insert default image url
		if result['response']['photos']['items']:
			firstpic = result['response']['photos']['items'][0]
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix + "300x300" + suffix
		else:
			imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
		#print "Restaurant Name: %s " % restaurantInfo['name']
		#print "Restaurant Address: %s " % restaurantInfo['address']
		#print "Image: %s \n " % restaurantInfo['image']
		return restaurantInfo
	else:
		#print "No Restaurants Found for %s" % location
			return "No Restaurants Found"


if __name__ == "__main__":
	food = input("Enter the food of the search: ")
	location = input("Enter the address: ")
	data_output = findARestaurant(food, location)
	print(data_output)