import peewee
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user
from models.user import User
from models.image import Image
from models.donation import Donation
from models.fan_idol import FanIdol
from instagram_web.util.helpers import allowed_file, upload_file_to_s3


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html', user=current_user)


@images_blueprint.route('/', methods=['POST'])
def create():
    if 'user_file' not in request.files:
        return "No user_file key in request.files"
    
    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        image = Image(path=file.filename, user_id=current_user.id)
        image.save()
        upload_file_to_s3(file)
        return redirect(url_for('users.show', username = current_user.username))
    
    else: 
        return redirect(url_for('image.new', id=id))


@images_blueprint.route('/<id>', methods=["GET"])
def show(id):
    image = Image.get_by_id(id)
    users = User.select()
    return render_template('images/show.html', image=image, users=users)


@images_blueprint.route('/', methods=["GET"])
def index():

#    images = Image.select().join(FanIdol, on=(Image.user_id == FanIdol.idol_id)).where(
#         (Image.user_id == current_user.id) |
#         ((FanIdol.fan_id == current_user.id) & (FanIdol.approved == True))
#     ).group_by(Image.id).order_by(Image.created_at.desc())

    followers = User.select().join(FanIdol, on=(FanIdol.idol_id == User.id)).where((FanIdol.fan_id == current_user.id) & (FanIdol.approved == True))

    images = Image.select().where((Image.user.in_(followers)) | (Image.user_id == current_user.id)).order_by(Image.created_at.desc())

    users = User.select()
    return render_template('images/index.html', images=images, users=users)


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('delete/<id>', methods=['POST'])
def delete(id):
    image = Image.get_by_id(id)
    image.delete_instance()
    return redirect(url_for('users.show', username=current_user.username))



