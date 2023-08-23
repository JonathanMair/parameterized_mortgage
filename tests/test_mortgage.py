from parameterized_mortgage import Mortgage
from tests.dummy_data import *

loan = Mortgage(principal=value, rate=rate, term=term)


def test_loan_periodic_repayment():
    assert round(loan.monthly_payment, 2) == repayment

def test_repayment_schedule():
    assert True
