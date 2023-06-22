from flask_restful import Api
from flask import Blueprint

roles_bp=Blueprint('roles',__name__)
role_api=Api(roles_bp)

from . import views