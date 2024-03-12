import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client[os.getenv('MONGO_DB', 'chat-history')]
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

@app.route('/get_all_messages', methods=['GET'])
def get_all_messages():
    try:
        # Fetch all messages from the database
        messages = list(messages_collection.find())
        for message in messages:
            message['_id'] = str(message['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify({'status': 'success', 'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("MongoDB connected successfully.")
    except Exception as e:
        print("MongoDB connection failed:", str(e))
    app.run(debug=True)
