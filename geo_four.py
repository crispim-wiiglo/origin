from fourtest import getfood
from geocod import getlocation
import json, requests

food = input("Enter the food of the search: ")
city = input("Enter the city: ")
country = input("Enter the country: ")

lat,lng = getlocation(city = city,country = country)
coord = '{0},{1}'.format(lat,lng)
getfood(food, coord)

