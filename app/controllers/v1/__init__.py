from flask import Blueprint
v1_blueprint = Blueprint("v1", __name__, url_prefix='/api/v1')

from app.controllers.v1.actors import save_actor
from app.controllers.v1.actors import get_actor
from app.controllers.v1.actors import save_role
from app.controllers.v1.actors import get_role
from app.controllers.v1.performance import save_performance
from app.controllers.v1.performance import get_performance
from app.controllers.v1.performance import get_all_performances
from app.controllers.v1.performance import add_actor
from app.controllers.v1.contract import save_contracts
from app.controllers.v1.contract import get_contract
