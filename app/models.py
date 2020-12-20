from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, FLOAT, DATE, SMALLINT

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


class Actor(db.Model, BaseModel):
    __tablename__ = 'actors'

    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(VARCHAR(100), nullable=False)
    surname = db.Column(VARCHAR(100), nullable=False)
    patronymic = db.Column(VARCHAR(100), nullable=False)
    rank = db.Column(VARCHAR(100), nullable=False)
    experience = db.Column(VARCHAR(100), nullable=False)
    achievements = db.Column(VARCHAR(100), nullable=False)
    salary = db.Column(FLOAT, default=0)
    balance = db.Column(FLOAT, default=0)
    created_at = db.Column(DATE, default=datetime.utcnow)
    updated_at = db.Column(DATE, default=datetime.utcnow)

    def __repr__(self):
        return self.name


class Performance(db.Model, BaseModel):
    __tablename__ = 'performances'

    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(VARCHAR(100), nullable=False)
    year_of_production = db.Column(DATE, nullable=False)
    budget = db.Column(FLOAT, nullable=False)
    created_at = db.Column(DATE, default=datetime.utcnow)
    updated_at = db.Column(DATE, default=datetime.utcnow)

    def to_json(self, columns_to_exclude=None):
        to_json = super().to_json()
        to_json['actors'] = self.get_actors()
        return to_json

    def get_actors(self):
        actor_ids = [
            actor_raw[0] for actor_raw in
            ActorsEmployment.query.with_entities(ActorsEmployment.actor_id)
            .filter(ActorsEmployment.performance_id == self.id).all()
        ]
        actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
        return [actor.to_json() for actor in actors]

    def __repr__(self):
        return self.name


class Role(db.Model, BaseModel):
    __tablename__ = 'roles'

    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(VARCHAR(100), nullable=False)
    created_at = db.Column(DATE, default=datetime.utcnow)
    updated_at = db.Column(DATE, default=datetime.utcnow)

    def __repr__(self):
        return self.name


class ActorsEmployment(db.Model, BaseModel):
    __tablename__ = 'actors_employments'

    id = db.Column(BIGINT, primary_key=True)
    actor_id = db.Column(BIGINT, db.ForeignKey(Actor.__table__.c.id), nullable=False)
    performance_id = db.Column(BIGINT, db.ForeignKey(Performance.__table__.c.id), nullable=False)
    role_id = db.Column(BIGINT, db.ForeignKey(Role.__table__.c.id), nullable=False)
    created_at = db.Column(DATE, default=datetime.utcnow)
    updated_at = db.Column(DATE, default=datetime.utcnow)


class Contract(db.Model, BaseModel):
    __tablename__ = 'contracts'

    id = db.Column(BIGINT, primary_key=True)
    term = db.Column(VARCHAR(100), nullable=False)
    actor_id = db.Column(BIGINT, db.ForeignKey(Actor.__table__.c.id), nullable=False)
    salary = db.Column(FLOAT, nullable=False)
    min_premium_amount = db.Column(SMALLINT, nullable=False)
    sign_date = db.Column(DATE, default=datetime.utcnow)
    expiration_date = db.Column(DATE, default=datetime.utcnow)

    created_at = db.Column(DATE, default=datetime.utcnow)
    updated_at = db.Column(DATE, default=datetime.utcnow)

    actor = db.relationship("Actor")

    def __repr__(self):
        return f"Actor: {self.actor.name}, ID: {self.id}"


class PremiumConfigs(db.Model, BaseModel):
    __tablename__ = 'premium_configs'

    id = db.Column(BIGINT, primary_key=True)
    performance_num = db.Column(SMALLINT, nullable=False)
    prize = db.Column(FLOAT, nullable=False)

    @staticmethod
    def get_prize(performance_num):
        performance = PremiumConfigs.query.filter(PremiumConfigs.performance_num == performance_num).first()

        return 0 if performance is None else performance.prize

    def __repr__(self):
        return f"Num: {self.performance_num}, prize: {self.prize}"
