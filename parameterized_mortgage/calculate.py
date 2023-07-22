"""Module provides parameterized functions for calculating data for mortgages."""

import pandas as pd
import param


class monthly_payment(param.ParameterizedFunction):
    """Returns monthly repayment amount for given mortgage."""
    principal = param.Number(0, doc="Loan principal at outset.", bounds=(0, None))
    rate = param.Number(0, doc="Annual interest rate espressed as a %.", bounds=(0, None))
    term = param.Number(1, doc="Mortgage term in years", bounds=(1, None))

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        monthly_interest = p.rate / 1200 # convert annual % rate to decimal and spread over 12 months
        number_of_periods = p.term * 12 # 12 repayments per year
        compound = (1 + monthly_interest) ** number_of_periods
        repayment_amount = p.principal * monthly_interest * compound / (compound - 1) \
            if monthly_interest != 0 and p.principal != 0 else 0.0
        return repayment_amount

class repayment_schedule(param.ParameterizedFunction):
    """Return a DataFrame of a repayment for mortgage of given characteristics."""
    principal = param.Number(doc="Loan principal at outset.", bounds=(0, None), allow_None=False)
    rate = param.Number(doc="Annual interest rate espressed as a %.", bounds=(0, None), allow_None=False)
    term = param.Number(doc="Mortgage term in years", bounds=(0, None), allow_None=False)

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)

        # get monthly repayment amount
        monthly_payment_amount = monthly_payment(
            principal=p.principal,
            rate=p.rate,
            term=p.term
        )
        monthly_interest = p.rate / 1200

        # set up variables for df columns
        months = range(1, p.term * 12 + 1)
        years = [int((m-0.01)//12 + 1) for m in months]
        monthly_payments = [monthly_payment_amount] * len(months)
        interest_payments = []
        balances = []
        capital_repayments = []

        # starting balance
        balance = p.principal

        # calculate rows
        for month in months:
            interest_due = balance * monthly_interest
            interest_payments.append(interest_due)
            capital_repayment = monthly_payment_amount - interest_due
            capital_repayments.append(capital_repayment)
            balance -= capital_repayment
            balances.append(balance)

        # construct df
        columns = ["year", "month", "payment", "interest", "capital repayment", "balance"]
        data = zip(years, months, monthly_payments, interest_payments, capital_repayments, balances)
        df = pd.DataFrame(data, columns=columns)
        df = df.set_index(keys=["month", "year"])

        return df


class annual_summary(param.ParameterizedFunction):
    """Return a year-by-year summary in a pd.DataFrame when passed a mortgage repayment schedule
    in the format supplied by calcs.repayment_schedule().
    """
    repayment_schedule = param.DataFrame(
        doc="DataFrame in the format returned by calcs.repayment_schedule()"
    )

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        by_year = p.repayment_schedule.groupby("year")
        summary_df = by_year[["payment", "interest", "capital repayment"]].sum()
        summary_df["balance"] = by_year["balance"].last()
        return summary_df


class lifetime_summary(param.ParameterizedFunction):
    """Return a lifetime summary as a pd.DataFrame."""
    annual_summary = param.DataFrame(
        doc="DataFrame in the format returned by calcs.annual_summary()"
    )

    def __call__(self, **params):
        p = param.ParamOverrides(self, params)
        lifetime = p.annual_summary[["payment", "interest", "capital repayment"]].sum()
        return lifetime

