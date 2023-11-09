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

    user = mongo.db.users.find_one({'username': username})

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

    if mongo.db.users.find_one({'username': username}):
        return jsonify({'message': 'User already exists!'}), 409

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user data into the collection
    user = {
        'username': username,
        'password': hashed_password,
        'user_type': user_type,
    }
    mongo.db.users.insert_one(user)

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
    
@app.route('/get-skills', methods=['POST'])
def get_skills():
    data = request.get_json()
    username = data.get('username')

    user = mongo.db.users.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User not found!'}), 404
    print("user", user)
    skills = user.get('skills', [])
    return jsonify({'skills': skills}), 200

@app.route('/add-skills', methods=['POST'])
def add_skills():
    print('entered the add-skills route')
    data = request.get_json()
    username = data.get('username')
    new_skills = data.get('skills')
    print('92', username)
    user = mongo.db.users.find_one({'username': username})
    print("user", user)
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    print('97')
    # If 'skills' key does not exist, create it as a new list
    existing_skills = user.get('skills', [])
    
    # Add or modify skills for the user
    user['skills'] = new_skills
    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'skills': user['skills']}})
    print('104')
    return jsonify({'message': 'Skills added/modified successfully'}), 200

@app.route('/get_usertype', methods=['POST'])
def get_usertype():
    data = request.get_json()
    username = data.get('username')

    user = mongo.db.users.find_one({'username': username})

    if not user:
        return jsonify({'message': 'User not found!'}), 404
    
    usertype = user.get('user_type', None)
    return jsonify({'user_type': usertype}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
