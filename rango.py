from geo_four import findARestaurant
import json, requests

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_rest import Base, Rest

import codecs
import sys

engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 
#POST localhost:5000/restaurants?location=__&mealType=__
#stores restaurante in database
#GET localhost:5000/restaurants
#returns all restaurant, id, address, image
#GEt localhost:5000/restaurants/<int:id>
#returns restaurant,id,address,image from that rest
#UPDATE localhost:5000/restaurants/<int:id>/name & location & image
#DELETE localhost:5000/restaurants/<int:id>

@app.route("/")
@app.route("/restaurants", methods = ['GET','POST','DELETE'])
def restFunction():
	if request.method == 'GET':
		restaurants = session.query(Rest).all()
		return jsonify(restaurants = [i.serialize for i in restaurants])

	elif request.method == 'POST':
		food = request.args.get('food','')
		location = request.args.get('location', '')
		rest_info = findARestaurant(food, location)
		if rest_info != "No restaurants Found":
			restaurant = Rest(restaurant_name = str(rest_info['name']), restaurant_address = str(rest_info['address']), restaurant_image = rest_info['image'])
			session.add(restaurant)
			session.commit()
			return jsonify(restaurant = restaurant.serialize)
		else:
			return jsonify({"error":"No Restaurants Found for %s in %s" % (food, location)})
	
	elif request.method == 'DELETE':
		restaurants = session.query(Rest).all()
		for i in restaurants:
			session.delete(i)
		session.commit()
		return "Removed all the restaurants"


@app.route("/restaurants/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
def restFunctionId(id):
	restaurant = session.query(Rest).filter_by(id = id).one()
	if request.method == 'GET':
		return jsonify(restaurant = restaurant.serialize)

	elif request.method == 'PUT':

		address = request.args.get('address')
		image = request.args.get('image')
		name = request.args.get('name')
		if address:
			restaurant.restaurant_address = address
		if image:
			restaurant.restaurant_image = image
		if name:
			restaurant.restaurant_name = name
		session.commit()
		return jsonify(restaurant = restaurant.serialize)

	elif request.method == 'DELETE':
		session.delete(restaurant)
		session.commit()
		return "Restaurant Deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	
