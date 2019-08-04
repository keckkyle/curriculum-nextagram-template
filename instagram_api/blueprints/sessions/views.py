from flask import Blueprint, jsonify, make_response, request
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash


sessions_api_blueprint = Blueprint('sessions_api',
                             __name__,
                             template_folder='templates')


@sessions_api_blueprint.route('/login', methods=['POST'])
def create():
    data = request.get_json()
    password = data['password']
    username = data['username']

    user = User.get_or_none(User.username == username)

    if not user:
        response = {
            "message": "Username does not exist"
        }
        return make_response(jsonify(response), 401)
    
    if not check_password_hash(user.password, password):
        response = {
            "message": "Incorrect password"
        }
        return make_response(jsonify(response), 401)

    access_token = create_access_token(identity=user.id)
    response = {
        'message': 'Successfully logged in',
        'auth_token': access_token,
        'user': {
                'id': user.id,
                'profileImage':  user.profile_picture_url,
                'username': user.username
            }
    }
    return make_response(jsonify(response), 200)