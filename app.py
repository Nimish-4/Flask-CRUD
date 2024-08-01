from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import hashlib
from schema import UserSchema
from marshmallow import ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["40 per day", "3 per minute"])

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
users_collection = mongo.db.users


@app.route('/users', methods=['GET'])
def get_all_users():
    users = users_collection.find()
    result = []
    for user in users:
        user['_id'] = str(user['_id'])
        result.append(user)
    return jsonify(result)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = users_collection.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():

    try :
        data = UserSchema().load(request.get_json())

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
    duplicate_user = users_collection.find_one({'password': data['password']})

    if duplicate_user==None:
        result = users_collection.insert_one(data)
        return jsonify({'_id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error':'Password already in use!'}), 400


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):

    try:
        data = UserSchema.load(request.get_json(), partial=True)  # allow updates for only 1 or 2 fields
        if 'password' in data:
            data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()  # ecryption

        updated_user = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})

        if updated_user.matched_count:
            return jsonify({'message': 'User updated'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except ValidationError as err:
        return jsonify(err.messages), 400
    

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = users_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


