"""Module provides panel components for use in a dashboard"""

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

tabulator_settings = {"disabled": True, "formatters": formatters, "text_align": "right"}


class PCard(pn.Card):
    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        self.collapsible = False
        self.objects.append(pn.VSpacer())
        self.height_policy = "fixed"
        self.height = 450


class Settings(pn.Param):
    def __init__(self, mortgage, **params):
        params["widgets"] = mortgage.custom_widgets()
        super().__init__(object=mortgage, **params)
        self.collapsible = False
        self.name = ""


class SettingsCard(PCard):
    def __init__(self, mortgage, **params):
        repayment_indicator = pn.panel(mortgage.get_monthly_payment)
        settings = Settings(mortgage=mortgage)
        objs = [settings, repayment_indicator]
        self.title = "Mortgage Settings"
        super().__init__(*objs, **params)


class ScheduleCard(PCard):
    def __init__(self, mortgage, *objs, **params):
        # remove extra params before calling super()
        super().__init__(*objs, **params)
        tabulator = pn.widgets.Tabulator(
            mortgage.lifetime_summary, **tabulator_settings
        )
        self.title = "Repayment schedule"
        self.objects = [tabulator]
        self.collapsible = True
        self.collapsed = False
        self.height = 540
        self.height_policy = "min"
