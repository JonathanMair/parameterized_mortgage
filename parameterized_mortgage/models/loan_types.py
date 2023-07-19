import pandas as pd
import param
import panel as pn
from typing import Dict

from .calcs import loan_repayment_metrics


class LoanBase(param.Parameterized):
    """Parameterized class to model a mortgage loan and provide methods to calculate repayments and schedule.

    Based on the following equation:
    E = P . r . (1+r)^n/((1+r)^n - 1)

    Where:

        E = periodic_repayment
        P = principal at the beginning of the mortgage
        r = the periodic interest rate
        n = the number of periods

    """
    # user settings
    principal = param.Number(
        100000, doc="The principal or loan amount at the beginning of the mortgage.", bounds=(0, None)
    )
    periodic_rate = param.Number(
        5 / 12, doc="Interest rate applied per period", bounds=(0, None)
    )
    number_of_periods = param.Number(
        240, doc="Number of periods over which payments will be spread.", bounds=(1, None)
    )

    # calculated properties
    periodic_repayment = param.Number(constant=True, precedence=-1)
    total_interest = param.Number(constant=True, precedence=-1)
    mean_interest_per_payment_period = param.Number(constant=True, precedence=-1)

    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def calculate_dependent_params(self, reference_period_repayment_period_ratio: int = 1):
        """Calculates periodic repayment and information about interest on a loan and sets dependent params.

        Parameters:
            int: reference_period_repayment_period_ratio
            repayment period / reference period. e.g. where reference period is one year and repayment period is
            one month: 12. This argument defaults to 1 and is intended to be used with subclasses to allow them to
            express interest in one unit of time (e.g., year) and repayment periods in another (e.g., months).
        """
        periodic_repayment, total_interest, mean_interest = \
            loan_repayment_metrics(self.principal, self.periodic_rate, self.number_of_periods)
        with param.edit_constant(self):
            self.periodic_repayment, self.total_interest, self.mean_interest_per_payment_period = \
                periodic_repayment, total_interest, mean_interest
        return periodic_repayment, total_interest, mean_interest

    @param.depends('calculate_dependent_params')
    def live_df(self, passed_dict: Dict=None):
        d = {
            'Periodic Repayment': self.periodic_repayment,
            'Total Interest': self.total_interest,
            'Mean Periodic Interest': self.mean_interest_per_payment_period
        } if passed_dict is None else passed_dict
        df = pd.DataFrame(list(d.values()), index=list(d.keys()))
        return pn.pane.DataFrame(df)

    def panel_param(self, parameters: [str], widgets: Dict):
        """Returns a customised panel.Param object linked to this instance"""




'''todo: set up panel_param() method to return suitable param set with annual interest rate 
add a param for annual interest rate and use it to set a dependent method to update superclass interest property
'''


class Mortgage(LoanBase):
    annual_interest_rate = param.Number(
        bounds=(0, None),
        doc="Annual interest rate for mortgage loan, expressed as a %."
    )
    mortgage_term = param.Integer(
        bounds=(0, None),
        doc=""
    )

    def __init__(self, loan_amount, annual_rate, term_in_years):
        kwargs = {
            'principal': loan_amount,
            'periodic_rate': annual_rate / 12,
            'number_of_periods': term_in_years * 12
        }
        super().__init__(**kwargs)


    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def calculate_dependent_params(self):
        return super().calculate_dependent_params(reference_period_repayment_period_ratio=12)


