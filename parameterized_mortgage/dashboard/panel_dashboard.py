import panel as pn
from panel.theme import Material

import parameterized_mortgage
import parameterized_mortgage.dashboard.components as cp


def get_dashboard_demo():
    """Returns panel template object with demo of the Mortgage class"""
    pn.extension("tabulator")
    pn.config.throttled = False
    pn.config.design = Material
    pn.config.sizing_mode = "stretch_width"
    loan = parameterized_mortgage.Mortgage(principal=67000, rate=3.4, term=30)
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

    stats_row = pn.Row(key_stats, interest_vs_capital, balance_over_time)

    template = pn.template.BootstrapTemplate(
        title="Mortgage Calculator  ",
        main=[
            pn.Row(
                pn.Column(settings, key_stats, width=320),
                pn.Column(
                    pn.Row(interest_vs_capital, balance_over_time), pn.Row(schedule)
                ),
            )
        ],
    )

    return template
