from database import engine
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from flask import request
from api.api import Api
import bcrypt
import jwt
import json
import os
from models.models import User as user_model

class User:
    connect = engine.connect()
    session = Session(engine)

    def registration(self):
        username = request.json['email']
        password = request.json['password']
        if not username or not password:
            return Api('Bad password or email').bad_request()
        existed_user_request = select(user_model).where(user_model.username.in_([f"{username}"]))
        existed_user = self.session.scalars(existed_user_request).one_or_none()
        if existed_user:
            return Api('Пользователь с такими данными уже существует').bad_request()
        hash_password = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
        new_user = user_model(username=username, password=hash_password, hunt_settings=bytes(json.dumps({}), 'utf8'), spectated_users=bytes(json.dumps([]), 'utf8'))
        self.session.add(new_user)
        self.session.commit()
        created_user = self.session.scalars(existed_user_request).one_or_none()
        print(created_user)
        # print(dict(created_user[0]))
        # token = jwt.encode(created_user, os.environ.get('SECRET_KEY'))
        # response = { "user": created_user, "token": token }
        return Api("User has been created", {"message": "Hellow world"}).response()

# class User:
#     connect = engine.connect()

#     def registration(self):
#         username = request.json['email']
#         password = request.json['password']
#         if not username or not password:
#             return Api('Bad password or email').bad_request()
#         existed_user = self.connect.execute(text("SELECT * from users WHERE username = :val"), dict(val=username)).first()
#         if existed_user:
#             return Api('Пользователь с такими данными уже существует').bad_request()
#         hash_password = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
#         self.connect.execute(
#             text(
#                 "INSERT INTO users (username, password, hunt_settings, spectated_users) VALUES"
#                 "(:username, :password, :hunt_settings, :spectated_users)"
#             ),
#             dict(username=username, password=hash_password, hunt_settings=json.dumps({}), spectated_users=json.dumps([]))
#         )
#         self.connect.commit()
#         created_user = self.connect.execute(text("SELECT * from users WHERE username = :val"), dict(val=username)).all()
#         print(created_user)
#         print(dict(created_user[0]))
#         token = jwt.encode(created_user, os.environ.get('SECRET_KEY'))
#         response = { "user": created_user, "token": token }
#         return Api("User has been created", response).response()