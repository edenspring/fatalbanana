from flask import Blueprint, jsonify, session, request
from app.models import User, db, ServerMember, Friendship
from app.forms import LoginForm
from app.forms import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.aws_s3_upload import (upload_file_to_s3, allowed_file, get_unique_filename)

auth_routes = Blueprint("auth", __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = {}
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages[field] = error
    return errorMessages


@auth_routes.route("/")
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {"errors": ["Unauthorized"]}


@auth_routes.route("/login", methods=["POST"])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        print("HIT VALIDATE ON SUBMIT ON LOGIN")
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data["email"]).first()
        login_user(user)
        return user.to_dict()
    return {"errors": validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route("/logout")
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {"message": "User logged out"}


@auth_routes.route("/signup", methods=["POST"])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    res = request.files

    print("RES >>>>>>>>>>", request.form)
    print("RES >>>>>>>>>>", form)
    print("RES >>>>>>>>>>", form.data)

    if form.validate_on_submit():
                user = User(
                    username=form.data["username"],
                    email=form.data["email"],
                    password=form.data["password"],
                    display_pic=form.data["display_pic"]
                    # display_pic="https://cdn.discordapp.com/attachments/1030261089168015532/1073712325409902632/datcord_logo_png.png"
                )
                db.session.add(user)
                db.session.commit()
                member = ServerMember(
                    user_id=user.id,
                    server_id=9,
                    nickname=user.username,
                    role="member",
                )
                db.session.add(member)
                db.session.commit()
                friend_keanu = Friendship (
                user_id = user.id,
                friend_id = 17,
                role = "friend"
                )
                db.session.add(friend_keanu)
                db.session.commit()

                login_user(user)
                return user.to_dict()
    return {"errors": validation_errors_to_error_messages(form.errors)}, 401
    


#  AWS

    # if request.files.get("image") == None:
    #     print("HIT NONE")
    #     if form.validate_on_submit():
    #             user = User(
    #                 username=form.data["username"],
    #                 email=form.data["email"],
    #                 password=form.data["password"],
    #                 display_pic=form.data["display_pic"]
    #                 # display_pic="https://cdn.discordapp.com/attachments/1030261089168015532/1073712325409902632/datcord_logo_png.png"
    #             )
    #             db.session.add(user)
    #             db.session.commit()
    #             member = ServerMember(
    #                 user_id=user.id,
    #                 server_id=9,
    #                 nickname=user.username,
    #                 role="member",
    #             )
    #             db.session.add(member)
    #             db.session.commit()
    #             friend_keanu = Friendship (
    #             user_id = user.id,
    #             friend_id = 17,
    #             role = "friend"
    #             )
    #             db.session.add(friend_keanu)
    #             db.session.commit()

    #             login_user(user)
    #             return user.to_dict()
    # else:
    #     image = request.files["image"]
    #     print("image>>>>", image)

    #     if not allowed_file(image.filename):
    #         return {"errors": "file type not permitted"}, 400

    #     image.filename = get_unique_filename(image.filename)

    #     upload = upload_file_to_s3(image)

    #     print("upload>>>>", upload)

    #     if "url" not in upload:
    #         # if the dictionary doesn't have a url key
    #         # it means that there was an error when we tried to upload
    #         # so we send back that error message
    #         print("THIS 400")
    #         return upload, 400

    #     url = upload["url"]

    #     if form.validate_on_submit():
    #         user = User(
    #             username=form.data["username"],
    #             email=form.data["email"],
    #             password=form.data["password"],
    #             display_pic=url
    #         )
    #         db.session.add(user)
    #         db.session.commit()
    #         member = ServerMember(
    #             user_id=user.id,
    #             server_id=9,
    #             nickname=user.username,
    #             role="member",
    #         )
    #         db.session.add(member)
    #         db.session.commit()
    #         friend_keanu = Friendship (
    #         user_id = user.id,
    #         friend_id = 17,
    #         role = "friend"
    #         )
    #         db.session.add(friend_keanu)
    #         db.session.commit()

    #         login_user(user)
    #         return user.to_dict()
    # return {"errors": validation_errors_to_error_messages(form.errors)}, 401

@auth_routes.route("/update_image", methods=["PUT"])
def update_profile_image():
    pass

@auth_routes.route("/unauthorized")
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {"errors": ["Unauthorized"]}, 401
