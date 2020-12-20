from flask import Blueprint
v1_blueprint = Blueprint("v1", __name__, url_prefix='/api/v1')

from app.controllers.v1.patient import save_patient
from app.controllers.v1.patient import get_patient