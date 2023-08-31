import panel as pn
from panel.theme import Material

import parameterized_mortgage
import parameterized_mortgage.dashboard.components as cp


def get_dashboard_demo():
    """Returns panel template object with demo of the Mortgage class"""
    pn.extension("tabulator")
    pn.config.throttled = True
    pn.config.design = Material
    pn.config.sizing_mode = "stretch_both"
    loan = parameterized_mortgage.Mortgage(principal=250000, rate=5, term=30)
    settings = cp.SettingsCard(mortgage=loan)
    interest_vs_capital = cp.PCard(
        loan.chart_interest_vs_capital, title="Interest vs capital repayments"
    )
    balance_over_time = cp.PCard(loan.amortization_chart, title="Balance of loan")
    summary_types = ["monthly", "annual summary", "lifetime summary"]
    tab_objects = []
    for s in summary_types:
        tabulator = cp.ScheduleRow(mortgage=loan, summary_type=s)
        tab_objects.append((s, tabulator))
    charts_row = pn.Row(interest_vs_capital, balance_over_time)
    schedule_tabs = pn.Tabs(objects=tab_objects)
    schedule_card = cp.PCard(schedule_tabs, title="Repayment schedule")
    schedule_card.height_policy="fit"
    monthly_payment_card = cp.MonthlyRepaymentCard(
        pn.panel(loan.get_monthly_payment),
        title="Monthly repayment"
    )

    template = pn.template.BootstrapTemplate(
        title="parameterized_mortgage",
        sidebar=[],
        main=[
            pn.Row(
                pn.Column(
                    pn.Row(settings, monthly_payment_card),
                    pn.Row(charts_row),
                    pn.Row(schedule_card)
                ),
            )
        ],
    )

    return template
