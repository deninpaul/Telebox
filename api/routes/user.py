from flask import Blueprint, request
from prisma.models import User

user_blueprint = Blueprint('user', __name__)