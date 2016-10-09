from flask_restful import Api
from app import app as application
from app.db import db
from app.resources import UserCreateResource, UserLoginResource, UserProfileResource


def setup_app():
    db.init_app(application)
    api = Api(application)

    api.add_resource(UserCreateResource, '/user', methods=['POST'])
    api.add_resource(UserLoginResource, '/login', methods=['POST'])
    api.add_resource(UserProfileResource, "/profile", methods=['GET'])

    return application

app = setup_app()
