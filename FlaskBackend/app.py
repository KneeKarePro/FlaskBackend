from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knee_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    device_data = db.relationship('DeviceData', backref='user', lazy=True)

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angle = db.Column(db.Float, nullable=False)
    rotation = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    username = data.get('username')
    angle = data.get('angle')
    rotation = data.get('rotation')

    if not all([username, angle, rotation]):
        return jsonify({'error': 'Missing data'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    device_data = DeviceData(angle=angle, rotation=rotation, user=user)
    db.session.add(device_data)
    db.session.commit()

    return jsonify({'message': 'Data received'}), 201

@app.route('/data/<username>', methods=['GET'])
def get_data(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = [{
        'angle': d.angle,
        'rotation': d.rotation,
        'timestamp': d.timestamp.isoformat()
    } for d in user.device_data]

    return jsonify({'username': username, 'data': data}), 200

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()

