from flask_restful import Api
from app import app as application
from app.db import db
from app.resources import UserCreateResource


def setup_app():
    db.init_app(application)
    api = Api(application)

    api.add_resource(UserCreateResource, '/user', methods=['POST'])

    return application

app = setup_app()
