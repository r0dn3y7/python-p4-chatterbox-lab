from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_msg = Message(body=data['body'], username=data['username'])
        db.session.add(new_msg)
        db.session.commit()
        return jsonify(new_msg.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    return jsonify(message.to_dict()), 200



@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5000, debug=True)