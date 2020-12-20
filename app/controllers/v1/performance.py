from flask import request, jsonify
from datetime import datetime

from app.utils import check_input
from app.extensions import db
from app.controllers.v1 import v1_blueprint
from app.models import Performance, ActorsEmployment


@v1_blueprint.route("/performances", methods=['POST'])
def save_performance():
    session = db.session
    request_json = request.json or {}
    schema = {
        "name": str,
        "year_of_production": str,
        "budget": float
    }
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    request_json['year_of_production'] = datetime.strptime(request_json['year_of_production'], '%y-%m-%d')
    performance = Performance(**request_json)
    session.add(performance)
    session.commit()
    return jsonify({'msg': 'Success', 'performance_id': performance.id})


@v1_blueprint.route("/performances/<int:performance_id>")
def get_performance(performance_id):
    performance = Performance.query.get(performance_id)
    if performance is None:
        return jsonify({'msg': 'No such performance'}), 404
    return jsonify({'msg': 'Success', 'performance': performance.to_json()})


@v1_blueprint.route("/all_performances")
def get_all_performances():
    performances = Performance.query.all()
    return jsonify({'msg': 'Success', 'performances': [performance.to_json() for performance in performances]})


@v1_blueprint.route("/performances/user_add", methods=['POST'])
def add_actor():
    session = db.session
    request_json = request.json or {}
    schema = {
        "actor_id": int,
        "performance_id": int,
        "role_id": int
    }
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    if ActorsEmployment.query.filter(ActorsEmployment.actor_id == request_json['actor_id'],
                                     ActorsEmployment.performance_id == request_json['performance_id']).first() is not None:
        return jsonify({'msg': 'This actor is already attached to this performance'}), 400

    actor_employments = ActorsEmployment(**request_json)
    session.add(actor_employments)
    session.commit()
    return jsonify({'msg': 'Success'}), 201
