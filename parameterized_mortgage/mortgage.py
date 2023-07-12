import param


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
        5, doc="Interest rate applied per period", bounds=(0, 100)
    )
    number_of_periods = param.Number(
        240, doc="Number of periods over which payments will be spread."
    )
    periodic_repayment = param.Number(
        0, doc="The amount payable each repayment period. Read only.", readonly=True, bounds=(0, None)
    )

    

