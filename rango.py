from fourtest import getfood
from geocod import getlocation
import json, requests

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_rest import Base, Rest


engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 
#
#
@app.route("/")
@app.route("/restaurants", methods = ['GET','POST'])
def restFunction():
	if request.method == 'GET':
		return getAllRest()
	elif request.method == 'POST':
		location = input("Enter the address: ")
		country = input("Enter the country: ")
		lat,lng = getlocation(data_input = location)
		coord = '{0},{1}'.format(lat,lng)
		food_location = getfood(food, coord)
		return makeANewRest(name, food_location)

#POST localhost:5000/restaurants?location=__&mealType=__
#stores restaurante in database
#GET localhost:5000/restaurants
#returns all restaurant, id, address, image
#GEt localhost:5000/restaurants/<int:id>
#returns restaurant,id,address,image from that rest
#UPDATE localhost:5000/restaurants/<int:id>/name & location & image
#DELETE localhost:5000/restaurants/<int:id>

def getAllRest():
	restaurants = session.query(Rest).all()
	return jsonify(Rest = [i.serialize for i in restaurants])

def getRest(id):
	restaurant = session.query(Rest).filter_by(id = id).one()
	return jsonify(restaurant = restaurant.serialize)

def makeANewRest(name,description):
	restaurant = Rest(name = name, description = description)
	session.add(restaurant)
	session.commit()
	return jsonify(Rest = restaurant.serialize)

def updateRest(id,name,description):
	restaurant = session.query(Rest).filter_by(id = id).one()
	if not name:
		restaurant.name = name
	if not description:
		restaurant.description = description
	session.add(restaurant)
	session.commit()
	return "Updated a restaurant with id %S" % id

def deleteRest(id):
	restaurant = session.query(Rest)filter_by(id = id).one()
	session.delete(restaurant)
	session.commit()
	return "Removed restaurant with id %s" % id

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	