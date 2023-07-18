from parameterized_mortgage import BaseLoan

value = 100000
rate = 8
term = 30
repayment = 733.76
total_interest = 164155.25
mean_interest = round(total_interest / term / 12, 2)

def test_loan_periodic_repayment():
    loan = BaseLoan(principal=value, periodic_rate=rate / 12, number_of_periods=30 * 12)
    assert round(loan.periodic_repayment, 2) == repayment

def test_loan_total_interest():
    loan = BaseLoan(principal=value, periodic_rate=rate / 12, number_of_periods=30 * 12)
    assert round(loan.total_interest, 2) == total_interest

def test_loan_mean_interest():
    loan = BaseLoan(principal=value, periodic_rate=rate / 12, number_of_periods=30 * 12)
    assert round(loan.mean_interest_per_payment_period, 2) == mean_interest
