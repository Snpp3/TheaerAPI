from flask import request, jsonify

from app.utils import check_input
from app.extensions import db
from app.controllers.v1 import v1_blueprint
from app.models import Actor, Role


@v1_blueprint.route("/actors", methods=['POST'])
def save_actor():
    session = db.session
    request_json = request.json or {}
    schema = {
        "name": str,
        "surname": str,
        "patronymic": str,
        "rank": str,
        "experience": str,
        "achievements": str,
        "balance": float
    }
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    actor = Actor(**request_json)
    session.add(actor)
    session.commit()
    return jsonify({'msg': 'Success', 'actor_id': actor.id}), 201


@v1_blueprint.route("/actors/<int:actor_id>")
def get_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        return jsonify({'msg': 'No such actor'}), 404
    return jsonify({'msg': 'Success', 'actor': actor.to_json()})


@v1_blueprint.route("/roles", methods=['POST'])
def save_role():
    session = db.session
    request_json = request.json or {}
    schema = {
        "name": str
    }
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    role = Role(**request_json)
    session.add(role)
    session.commit()
    return jsonify({'msg': 'Success', 'role_id': role.id}), 201


@v1_blueprint.route("/roles/<int:role_id>")
def get_role(role_id):
    role = Role.query.get(role_id)
    if role is None:
        return jsonify({'msg': 'No such role'}), 404
    return jsonify({'msg': 'Success', 'role': role.to_json()})
