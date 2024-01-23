from flask import Flask
from database import engine
from sqlalchemy import text
from controllers import userController
from api import Api
from router import router
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('/.env')
@app.before_request
def handle_before():
    return Api.Api.handle_preflight()

router.create_routes(app)

def load_users():
    with engine.connect() as conn:
        result = conn.execute(text('select * from users'))
        users = []
        for row in result:
            users.append(dict(row))

def test_user():
    # user = userController.User()
    req = dict(username="12312", password=21312313)
    print(req.get('username'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)