
from app import (
    app, 
    Resource, 
    reqparse, 
    jwt_required, 
    create_access_token,
    get_jwt_identity)
from app.models.user import User


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str, required=False, help="username field cannot be left blank")
    parser.add_argument('email', type=str, required=True, help="email field cannot be left blank")
    parser.add_argument('password',type=str, required=True, help="password field cannot be left blank")
    
    @jwt_required()
    def get(self):
        data = [user.json() for user in User.query.all()]
        return {'users': data}
    
    def post(self):
        data = UserResource.parser.parse_args()
        
        if User.find_by_email(data['email']):
            return {'message': 'user already exists in our system'}, 400
        
        user = User(**data)
        
        try:
            user.gen_hash()
            user.save_user()
            return {'message': 'user has been created successfully.'}, 201
        except:
            return {'message': 'An error occurred creating the user.'}, 500
              
class UserDetailResource(Resource): 
    @jwt_required() 
    def get(self, id):
        user = User.find_by_user(id)
        if user:
            return {'users': user.json()}
        return {'message': 'user not found'}, 404
    
    @jwt_required()
    def delete(self, id):
        user = User.find_by_user(id)
        user_id = get_jwt_identity()
        
        if user.id == user_id:
            try:
                user.delete_user()
                return {'users': 'user successfully deleted'}, 200
            except:
                return {'message': 'An error occurred deleted the user.'},500
        return {'message': 'user not found'}, 404

class LoginResource(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="this field cannot be left blank")
    parser.add_argument('password',type=str, required=True, help="this field cannot be left blank")
    
    def post(self):
        data = UserResource.parser.parse_args()
        
        user = User.find_by_email(data['email'])
        
        if user and user.verify_password(data['password']) :
            token_acesso = create_access_token(
                identity=user.id)
            return {'access_token': token_acesso }, 200
        return {'message': 'your invalid credentials'}, 401