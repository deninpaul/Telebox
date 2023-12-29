import json
from flask import Blueprint, Response, request
from prisma.models import User

userBlueprint = Blueprint('user', __name__)

@userBlueprint.route('/', methods=['GET'])
def listUsers():
    if request.method == "GET":
        users = User.prisma().find_many(include={'files': True})
        return Response(
            json.dumps([user.dict() for user in users]),
            mimetype="application/json",
            status=200
        )

    else:
        return Response(
            json.dumps({"error": True, "reason": "Invalid method"}),
            mimetype="application/json",
            status=400
        )
