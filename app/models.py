from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, JSON, TIMESTAMP

from app.extensions import db


class BaseModel:

    def to_json(self, columns_to_exclude=None):
        if columns_to_exclude is None:
            columns_to_exclude = []
        json_obj = {}
        for column in self.__table__.columns:
            column = column.description
            if column in columns_to_exclude:
                continue
            value = getattr(self, column)
            if type(value) is date:
                value = value.strftime("%d-%m-%Y")
            elif type(value) is datetime:
                value = value.strftime("%d-%m-%Y %H:%M:%S")
            elif isinstance(value, Decimal):
                value = float(value)
            json_obj[column] = value
        return json_obj


class Patient(db.Model, BaseModel):
    __tablename__ = 'patients'

    id = db.Column(BIGINT, primary_key=True)
    prescription_id = db.Column(VARCHAR(100), nullable=False)
    data = db.Column(JSON, nullable=False)
    created_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)


class PatientReference(db.Model, BaseModel):
    __tablename__ = 'patient_references'

    id = db.Column(BIGINT, primary_key=True)
    patient_id = db.Column(BIGINT, db.ForeignKey(Patient.__table__.c.id), nullable=False)
    data = db.Column(JSON, nullable=False)
    created_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)

    patient = db.relationship("Patient", backref="reference")


class PatientBaselineSpecimens(db.Model, BaseModel):
    __tablename__ = 'patient_baseline_specimens'

    id = db.Column(BIGINT, primary_key=True)
    patient_id = db.Column(BIGINT, db.ForeignKey(Patient.__table__.c.id), nullable=False)
    audio_url = db.Column(VARCHAR(255), nullable=False)
    created_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)
    updated_at = db.Column(TIMESTAMP(0), default=datetime.utcnow)

    patient = db.relationship("Patient", backref="baseline_specimen")
