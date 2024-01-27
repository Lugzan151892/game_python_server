from sqlalchemy import select, update
from flask import request
from api.api import Api
import bcrypt
import jwt
import json
import os
from models.models import db, Users as user_model

class User():
    def registration(self):
        username = request.json['email']
        password = request.json['password']
        if not username or not password:
            return Api('Bad password or email').bad_request()
        existed_user_request = select(user_model).where(user_model.username.in_([f"{username}"]))
        existed_user = db.session.scalars(existed_user_request).one_or_none()
        if existed_user:
            return Api('Пользователь с такими данными уже существует').bad_request()
        hash_password = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
        new_user = user_model(username=username, password=hash_password, hunt_settings=bytes(json.dumps({}), 'utf8'), spectated_users=bytes(json.dumps([]), 'utf8'))
        db.session.add(new_user)
        db.session.commit()
        created_user = db.session.scalars(existed_user_request).one_or_none()
        if created_user:
            created_user = created_user.__dict__
        else:
            Api("Something went wrong").internal()

        response_user = {
            "username": created_user['username'],
            "id": created_user['id'],
            "spectated_users": json.loads(created_user['spectated_users']),
            "hunt_settings": json.loads(created_user['hunt_settings'])
        }
        token = jwt.encode(response_user, os.environ.get('SECRET_KEY'))
        response = { "user": response_user, "token": token }
        return Api("User has been created", response).response()
    
    def login(self):
        username = request.json['email']
        password = request.json['password']
        if not username or not password:
            return Api('Bad password or email').bad_request()
        existed_user_request = select(user_model).where(user_model.username.in_([f"{username}"]))
        existed_user = db.session.scalars(existed_user_request).one_or_none()
        if not existed_user:
            return Api(f'User with username {username} not found').bad_request()
        else:
            existed_user = existed_user.__dict__
        compare_passwords = bcrypt.checkpw(password.encode(), hashed_password=existed_user['password'].encode())
        if not compare_passwords:
            return Api(f'User with username {username} not found').bad_request()
        response_user = {
            "username": existed_user['username'],
            "id": existed_user['id'],
            "spectated_users": json.loads(existed_user['spectated_users']),
            "hunt_settings": json.loads(existed_user['hunt_settings'])
        }
        token = jwt.encode(response_user, os.environ.get('SECRET_KEY'))
        response = { "user": response_user, "token": token }
        return Api("Successfully login", response).response()
    
    def check(self):
        authtoken = request.headers.get('authorization', type=str)
        if not authtoken:
            return Api().system_error('Auth token not valid')
        authtoken = authtoken.split()[1]
        if authtoken == 'undefined':
            return Api().system_error('Auth token not valid')
        decoded = jwt.decode(authtoken, os.environ.get('SECRET_KEY'), algorithms='HS256')
        existed_user_request = select(user_model).where(user_model.username.in_([f"{decoded['username']}"]))
        existed_user = db.session.execute(existed_user_request).scalar_one_or_none()
        if not existed_user:
            return Api('User not found').bad_request()
        else:
            existed_user = existed_user.__dict__
        response_user = {
            "username": existed_user['username'],
            "id": existed_user['id'],
            "spectated_users": json.loads(existed_user['spectated_users']),
            "hunt_settings": json.loads(existed_user['hunt_settings'])
        }
        token = jwt.encode(response_user, os.environ.get('SECRET_KEY'))
        response = { "user": response_user, "token": token }
        return Api(data=response).response()
    
    def get_user(self):
        authtoken = request.headers.get('authorization', type=str)
        if not authtoken:
            return Api().system_error('Auth token not valid')
        authtoken = authtoken.split()[1]
        if authtoken == 'undefined':
            return Api().system_error('Auth token not valid')
        decoded = jwt.decode(authtoken, os.environ.get('SECRET_KEY'), algorithms='HS256')
        existed_user_request = select(user_model).where(user_model.username.in_([f"{decoded['username']}"]))
        existed_user = db.session.execute(existed_user_request).scalar_one_or_none()
        if not existed_user:
            return Api('Не авторизован').bad_request()
        else:
            existed_user = existed_user.__dict__
        response_user = {
            "username": existed_user['username'],
            "id": existed_user['id'],
            "spectated_users": json.loads(existed_user['spectated_users']),
            "hunt_settings": json.loads(existed_user['hunt_settings'])
        }
        response = { "user": response_user }
        return Api(data=response).response()
    
    def save_user(self):
        authtoken = request.headers.get('authorization', type=str).split()[1]
        if not authtoken:
            return Api('Не авторизован').bad_request()
        decoded = jwt.decode(authtoken, os.environ.get('SECRET_KEY'), algorithms='HS256')
        hunt_settings = request.json['hunt_settings']
        spectated_users = request.json['spectated_users']
        update_request = update(user_model).where(user_model.id == decoded['id']).values(
            hunt_settings=bytes(json.dumps(hunt_settings), 'utf8'),
            spectated_users=bytes(json.dumps(spectated_users), 'utf8')
        )
        updated_user = db.session.scalars(update_request)
        print(updated_user)
        
