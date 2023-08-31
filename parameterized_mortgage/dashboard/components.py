"""Module provides panel components for use in a dashboard"""
import pandas as pd
import panel as pn
import param
from bokeh.models import NumberFormatter

formatters = {
    "payment": NumberFormatter(format="0,0", text_align="right"),
    "interest": NumberFormatter(format="0,0", text_align="right"),
    "capital repayment": NumberFormatter(format="0,0", text_align="right"),
    "balance": NumberFormatter(format="0,0", text_align="right"),
    "value": NumberFormatter(format="0,0", text_align="right"),
}

tabulator_settings = {
    "disabled": True, "formatters": formatters, "text_align": "right",  "height": 600
}


class PCard(pn.Card):
    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        self.collapsible = False
        self.objects.append(pn.VSpacer())
        self.height_policy = "fixed"

class MonthlyRepaymentCard(pn.Card):
    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        self.collapsible = False
        self.objects.append(pn.VSpacer())


class Settings(pn.Param):
    def __init__(self, mortgage, **params):
        params["widgets"] = mortgage.custom_widgets()
        super().__init__(object=mortgage, **params)
        self.collapsible = False
        self.name = ""


class SettingsCard(PCard):
    def __init__(self, mortgage, **params):
        settings = Settings(mortgage=mortgage)
        objs = [settings]
        self.title = "Mortgage Settings"
        super().__init__(*objs, **params)




class ScheduleRow(pn.Row):


    def __init__(self, mortgage, summary_type="monthly", **params):
        """Argument summary_type determines whether the table returned is a full amortization table (default), or
        an annual summary (summary_type=\"annual_summary\"), or a lifetime summary (summary_type=\"lifetime_summary\".
        """
        super().__init__(**params)
        function_ = mortgage.lifetime_summary
        if summary_type == "monthly":
            function_ = mortgage.repayment_schedule
        elif summary_type == "annual summary":
            function_ = mortgage.annual_summary
        tabulator = pn.widgets.Tabulator(
            function_, **tabulator_settings
        )
        self.title = f"Repayment schedule: {summary_type}"
        self.objects = [tabulator]
