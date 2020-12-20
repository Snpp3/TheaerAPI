import sys

from app.cronjobs import SalaryPayment
from app.app import create_app

app = create_app()


def salary_payment_run():
    with app.app_context():
        salary_payment = SalaryPayment()
        salary_payment.run()


if __name__ == '__main__':
    eval(sys.argv[1])()
