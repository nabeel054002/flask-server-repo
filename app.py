from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import json
from bson import ObjectId
from jwt.exceptions import ExpiredSignatureError, DecodeError
import time
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Team-8"
mongo = PyMongo(app)
CORS(app)

secret_key = 'yourSecretKey'

candidates = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

companies = [
    {'username': 'company1', 'password': 'pwd1'},
    {'username': 'company2', 'password': 'pwd2'}
]

# Custom JSONEncoder for handling ObjectId
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to its string representation
        return super().default(obj)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    candidate = next((c for c in candidates if c['username'] == username and c['password'] == password), None)
    company = next((c for c in companies if c['username'] == username and c['password'] == password), None)

    if not candidate and not company:
        return jsonify({'message': 'User Does not exist, wrong credentials!'}), 401

    user = candidate if candidate else company
    token = jwt.encode({'username': user['username'], 'exp': int(time.time()) + 3600}, secret_key, algorithm='HS256')

    return jsonify({'token': token}), 200


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user')

    if any(c['username'] == username for c in candidates) or any(c['username'] == username for c in companies):
        return jsonify({'message': 'User Already Exists!'}), 409

    if user_type == 'candidate':
        candidates.append({'username': username, 'password': password})
    elif user_type == 'employer':
        companies.append({'username': username, 'password': password})

    token = jwt.encode({'username': username, 'exp': int(time.time()) + 3600}, secret_key, algorithm='HS256')
    return jsonify({'token': token}), 200

@app.route('/msg', methods=['GET'])
def add_entry():
    new_entry = {
        "name": "Nabeel",
        "surname": "Khan"
    }
    
    # Specify the collection where you want to insert the document
    collection = mongo.db.your_collection_name
    
    # Insert the new document into the collection
    collection.insert_one(new_entry)
    
    return "Entry added to MongoDB"

@app.route('/get_entry', methods=['GET'])
def get_entry():
    entry = mongo.db.your_collection_name.find_one({"name": "Nabeel"})
    print("entry", entry, "stringify", json.dumps(entry, cls=CustomJSONEncoder))
    if entry:
        return jsonify(json.dumps(entry, cls=CustomJSONEncoder)), 200
    else:
        return jsonify({"message": "Entry not found"}), 404
    
@app.route('/update_entry', methods=['POST'])
def update_entry():
    # Define the filter to identify the document to update
    filter = {"name": "Nabeel"}
    
    # Define the update to set the new surname
    update = {"$set": {"mum surname": "Shaiakh"}}
    
    # Specify the collection where you want to update the document
    collection = mongo.db.your_collection_name
    
    # Use update_one to modify the document
    result = collection.update_one(filter, update)
    
    if result.modified_count == 1:
        return jsonify({"message": "Entry updated successfully"}), 200
    else:
        return jsonify({"message": "Entry not found or not updated"}), 404
    
@app.route('/add-applicant')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
