from flask import request, jsonify
from datetime import datetime

from app.utils import check_input
from app.extensions import db
from app.controllers.v1 import v1_blueprint
from app.models import Contract, Actor


@v1_blueprint.route("/contracts", methods=['POST'])
def save_contracts():
    session = db.session
    request_json = request.json or {}
    schema = {
        "term": str,
        "actor_id": int,
        "salary_per_year": float,
        "min_premium_amount": int,
        "sign_date": str,
        "expiration_date": str
    }
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    if Contract.query.filter(Contract.actor_id == request_json['actor_id'], Contract.expiration_date > datetime.now()).first() is not None:
        return jsonify({'msg': 'This actor already has contract'}), 400

    actor = Actor.query.get(request_json['actor_id'])
    if actor is None:
        return jsonify({'msg': 'There is no such actor'}), 404

    request_json['sign_date'] = datetime.strptime(request_json['sign_date'], '%y-%m-%d')
    request_json['expiration_date'] = datetime.strptime(request_json['expiration_date'], '%y-%m-%d')
    contract = Contract(**request_json)
    session.add(contract)
    session.commit()

    actor.salary = request_json['salary_per_year'] / 12
    session.add(actor)
    session.commit()
    return jsonify({'msg': 'Success', 'contract_id': contract.id})


@v1_blueprint.route("/contracts/<int:contract_id>")
def get_contract(contract_id):
    contract = Contract.query.get(contract_id)
    if contract is None:
        return jsonify({'msg': 'No such contract'}), 404
    return jsonify({'msg': 'Success', 'contract': contract.to_json()})
