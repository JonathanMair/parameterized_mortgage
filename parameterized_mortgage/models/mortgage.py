import param
import panel as pn
import pandas as pd
import hvplot.pandas

import parameterized_mortgage.calculate as calculate

hvplot.extension("plotly")
pd.options.display.float_format = "{:,.2f}".format
pn.extension("tabulator")


class Mortgage(param.Parameterized):
    """Provides methods for calculating mortgage data."""

    # user settings
    principal = param.Number(100000, bounds=(0, None), doc="Amount borrowed.")
    rate = param.Number(
        4, bounds=(0, None), doc="Annual interest rate expressed as a percentage."
    )
    term = param.Integer(20, bounds=(1, None), doc="Mortgage term in years.")

    # calculated properties
    monthly_payment = param.Number(constant=True, precedence=-1)

    @param.depends("principal", "rate", "term", watch=True, on_init=True)
    def _calculate_dependent_parameters(self):
        """Calculate mortgage interest data and set corresponding parameters."""
        with param.edit_constant(self):
            self.monthly_payment = calculate.get_monthly_payment(
                principal=self.principal, rate=self.rate, term=self.term
            )

    @param.depends("_calculate_dependent_parameters")
    def repayment_schedule(self) -> pd.DataFrame:
        df = calculate.repayment_schedule(
            principal=self.principal, rate=self.rate, term=self.term
        )
        return df

    @param.depends("_calculate_dependent_parameters")
    def annual_summary(self) -> pd.DataFrame:
        df = self.repayment_schedule()
        annual_summary_df = calculate.annual_summary(repayment_schedule=df)
        return annual_summary_df

    @param.depends("_calculate_dependent_parameters")
    def lifetime_summary(self):
        df = self.annual_summary()
        lifetime_summary_df = calculate.lifetime_summary(annual_summary=df)
        return lifetime_summary_df

    def custom_widgets(self):
        """Returns dictionary detailing customised widgets for a panel.Param object."""
        return {
            "principal": {"type": pn.widgets.FloatInput, "start": 0, "step": 1000},
            "rate": {
                "type": pn.widgets.FloatInput,
                "start": 0,
                "end": 10,
                "step": 0.01,
            },
            "term": {
                "type": pn.widgets.IntSlider,
                "start": 0,
                "end": 40,
                "step": 1,
                "name": "term in years",
            },
        }

    @param.depends("repayment_schedule")
    def amortization_chart(self):
        fig = (
            self.repayment_schedule()["balance"]
            .hvplot(
                kind="line",
                y=["balance"],
                title="",
                height=360,
                width=600,
                legend=False,
            )
        )
        return pn.panel(fig, sizing_mode="stretch_width")

    @param.depends("repayment_schedule")
    def chart_interest_vs_capital(self):
        layout = (
            self.repayment_schedule()
            .hvplot(
                kind="area",
                stacked=False,
                legend=False,
                y=["interest", "capital repayment"],
                height=360,
                width=600,
            )
        )
        return pn.panel(layout, sizing_mode="stretch_width")


    @param.depends("_calculate_dependent_parameters")
    def get_monthly_payment(self):
        return f"{self.monthly_payment:,.0f}"
