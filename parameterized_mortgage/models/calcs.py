def loan_repayment_metrics(
    principal: float, periodic_rate: float, number_of_periods: int, reference_period_repayment_period_ratio=1
):
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
        (float, float, float): periodic repayment amount, total interest payable over the life of the loan,
        mean interest paid in each repyament period
    """
    periodic_rate /= reference_period_repayment_period_ratio
    number_of_periods *= reference_period_repayment_period_ratio
    periodic_repayment = \
        principal * periodic_rate / 100 \
        * (1 + periodic_rate / 100) ** number_of_periods \
        / (((1 + periodic_rate / 100) ** number_of_periods) - 1) \
            if periodic_rate != 0 and principal != 0 else 0.0
    total_interest = periodic_repayment * number_of_periods - principal
    mean_interest = total_interest / number_of_periods
    return periodic_repayment, total_interest, mean_interest
