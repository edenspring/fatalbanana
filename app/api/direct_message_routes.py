from flask import Blueprint, request
from sqlalchemy import or_, and_
from flask_login import current_user, login_required
from app.models import DirectMessage, db, User
from .channel_routes import channel_routes
from datetime import datetime
from app.aws_s3_upload import upload_file_to_s3, allowed_file, get_unique_filename


#  url_prefix="/api/dms
direct_message_routes = Blueprint("direct_messages", __name__)

# get all messages
@direct_message_routes.route("/<int:id>")
@login_required
def get_dms(id):
    messages = (
        DirectMessage.query.filter(
            or_(
                and_(
                    DirectMessage.sender_id == current_user.id,
                    DirectMessage.friend_id == id,
                ),
                and_(
                    DirectMessage.sender_id == id,
                    DirectMessage.friend_id == current_user.id,
                ),
            )
        )
        .order_by(DirectMessage.created_at.asc())
        .all()
    )
    return {"direct_message": [el.to_dict() for el in messages]}


@direct_message_routes.route("/images/<int:id>", methods=["POST"])
# @login_required
def create_message_image(id):
    res = request.files
    # images
    if "image" not in res:
        return {"errors": "image required"}, 400
    image = res["image"]
    if not allowed_file(image.filename):
        return {"errors": "file type not permitted"}, 400
    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_s3(image)

    if "url" not in upload:
        # if dict doesn't have url key = err when uploading > send back err msg
        return upload, 400
    url = upload["url"]
    data = DirectMessage(
        sender_id=current_user.id,
        message=url,
        friend_id=id,
    )
    db.session.add(data)
    db.session.commit()
    return data.to_dict()


# delete messages by channel id
@direct_message_routes.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_dms(id):
    data = DirectMessage.query.get(id)
    temp = data.to_dict()
    if data:
        db.session.delete(data)
        db.session.commit()
    return temp


# edit channel message
@direct_message_routes.route("/<int:id>", methods=["PUT"])
@login_required
def update_dms(id):
    res = request.get_json()
    data = DirectMessage.query.get(id)
    if data:
        data.message = res["message"]
        db.session.add(data)
        db.session.commit()
        return data.to_dict()
