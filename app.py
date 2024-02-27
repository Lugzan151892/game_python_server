from flask import Flask
from api.Api import Api
from router import router
from models.models import db, Users
from decouple import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config('DB_LINK')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def handle_before():
    return Api.handle_preflight()

router.create_routes(app)

if __name__ == '__main__':
    app.run()