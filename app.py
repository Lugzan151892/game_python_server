from flask import Flask
from api.api import Api
from router import router
from dotenv import load_dotenv
from models.models import db, Users

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://lugzan_hunt_py:lugzanHuntPy123456@lugzan.beget.tech/lugzan_hunt_py?charset=utf8mb4'
db.init_app(app)

with app.app_context():
    db.create_all()

load_dotenv('/.env')
@app.before_request
def handle_before():
    return Api.handle_preflight()

router.create_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)