from parameterized_mortgage import Loan

value = 100000
rate = 8
term = 30
repayment = 733.76

def test_loan_periodic_repayment():
    loan = Loan(principal=value, periodic_rate=rate/12, number_of_periods=30*12)
    assert round(loan.periodic_repayment, 2) == repayment
