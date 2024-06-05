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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([{
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        } for message in all_messages])
        
    elif request.method == 'POST':
        try:
            body = request.get_json()["body"]
            username = request.get_json()["username"]
            new_message = Message(body = body, username = username)
            db.session.add(new_message)
            db.session.commit()
            return jsonify({
                'id': new_message.id,
                'body': new_message.body,
                'username': new_message.username
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = db.session.get(Message, id)
        message.body = request.get_json()["body"]
        db.session.commit()
        return make_response({
            'id': message.id,
            'body': message.body,
            }), 200
    elif request.method == 'DELETE':
        message = db.session.get(Message, id)
        print(message)
        db.session.delete(message)
        db.session.commit()
        return ('', 204)
            

if __name__ == '__main__':
    app.run(port=5555)
