from flask import Blueprint, jsonify, make_response, request
from models.image import Image
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from instagram_web.util.helpers import allowed_file, upload_file_to_s3

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

@images_api_blueprint.route('/', methods=['GET'])
def index():
    user = request.args.get('userId')

    if user:
        images = Image.select().where(Image.user_id == user)
    else:
        images = Image.select()

    image_list = []

    for image in images:
        image_list.append(
           image.image_url
        )
    
    return make_response(jsonify(image_list), 200)


@images_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    current_user = get_jwt_identity()

    if 'user_file' not in request.files:
        response = {
            "message": "No user_file key in request.files",
            "status": "failed"
        }
        return make_response(jsonify(response),400)

    
    file = request.files["user_file"]

    if file.filename == "":
        response = {
            "message": "Please select a file",
            "status": "failed"
        }
        return make_response(jsonify(response),400)

    if file and allowed_file(file.filename):
        image = Image(path=file.filename, user_id=current_user)
        image.save()
        upload_file_to_s3(file)
        response = {
            "image_url": image.image_url,
            "success": True
        }
        return make_response(jsonify(response),200)
    
    else: 
        response = {
            "message": "No image provided",
            "status": "failed"
        }
        return make_response(jsonify(response),400)


@images_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def show():
    current_user = get_jwt_identity()

    user = User.get_or_none(User.id == current_user)

    if not user:
        response = {
            "message": "Authentication failed",
            "status": "failed"
        }
        return make_response(jsonify(response), 401)
    
    user_images = Image.select().where(Image.user_id == current_user)

    image_list = []

    for image in user_images:
        image_list.append(
           image.image_url
        )

    return make_response(jsonify(image_list), 200)