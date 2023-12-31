import json
from flask import Blueprint, Response, request
from prisma.models import User
from utils import logger
import prisma.errors as Error

userBlueprint = Blueprint('user', __name__)
error = ""

@userBlueprint.route('/', methods=['GET'])
def listUsers():
    users = User.prisma().find_many(include={'files': False})
    return Response(
        json.dumps([user.model_dump() for user in users]),
        mimetype="application/json",
        status=200
    )

@userBlueprint.route('/', methods=['POST'])
def createUser():
    id = request.form.get('id')
    userName = request.form.get('userName')
    fullName = request.form.get('fullName')

    try:
        user = User.prisma().create(data={
            "id": int(id),
            "userName": userName,
            "fullName": fullName
        })
        logger.info("Created user: ", user.userName)

        return Response(
            json.dumps(user.model_dump()),
            mimetype="application/json",
            status=200
        )
    except Exception as e:
        logger.error(e)
        return Response(str(e), mimetype="application/json", status=400)