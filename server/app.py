from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    # Query all messages from the database
    messages = Message.query.all()
    
    # Convert messages to JSON format
    json_messages = [{'id': message.id, 'body': message.body, 'username': message.username,
                      'created_at': message.created_at, 'updated_at': message.updated_at}
                     for message in messages]
    
    # Return the JSON response
    return jsonify(json_messages)

@app.route('/messages', methods=['POST'])
def create_message():
    # Extract data from the request JSON
    data = request.json
    body = data.get('body')
    username = data.get('username')
    
    # Create a new message object
    new_message = Message(body=body, username=username)
    
    # Add the message to the database session and commit
    db.session.add(new_message)
    db.session.commit()
    
    # Return the newly created message as JSON
    return jsonify({
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at,
        'updated_at': new_message.updated_at
    }), 201  # HTTP status code for "Created"

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Find the message by id
    message = Message.query.get_or_404(id)
    
    # Extract the new body from the request JSON
    new_body = request.json.get('body')
    
    # Update the message body
    message.body = new_body
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return the updated message as JSON
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at,
        'updated_at': message.updated_at
    })

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    # Find the message by id
    message = Message.query.get_or_404(id)
    
    # Delete the message from the database
    db.session.delete(message)
    db.session.commit()
    
    # Return a success message
    return jsonify({'message': 'Message deleted successfully'}), 204  # HTTP status code for "No Content"

if __name__ == '__main__':
    app.run(port=5555)
