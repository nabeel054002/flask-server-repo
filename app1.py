from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import bcrypt
from jwt.exceptions import ExpiredSignatureError, DecodeError
import time
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Team-8"
mongo = PyMongo(app)
CORS(app)

secret_key = 'yourSecretKey'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user_type = data.get('user_type')  # Added user_type field to identify candidate or company

    # Specify the collection based on the user_type
    collection = mongo.db.candidates if user_type == 'candidate' else mongo.db.companies

    user = collection.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User does not exist or wrong credentials!'}), 401

    # Check the hashed password
    stored_password = user.get('password', '')
    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        token = jwt.encode({'username': user['username'], 'exp': int(time.time()) + 3600}, secret_key, algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Wrong credentials!'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    # Specify the collection based on the user_type
    collection = mongo.db.candidates if user_type == 'candidate' else mongo.db.companies

    if collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists!'}), 409

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert the new user data into the respective collection
    user = {
        'username': username,
        'password': hashed_password,
    }
    collection.insert_one(user)

    token = jwt.encode({'username': username, 'exp': int(time.time()) + 3600}, secret_key, algorithm='HS256')
    return jsonify({'token': token}), 200

@app.route('/decode_jwt', methods=['POST'])
def decode_jwt():
    data = request.get_json()
    jwt_token = data.get('jwt_token')

    try:
        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        username = decoded_token.get('username', 'User not found in token')
        return jsonify({'username': username}), 200
    except ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except DecodeError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
