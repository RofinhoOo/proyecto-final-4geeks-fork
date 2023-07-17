from flask import Flask, request
import json
from models.users import User
from models.token_provisional import Provisional_token
from utils.db import db 
from utils.crypt import bcrypt
import datetime
from flask_jwt_extended import create_access_token
from services.send_mail import send_mail

def set_register(data):
    if data is None:
        return {'message': 'Missing data'}, 400
    data = json.loads(data)
    if data.get('username') and data.get('email') and data.get('password'):
        if User.query.filter_by(email=data['email']).first() or User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        else:
            user = User()
            user.username = data.get('username')
            user.email = data.get('email')
            password_hash = bcrypt.generate_password_hash(data.get('password'))
            user.password = password_hash
            user.active = False
            db.session.add(user)
            db.session.commit()
            
            token = Provisional_token()
            token.user_id = user.id
            hash_token = create_access_token(identity=user.id)
            token.token = hash_token
            token.expiration_date = datetime.datetime+datetime.timedelta('15 minutes')
            db.session.add(token)
            db.session.commit()
            
            send_mail('activacion', 'from_email@activacion', 'to_email@activacion', 'Por favor active su cuenta', 'activacion.html')
            
            return {'message': 'User created successfully'}, 201
        
        
        
def set_login(data):
    data = json.loads(data)
    find_user = User.query.filter_by(email=data.get('email')).first()
    if find_user:
        if bcrypt.check_password_hash(find_user.password, data.get('password')):
            access_token = create_access_token(identity=find_user.id)
            
            return {'message': 'Login successful', 'token': access_token}, 200
        else:
            return {'message': 'Invalid password'}, 400
    else:
        return {'message': 'User not found'}, 404
    
def set_active(token):
    find_token = Provisional_token.query.filter_by(token=token).first()
    if find_token:
        if find_token.expiration_date < datetime.datetime.now():
            return {'message': 'Token expired'}, 400
        user_id = find_token.user_id
        find_user = User.query.filter_by(id=user_id).first()
        if find_user:
            find_user.active = True
            db.session.commit()
            Provisional_token.query.filter_by(token=token).delete()
            db.session.commit()
            return {'message': 'User activated'}, 200