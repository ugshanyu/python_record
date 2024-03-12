import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client[os.getenv('MONGO_DB', 'default_db_name')]
messages_collection = db['messages']  # Replace 'messages' with your collection name

@app.route('/save_message', methods=['POST'])
def save_message():
    data = request.json
    # Validate the incoming data
    if 'userId' not in data or 'id' not in data or 'message' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    # Save the message to MongoDB
    messages_collection.insert_one(data)
    return jsonify({'status': 'success'}), 201

@app.route('/update_rating/<message_id>', methods=['POST'])
def update_rating(message_id):
    data = request.json
    # Validate the incoming data
    if 'rating' not in data:
        return jsonify({'error': 'Missing required field: rating'}), 400
    # Update the message with the given rating
    result = messages_collection.update_one(
        {'id': message_id},
        {'$set': {'rating': data['rating']}}
    )
    if result.matched_count == 0:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
