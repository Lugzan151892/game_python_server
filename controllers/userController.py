from database import engine
from sqlalchemy import text
from flask import request
from api import Api
import bcrypt
import jwt
import json
import os

class Response:
    error = False


class User:
    connect = engine.connect()

    def registration(self):
        username = request.json['email']
        password = request.json['password']
        if not username or not password:
            return Api.Api('Bad password or email').bad_request()
        existed_user = self.connect.execute(text("SELECT * from users WHERE username = :val"), dict(val=username)).first()
        if existed_user:
            return Api.Api('Пользователь с такими данными уже существует').bad_request()
        hash_password = bcrypt.hashpw(str(password).encode(), bcrypt.gensalt())
        self.connect.execute(
            text(
                "INSERT INTO users (username, password, hunt_settings, spectated_users) VALUES"
                "(:username, :password, :hunt_settings, :spectated_users)"
            ),
            dict(username=username, password=hash_password, hunt_settings=json.dumps({}), spectated_users=json.dumps([]))
        )
        self.connect.commit()
        created_user = self.connect.execute(text("SELECT * from users WHERE username = :val"), dict(val=username)).all()
        print(created_user)
        print(dict(created_user[0]))
        token = jwt.encode(created_user, os.environ.get('SECRET_KEY'))
        response = { "user": created_user, "token": token }
        return Api.Api("User has been created", response).response()

user_module = User()