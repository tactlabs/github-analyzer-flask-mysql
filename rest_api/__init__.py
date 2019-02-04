from flask import Blueprint
api = Blueprint('dummy_name', __name__)

from .index import *
from .template_controller import *
from .city_controller import *
