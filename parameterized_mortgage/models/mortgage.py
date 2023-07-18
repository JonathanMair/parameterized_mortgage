import param
import panel as pn


class BaseLoan(param.Parameterized):
    """Parameterized class to model a mortgage loan and provide methods to calculate repayments and schedule.

    Based on the following equation:
    E = P . r . (1+r)^n/((1+r)^n - 1)

    Where:

        E = periodic_repayment
        P = principal at the beginning of the mortgage
        r = the periodic interest rate
        n = the number of periods

    """
    # parameters
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
    periodic_repayment: float
    total_interest: float
    mean_interest_per_payment_period: float

    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def calculate_dependent_params(self, reference_period_repayment_period_ratio: int=1):
        """Calculates periodic repayment and information about interest on a loan and sets dependent params.

        Parameters:
            int: reference_period_repayment_period_ratio
            repayment period / reference period. e.g. where reference period is one year and repayment period is
            one month: 12. This argument defaults to 1 and is intended to be used with subclasses to allow them to
            express interest in one unit of time (e.g., year) and repayment periods in another (e.g., months).
        """
        principal, periodic_rate, number_of_periods = self.principal, self.periodic_rate, self.number_of_periods
        periodic_rate /= reference_period_repayment_period_ratio
        number_of_periods *= reference_period_repayment_period_ratio
        periodic_repayment = \
            principal * periodic_rate / 100 \
            * (1 + periodic_rate / 100) ** number_of_periods \
            / (((1 + periodic_rate / 100) ** number_of_periods) - 1) \
            if periodic_rate != 0 and principal != 0 else 0.0
        total_interest = periodic_repayment * number_of_periods - principal
        mean_interest = total_interest / number_of_periods
        with param.edit_constant(self):
            self.periodic_repayment, self.total_interest, self.mean_interest_per_payment_period = \
                periodic_repayment, total_interest, mean_interest
        return  (periodic_repayment, total_interest, mean_interest)

    @param.depends('calculate_dependent_params')
    def live_repayment_amount(self, rate=None):
        self.periodic_rate = rate if rate is not None else self.periodic_rate
        self.calculate_dependent_params()
        return pn.panel(self.periodic_repayment)

    @param.depends('calculate_dependent_params')
    def live_mortgage_metrics_panel(self):
        s = f"""* Repayment amount: {self.periodic_repayment:.2f}\n
        * Total interest: {self.total_interest:.2f}\n
        * Mean interest: {self.mean_interest_per_payment_period:.2f}\n
        """
        return pn.panel(s)



'''todo: set up panel_param() method to return suitable param set with annual interest rate 
add a param for annual interest rate and use it to set a dependent method to update superclass interest property
'''
class Mortgage(BaseLoan):
    annual_interest_rate = param.Number(
        bounds=(0, None),
        doc="Annual interest rate for mortgage loan, expressed as a %."
    )
    mortgage_term = param.Integer(
        bounds=(0, None),
        doc=""
    )

    def __init__(self, **kwargs):
        kwargs['periodic_rate'] = self.annual_interest_rate / 12
        kwargs['number_of_periods'] = self.mortgage_term * 12
        super().__init__(**kwargs)

    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def calculate_dependent_params(self):
        return super().calculate_dependent_params(reference_period_repayment_period_ratio=12)

