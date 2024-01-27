from flask import Flask
from database import engine
from api.api import Api
from router import router
from dotenv import load_dotenv
from sqlalchemy.orm import Session

app = Flask(__name__)

connect = engine.connect()

load_dotenv('/.env')
@app.before_request
def handle_before():
    return Api.handle_preflight()

router.create_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)