import param
import panel as pn
import pandas as pd

from parameterized_mortgage.calcs import loan_repayment_metrics

pn.extension('tabulator')


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
    monthly_repayment = param.Number(constant=True, precedence=-1)
    total_interest = param.Number(constant=True, precedence=-1)

    @param.depends("principal", "rate", "term", watch=True, on_init=True)
    def calculate_dependent_parameters(self):
        """Calculate mortgage interest data and set corresponding parameters."""
        with param.edit_constant(self):
            self.monthly_repayment, self.total_interest, _ = \
                loan_repayment_metrics(
                    principal=self.principal,
                    periodic_rate=self.rate,
                    number_of_periods=self.term,
                    reference_period_repayment_period_ratio=12
                )

    # todo: split these returned data into two methods
    @param.depends("monthly_repayment", "total_interest")
    def live_df(self):
        """Returns a DataFrame containing interest data, updated as figures change."""
        index = ["Monthly repayment", "Total interest payable"]
        values = [self.monthly_repayment, self.total_interest]
        df = pd.DataFrame(values, index=index, columns=["Value"])
        return df

    @param.depends("calculate_dependent_parameters")
    def repayment_schedule(self) -> pd.DataFrame:
        pass

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
                "type": pn.widgets.FloatSlider,
                "start": 0,
                "end": 10,
                "step": 0.01,
            },
            "term": {
                "type": pn.widgets.IntSlider,
                "start": 0,
                "end": 40,
                "step": 1
            }
        }

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __pprint__(self):
        pass

