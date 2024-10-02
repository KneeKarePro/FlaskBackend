from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import asyncio
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

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

@app.route('/data/range/<username>', methods=['GET'])
def get_data_range(username):
    """
    The purpose of this func is to get the data of a user within a certain range of time specified by the user. The user will specify the start and end time of the range and the function will return the data within that range.

    Args:
        username (_type_): The username of the user whose data is to be fetched.
    """
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not all([start_time, end_time]):
        return jsonify({'error': 'Missing start_time or end_time'}), 400
    
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    
    data = [{
        'angle': d.angle,
        'rotation': d.rotation,
        'timestamp': d.timestamp.isoformat()
    } for d in user.device_data if start_time <= d.timestamp <= end_time]
    
    return jsonify({'username': username, 'data': data}), 200

@app.route('/data/stats/<username>', methods=['GET'])
def get_data_stats(username):
    """
    Retrieve and return statistical data for a given user's device data.
    This function fetches the device data associated with the specified username
    from the database, computes statistical metrics (mean, standard deviation, 
    minimum, and maximum) for the 'angle' and 'rotation' fields, and returns 
    these statistics in a JSON response.
        username (str): The username of the user whose data statistics are to be fetched.
    Returns:
        Response: A JSON response containing the username and the computed statistics 
                  for 'angle' and 'rotation' fields if the user is found, otherwise 
                  an error message with a 404 status code.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = pd.DataFrame([{
        'angle': d.angle,
        'rotation': d.rotation,
        'timestamp': d.timestamp
    } for d in user.device_data])

    stats = {
        'angle': {
            'mean': data['angle'].mean(),
            'std': data['angle'].std(),
            'min': data['angle'].min(),
            'max': data['angle'].max()
        },
        'rotation': {
            'mean': data['rotation'].mean(),
            'std': data['rotation'].std(),
            'min': data['rotation'].min(),
            'max': data['rotation'].max()
        }
    }

    return jsonify({'username': username, 'stats': stats}), 200

@app.route('/data/<username>', methods=['DELETE'])
def delete_data(username):
    """
    **Deletes the data associated with the given username.**

    Args:
        username (_type_): The username of the user whose data is to be deleted.
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Data deleted'}), 200

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()