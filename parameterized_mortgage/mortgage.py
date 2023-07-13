import param
import panel as pn

class Loan(param.Parameterized):
    """Parameterized class to model a mortgage loan and provide methods to calculate repayments and schedule.

    Based on the following equation:
    E = P . r . (1+r)^n/((1+r)^n - 1)

    Where:

        E = periodic_repayment
        P = principal at the beginning of the mortgage
        r = the periodic interest rate
        n = the number of periods

    """
    # user-defined settings
    principal = param.Number(
        100000, doc="The principal or loan amount at the beginning of the mortgage.", bounds=(0, None)
    )
    periodic_rate = param.Number(
        5/12, doc="Interest rate applied per period", bounds=(0, 100)
    )
    number_of_periods = param.Number(
        240, doc="Number of periods over which payments will be spread.", bounds=(1, None)
    )

    # outputs
    periodic_repayment = param.Number(
        doc="Repayment due each period. Not settable by the user.",
        constant=True
    )
    total_interest = param.Number(
        doc="Calculated amount of interest payable over the whole lifetime of the loan. . Not settable by the user.",
        constant=True
    )
    mean_interest_per_payment_period = param.Number(
        doc="Calculated amount of interest payable over the whole lifetime of the loan. Not settable by the user.",
        constant=True
    )

    # todo: do I need watch=True here?
    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def calculate_dependent_params(self):
        """Calculates periodic repayment and information about interest on a loan and sets dependent params."""
        principal, periodic_rate, number_of_periods = self.principal, self.periodic_rate, self.number_of_periods
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



class Mortgage(Loan):
    pass


