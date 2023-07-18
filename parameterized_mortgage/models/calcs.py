def loan_repayment_metrics(
    principal: float, periodic_rate: float, number_of_periods, reference_period_repayment_period_ratio=1
):
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
