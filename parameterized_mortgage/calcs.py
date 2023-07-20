import pandas as pd
import param


def loan_repayment_metrics(
    principal: float, periodic_rate: float, number_of_periods: int, reference_period_repayment_period_ratio=1
) -> (float, float):
    """Return a tuple of loan interest data.

        Based on the following equation:
        E = P . r . (1+r)^n/((1+r)^n - 1)

        Where:

            E = periodic_repayment
            P = principal at the beginning of the mortgage
            r = the periodic interest rate
            n = the number of periods

    Parameters:
        principal (float): amount of loan in given currency
        periodic_rate (float): interest rate to be applied per repayment period (i.e., for a mortgage, usually
        monthly)
        number_of_periods (int): number of repayment periods over which the principal is to be repaid

    Returns:
        (float, float): periodic repayment amount, total interest payable over the life of the loan
    """
    periodic_rate /= reference_period_repayment_period_ratio
    number_of_periods *= reference_period_repayment_period_ratio
    periodic_repayment = \
        principal * periodic_rate / 100 \
        * (1 + periodic_rate / 100) ** number_of_periods \
        / (((1 + periodic_rate / 100) ** number_of_periods) - 1) \
            if periodic_rate != 0 and principal != 0 else 0.0
    total_interest = periodic_repayment * number_of_periods - principal
    return periodic_repayment, total_interest

class mortgage_repayment_schedule(param.ParameterizedFunction):
    """Return a DataFrame of a repayment for mortgage of given characteristics."""
    principal = param.Number(doc="Loan principal at outset.", bounds=(0, None), allow_None=False)
    rate = param.Number(doc="Annual interest rate espressed as a %.", bounds=(0, None), allow_None=False)
    term = param.Number(doc="Mortgage term in years", bounds=(0, None), allow_None=False)

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)

        # get monthly repayment amount
        monthly_payment, _ = loan_repayment_metrics(
            principal=p.principal,
            periodic_rate=p.rate,
            number_of_periods=p.term,
            reference_period_repayment_period_ratio=12
        )

        # set up variables for df columns
        months = range(1, p.term * 12 + 1)
        years = [(m-0.01)//12 + 1 for m in months]
        monthly_payments = [monthly_payment] * len(months)
        interest_payments = []
        balances = []
        capital_repayments = []

        # starting balance
        balance = p.principal

        # calculate rows
        for month in months:
            interest_due = balance * p.rate
            interest_payments.append(interest_due)
            capital_repayment = monthly_payment - interest_due
            capital_repayments.append(capital_repayment)
            balance -= capital_repayment
            balances.append(balance)

        # construct df
        columns = ["year", "month", "payment", "interest", "capital repayment", "balance"]
        data = zip(years, months, monthly_payments, interest_payments, capital_repayments, balances)
        df = pd.DataFrame(data, columns=columns)

        return df
