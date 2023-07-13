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
    principal = param.Number(
        100000, doc="The principal or loan amount at the beginning of the mortgage.", bounds=(0, None)
    )
    periodic_rate = param.Number(
        5/12, doc="Interest rate applied per period", bounds=(0, 100)
    )
    number_of_periods = param.Number(
        240, doc="Number of periods over which payments will be spread.", bounds=(1, None)
    )
    periodic_repayment = param.Number(
        doc="Calculated repayment due each period.", constant=True
    )

    def _get_periodic_repayment(self):
        """Calculate the periodic repayment using the independent parameters"""
        periodic_repayment = \
            self.principal * self.periodic_rate/100 \
            * (1+self.periodic_rate/100)**self.number_of_periods\
            / (((1+self.periodic_rate/100)**self.number_of_periods) - 1)
        return periodic_repayment

    @param.depends('principal', 'periodic_rate', 'number_of_periods', on_init=True, watch=True)
    def _update_periodic_repayment(self):
        with param.edit_constant(self):
            self.periodic_repayment = self._get_periodic_repayment()

    @param.depends('principal', 'periodic_rate', 'number_of_periods')
    def view_periodic_payment(self):
        return pn.pane.Str(str(self._get_periodic_repayment()))


class Mortgage(Loan):
    pass


