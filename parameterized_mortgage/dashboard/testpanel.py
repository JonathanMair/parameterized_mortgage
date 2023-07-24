import panel as pn
from panel.theme import Material
from pathlib import Path

import parameterized_mortgage


path = Path(__file__).with_name("piso_rentable.png")
with open(path, "rb") as f:
    logo = f.read()

pn.config.throttled = True
pn.config.design = Material


loan = parameterized_mortgage.Mortgage(principal=67000, rate=3.4, term=30)

stats_row = pn.Row(
    loan.mortgage_stats_table,
    loan.chart_interest_vs_capital,
    loan.amortization_chart
)

template = pn.template.MaterialTemplate(
    title="Piso Rentable",
    logo="./piso_rentable.png",
    sidebar=pn.Param(
        loan,
        widgets=loan.custom_widgets()
    ),
    main=[
        stats_row,
        loan.repayment_schedule
    ]
)

template.servable()



""""
        pn.widgets.Tabulator(
            loan.repayment_schedule,
            disabled=True,
            formatters={
                "Value": NumberFormatter(format="0,0.00", text_align="right")
            },
            text_align="right"
        ),

"""

