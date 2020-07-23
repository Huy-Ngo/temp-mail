from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blueprints import bp
from resources import Mailbox, Auth, Mail

app = Flask(__name__)
app.config.from_json('config.json')

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

api.add_resource(Mailbox, '/api/mail/')
api.add_resource(Mail, '/api/mail/<int:_id>')
api.add_resource(Auth, '/api/auth/')

app.register_blueprint(bp)


@app.before_first_request
def create_database():
    """Create database on first request."""
    db.create_all()


if __name__ == '__main__':
    app.run()
