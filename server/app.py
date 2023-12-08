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

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        response = make_response(messages,200)
    elif request.method == 'POST':
        post_content = request.get_json()
        new_message = Message(
            username = post_content['username'],
            body = post_content['body']
        )
        db.session.add(new_message)
        db.session.commit()
        response = make_response(new_message.to_dict(),201)
    return response

@app.route('/messages/<int:id>', methods = ['GET','PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'GET':
        response = make_response(message.to_dict(),200)
    elif request.method == 'PATCH':
        patch_content = request.get_json()
        for attr in patch_content:
            setattr(message, attr, patch_content[attr])
            db.session.add(message)
            db.session.commit()
            response = make_response(message.to_dict(),200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = make_response({
            "delete_successful":True,
            "message": "Message deleted."
        },200)
    return response

if __name__ == '__main__':
    app.run(port=5555)
