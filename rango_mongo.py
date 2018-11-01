from flask import Flask, jsonify, request, url_for, abort, g
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient

auth = HTTPBasicAuth()

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection
app = Flask(__name__)


#ADD @auth.verify_password here
@auth.verify_password
def get_pw(username, password):
    print("Looking for user %s" % username)
    user = collection.find({'username' : username})
    if not collection.find({'username' : username}):
        print("User not found")
        return False
    elif not collection.find({'username' : username},{'password':password}):
        print("Unable to verify password")
        return False
    else:    
        g.username = username
        return True

#ADD a /users route here

@app.route('/users', methods = ['POST'])
def new_user():
    username = request.args.get('username','')
    password = request.args.get('password','')
    if username is None or password is None:
        print("missing arguments")
        abort(400)

    user = collection.find({'username' : username})
    if user is not None:
        print("existing user")
        return jsonify({'message': 'user already exists' }),200

    new = dict(
    	username = username,
    	password = hash_password(password)
    )

    collection.insert(new)
    return jsonify({ 'username': username }), 201

@app.route('/users/<username>')
def get_user(username):
    if not collection.find({'username':username}):
        abort(400)
    return jsonify({'username': username})

@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.username })

@app.route('/bagels', methods = ['GET','POST'])
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = serialize(collection.find())
        return jsonify({'bagels':bagels})

    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = dict(
        	name = name,
        	description = description,
        	picture = picture,
        	price = price
        )
        collection.insert(newBagel)

        return jsonify(newBagel)

def hash_password(self, password):
	self.password_hash = pwd_context.encrypt(password)

def verify_password(self,password):
	return pwd_context.verify(password, self.password_hash)

def serialize(data_input):
    data_out = []
    for doc in data_input:
        if 'username' and 'password' in doc:
            username = doc['username']
            password = doc['password']
        #    item = username, password
            data_out.append(username, password)
    return data_out

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)