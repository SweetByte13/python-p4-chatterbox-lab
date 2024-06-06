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
        # all_messages = Message.query.order_by(Message.created_at.asc()).all()
        # return jsonify([{
        #     'id': message.id,
        #     'body': message.body,
        #     'username': message.username,
        #     'created_at': message.created_at,
        #     'updated_at': message.updated_at
        # } for message in all_messages])
        messages = []
        for message in Message.query.order_by(Message.created_at).all():
            messages.append(message.to_dict())
        return make_response(messages)
    
    elif request.method == 'POST':
        # try:
        #     body = request.get_json()["body"]
        #     username = request.get_json()["username"]
        #     new_message = Message(body = body, username = username)
        #     db.session.add(new_message)
        #     db.session.commit()
        #     return jsonify({
        #         'id': new_message.id,
        #         'body': new_message.body,
        #         'username': new_message.username
        #     }), 201
            
        # except Exception as e:
        #     return jsonify({'error': str(e)}), 400
        params=request.json
        new_message = Message(body=params['body'], username=params['username'])
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)
        
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    
    if request.method == 'PATCH':
        if message:
            message.body = request.get_json()["body"]
            db.session.commit()
            return make_response({
                'id': message.id,
                'body': message.body,
                }), 200
        # message=Message.query.get(id)
        # if message:
        #   params=request.json
        #   message.body=params['body']
        #   db.session.commit()
        #   return make_response(message.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response('', 204)

        

if __name__ == '__main__':
    app.run(port=4000)
