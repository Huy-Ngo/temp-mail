from asyncore import loop
from multiprocessing import Process

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources import TempMailServer, Mailbox, Auth, Mail

app = Flask(__name__)
app.config.from_json('config.json')

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

api.add_resource(Mailbox, '/mail/')
api.add_resource(Mail, '/mail/<int:_id>')
api.add_resource(Auth, '/auth/')


@app.before_first_request
def create_database():
    db.create_all()


def run_mail_server():
    server = TempMailServer(('127.0.0.1', 1025), None)
    print('This is running.')
    loop()


if __name__ == '__main__':
    app_proc = Process(target=app.run)
    mail_server_proc = Process(target=run_mail_server)

    app_proc.start()
    mail_server_proc.start()

    app_proc.join()
    mail_server_proc.join()
