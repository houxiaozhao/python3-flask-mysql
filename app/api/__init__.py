from flask import Blueprint

from app import app

bp = Blueprint('api', __name__)
from app.api import user
from app.api import post
