import panel as pn
from panel.theme import Material
from pathlib import Path

import parameterized_mortgage
import parameterized_mortgage.dashboard.components as cp

pn.extension("tabulator", "bokeh")

path = Path(__file__).with_name("piso_rentable.png")
with open(path, "rb") as f:
    logo = f.read()

pn.config.throttled = True
pn.config.design = Material
pn.config.sizing_mode = "stretch_width"

loan = parameterized_mortgage.Mortgage(principal=67000, rate=3.4, term=30)

stats_row = pn.Row(
    cp.PCard(
        pn.widgets.Tabulator(loan.key_stats, disabled=True),
        title="Key stats"
    ),
    cp.PCard(
        loan.chart_interest_vs_capital,
        title="Interest vs capital repayments"
    ),
    cp.PCard(
        loan.amortization_chart,
        title="Balance of loan"
    )
)

template = pn.template.BootstrapTemplate(
    title="Piso Rentable",
    logo="./piso_rentable.png",
    sidebar=cp.SettingsCard(mortgage=loan),
    main=[
        pn.Column(
            stats_row,
            # cp.ScheduleCard(mortgage=loan)
        )
    ]
)

template.servable()

