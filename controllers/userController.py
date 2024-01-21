from database import engine
from sqlalchemy import text
from flask import request
from api import Api
import bcrypt
import jwt

class Response:
    error = False


class User:
    connect = engine.connect()

    def registration(self):
        username = request.json['email']
        password = request.json['password']
        if not username or not password:
            return Api.Api('Bad password or email').bad_request()
        existed_user = self.connect.execute(text(f'SELECT * FROM users WHERE username = {username}')).first()
        if existed_user:
            return Api.Api('Пользователь с такими данными уже существует').bad_request()
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.connect.execute(
            text("INSERT INTO users (username, password, hunt_settings, spectated_users) VALUES (:username, :password, :hunt_settings, :spectated_users)"),
            [{"username": username, "password": hash_password, 'hunt_settings': {}, 'spectated_users': []}],
        )
        self.connect.commit()
        created_user = self.connect.execute(text(f'SELECT * FROM users WHERE username = {username}')).first()
        print(created_user)
        response = {"message": 'hello world'}
        return Api.Api(None, response).request()
        # if not req or not req.password:
        #     result = Api('Username and password are required')
        #     return result.bad_request()
        # existed_user = self.connect.execute(text('SELECT * FROM users WHERE username = req.username'))
        # return existed_user
        # result = self.connect.execute(text('INSERT INTO users(username, password)'))

user_module = User()