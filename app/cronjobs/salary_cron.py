from datetime import date, timedelta

from app.models import Actor, ActorsEmployment, Contract, PremiumConfigs
from app.extensions import db


class SalaryPayment:

    def __init__(self):
        pass

    def run(self):
        actors = Actor.query.all()
        for actor in actors:
            self.pay_salary(actor)

    @staticmethod
    def pay_salary(actor):
        num_plays = ActorsEmployment.query.filter(ActorsEmployment.actor_id == actor.id, ActorsEmployment.created_at > date.today() - timedelta(days=30)).count()
        contract = Contract.query.filter(Contract.actor_id == actor.id).first()
        if contract is None:
            return
        premium = PremiumConfigs.get_prize(num_plays)
        actor.balance += actor.salary + premium if contract.min_premium_amount <= num_plays else 0
        session = db.session
        session.add(actor)
        session.commit()
