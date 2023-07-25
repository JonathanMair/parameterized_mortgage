import param
import panel as pn
import pandas as pd
import hvplot.pandas
pd.options.display.float_format = '{:,.2f}'.format

import parameterized_mortgage.calculate as calculate

pn.extension('tabulator', )


class Mortgage(param.Parameterized):
    """Provides methods for calculating mortgage data. 
    """

    # user settings
    principal = param.Number(
        100000,
        bounds=(0, None),
        doc="Amount borrowed."
    )
    rate = param.Number(
        4,
        bounds=(0, None),
        doc="Annual interest rate expressed as a percentage."
    )
    term = param.Integer(
        20,
        bounds=(1, None),
        doc="Mortgage term in years."
    )

    # calculated properties
    monthly_payment = param.Number(constant=True, precedence=-1)

    @param.depends("principal", "rate", "term", watch=True, on_init=True)
    def calculate_dependent_parameters(self):
        """Calculate mortgage interest data and set corresponding parameters."""
        with param.edit_constant(self):
            self.monthly_payment = calculate.get_monthly_payment(principal=self.principal, rate=self.rate, term=self.term)

    # todo: split these returned data into two methods
    @param.depends("get_monthly_payment")
    def live_df(self):
        """Returns a DataFrame containing interest data, updated as figures change."""
        index = ["Monthly repayment"]
        values = [self.monthly_payment]
        df = pd.DataFrame(values, index=index, columns=["Value"])
        return df

    @param.depends("calculate_dependent_parameters")
    def repayment_schedule(self) -> pd.DataFrame:
        df = calculate.repayment_schedule(principal=self.principal, rate=self.rate, term=self.term)
        return df

    @param.depends("calculate_dependent_parameters")
    def annual_summary(self) -> pd.DataFrame:
        pass

    @param.depends("calculate_dependent_parameters")
    def lifetime_summary(self):
        pass

    def custom_widgets(self):
        """Returns dictionary detailing customised widgets for a panel.Param object."""
        return {
            "principal": {
                "type": pn.widgets.FloatInput,
                "start": 0,
                "step": 1000
            },
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
                "name": "term in years"
            }
        }

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __pprint__(self):
        pass

#got here....

    @param.depends("repayment_schedule")
    def amortization_chart(self):
        fig = self.repayment_schedule()["balance"].hvplot()
        return pn.panel(fig, sizing_mode="stretch_width")


    @param.depends("repayment_schedule")
    def chart_interest_vs_capital(self):
        layout = self.repayment_schedule().hvplot(
            kind="area",
            stacked=True,
            legend="top",
            y=["interest", "capital repayment"],
        )
        fig = layout.opts(
            title="Interest and Capital Repayments",
        )
        return pn.panel(fig, sizing_mode="stretch_width")

    @param.depends("calculate_dependent_parameters")
    def mortgage_stats_table(self):
        stats = calculate.get_mortgage_stats(principal=self.principal, rate=self.rate, term=self.term)
        df = pd.DataFrame(stats.values(), index=stats.keys()).round(2)
        return df
