import panel as pn
from panel.theme import Material

import parameterized_mortgage
import parameterized_mortgage.dashboard.components as cp


def get_dashboard_demo():
    """Returns panel template object with demo of the Mortgage class"""
    pn.extension("tabulator")
    pn.config.throttled = True
    pn.config.design = Material
    pn.config.sizing_mode = "stretch_width"
    loan = parameterized_mortgage.Mortgage(principal=250000, rate=5, term=30)
    settings = cp.SettingsCard(mortgage=loan)
    key_stats = cp.PCard(
        pn.widgets.Tabulator(loan.lifetime_summary, **cp.tabulator_settings),
        title="Lifetime summary",
    )
    interest_vs_capital = cp.PCard(
        loan.chart_interest_vs_capital, title="Interest vs capital repayments"
    )
    balance_over_time = cp.PCard(loan.amortization_chart, title="Balance of loan")
    schedule = cp.ScheduleCard(mortgage=loan)
    annual_summary = cp.ScheduleCard(mortgage=loan, summary_type="annual summary")
    lifetime_summary = cp.ScheduleCard(mortgage=loan, summary_type="lifetime summary")

    charts_row = pn.Row(interest_vs_capital, balance_over_time)

    monthly_payment_card = cp.MonthlyRepaymentCard(
        pn.panel(loan.get_monthly_payment),
        title="Monthly repayment"
    )

    template = pn.template.BootstrapTemplate(
        title="Mortgage Calculator  ",
        sidebar=[settings,],
        main=[
            pn.Row(
                pn.Column(
                    pn.Row(monthly_payment_card),
                    pn.Row(charts_row),
                    pn.Row(
                        pn.Tabs(
                            ("Repayment schedule: monthly", schedule),
                            ("Repayment schedule: annual summary", annual_summary),
                            ("Repayment schedule: lifetime summary", lifetime_summary),

                        )
                    ),
                ),
            )
        ],
    )

    return template
