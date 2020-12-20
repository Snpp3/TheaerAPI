from flask import request, jsonify

from app.models import Patient
from app.utils import check_input
from app.extensions import db
from app.controllers.v1 import v1_blueprint


@v1_blueprint.route("/patients", methods=['POST'])
def save_patient():
    session = db.session
    request_json = request.json or {}
    prescription_id = request_json.get('prescription_id')
    if prescription_id is None:
        return jsonify({'msg': 'Missing prescription_id in request body'}), 400

    data = request_json.get('data')
    if data is None:
        return jsonify({'msg': 'Missing data in request body'}), 400

    schema = {'prescription_id': str, 'data': dict}
    msg = check_input(request_json, schema)
    if msg is not None:
        return jsonify({'msg': msg}), 400

    if Patient.query.filter(Patient.prescription_id == prescription_id).scalar() is not None:
        return jsonify({'msg': f'Patient with prescription_id: {prescription_id} already exists'}), 400

    patient = Patient(prescription_id=prescription_id, data=data)
    session.add(patient)
    session.commit()
    return jsonify({'msg': 'Success'}), 201


@v1_blueprint.route('/patients/<string:prescription_id>')
def get_patient(prescription_id):
    patient = Patient.query.filter(Patient.prescription_id == prescription_id).first()
    if patient is None:
        return jsonify({'msg': f'No patient with prescription ID: {prescription_id}'}), 404
    return jsonify(patient.to_json(columns_to_exclude=['id', 'prescription_id']))
