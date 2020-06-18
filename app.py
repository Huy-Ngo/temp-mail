from asyncore import loop

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources import TempMailServer, Mailbox, Auth

app = Flask(__name__)
app.config.from_json('config.json')

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

api.add_resource(Mailbox, '/mail/')
api.add_resource(Auth, '/auth/')


@app.before_first_request
def create_database():
    db.create_all()


if __name__ == '__main__':
    app.run()
    server = TempMailServer(('127.0.0.1', 1025), None)
    loop()
