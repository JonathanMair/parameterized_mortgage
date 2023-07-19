import pandas as pd
import param
import panel as pn
from typing import Dict

from .calcs import loan_repayment_metrics


class LoanBase(param.Parameterized):
    """Parameterized class to model a mortgage loan and provide methods to calculate repayments and schedule.
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


    # todo: format the df or work out how to do it in panel, esp wrt rounding of figures
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

    def custom_widgets(self, parameters: [str]=None, widgets: Dict=None, name: str=None):
        """Return customised widgets for panel.Param object."""
        if widgets is None:
            widgets={
                "principal": {
                    "type": pn.widgets.FloatInput,
                    "start": 0,
                    "step": 1000
                },
                "periodic_rate": {
                    "type": pn.widgets.FloatInput,
                    "start": 0,
                    "end": 5,
                    "step": 0.01,
                },
                "number_of_periods": {
                    "type": pn.widgets.IntInput,
                    "start": 0,
                    "step": 1
                }
            }
        return widgets




'''todo: set up panel_param() method to return suitable param set with annual interest rate 
add a param for annual interest rate and use it to set a dependent method to update superclass interest property

set precedence on periodic variables from super() to prevent them from appearing in panel.Param
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
        self.annual_interest_rate = annual_rate
        self.mortgage_term = term_in_years
        kwargs = {
            'principal': loan_amount,
            'periodic_rate': annual_rate / 12,
            'number_of_periods': term_in_years * 12
        }
        super().__init__(**kwargs)

        # set precedence to hide from pn.Param members of super that will now depend on parameters of this subclass
        self.param.periodic_rate.precedence = -1
        self.param.number_of_periods.precedence = -1


    # TODOOO THISSSSSS....
    @param.depends('principal',  on_init=True, watch=True)
    def calculate_dependent_params(self):
        return super().calculate_dependent_params(reference_period_repayment_period_ratio=12)


