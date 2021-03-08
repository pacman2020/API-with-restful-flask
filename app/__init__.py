from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource , Api, reqparse
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    jwt_required, 
    get_jwt_identity)

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
jwt = JWTManager(app)


db = SQLAlchemy(app)
Migrate(app, db)

#models
from app.models import user, suggestion

#controlles
from app.controllers.user import UserResource, UserDetailResource, LoginResource
from app.controllers.suggestion import SuggestionResource, SuggestionsDetailResource

api.add_resource(UserResource, '/user')
api.add_resource(UserDetailResource, '/user/<int:id>')
api.add_resource(LoginResource, '/login')
api.add_resource(SuggestionResource, '/')
api.add_resource(SuggestionsDetailResource, '/<int:id>')
