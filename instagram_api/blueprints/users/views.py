from flask import Blueprint, jsonify, make_response, request, json
from models.user import User
from flask_jwt_extended import create_access_token

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()

    user_list = []

    for user in users:
        user_list.append({
            'id': user.id,
            'name': f'{user.first_name} {user.last_name}',
            'username': user.username,
            'email': user.email,
            'profileImage':  user.profile_picture_url
        })
    
    response = {'data': user_list}

    return make_response(jsonify(response), 200)


@users_api_blueprint.route('/', methods=['POST'])
def create():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    email = data['email']
    password = data['password']
    # first_name = request.values.get('first_name')
    # last_name = request.values.get('last_name')
    # email = request.values.get('email')
    # username = request.values.get('username')
    # password = request.values.get('password')

    user = User(first_name = first_name, last_name = last_name, email = email, username = username, password = password)

    if user.save():
        access_token = create_access_token(identity=user.id)
        response = {
            'auth_token': access_token,
            'message': 'New user created successfully',
            'status': 'success',
            'user': {
                'id': user.id,
                'profileImage':  user.profile_picture_url,
                'username': user.username
            }
        }
        return make_response(jsonify(response),200)
    else:
        response = {
            'message': [],
            'status': 'failed'
        }
        for error in user.errors:
            response['message'].append(error)
        return make_response(jsonify(response),400)


@users_api_blueprint.route('/<id>', methods=['GET'])
def show(id):
    user = User.get_by_id(id)

    user_info = {
        'id': user.id,
        'profile_image': user.profile_picture_url,
        'username': user.username
    }

    return make_response(jsonify(user_info), 200)


@users_api_blueprint.route('check_name')
def check_name():
    username = request.args.get('username')

    if not username:
        response = {
            "message": "Username not provided",
            "status": "failed"
        }
        return make_response(jsonify(response), 400)

    check_name = User.get_or_none(User.username == username)  
    if check_name:
        valid = {
            'exists': True,
            'valid': False,
        } 
    else:
        valid = {
            'exists': False,
            'valid': True,
        } 
    
    return make_response(jsonify(valid), 200)