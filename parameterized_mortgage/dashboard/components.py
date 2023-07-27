import panel as pn
import param
from bokeh.models import NumberFormatter

formatters = {
    "payment": NumberFormatter(format="0,0", text_align="right"),
    "interest": NumberFormatter(format="0,0", text_align="right"),
    "capital repayment": NumberFormatter(format="0,0", text_align="right"),
    "balance": NumberFormatter(format="0,0", text_align="right"),
    "value":  NumberFormatter(format="0,0", text_align="right")
}

tabulator_settings = {
    "disabled": True,
    "formatters": formatters,
    "text_align": "right"
}

class PCard(pn.Card):

    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        self.collapsible = False
        self.objects.append(pn.VSpacer())
        self.height_policy = "fixed"
        self.height = 450


class Settings(pn.Param):

    def __init__(self, **params):
        params["widgets"] = params["object"].custom_widgets()
        super().__init__(**params)
        self.collapsible = False
        self.name = ""
        # self.sizing_mode = "stretch_both"


class SettingsCard(PCard):

    def __init__(self, *objs, **params):
        card_params = {key: value for key, value in params.items() if key != "mortgage"}
        card_params["title"] = "Mortgage Settings"
        super().__init__(*objs, **card_params)
        obj = [Settings(object=params["mortgage"])]
        self.objects = obj

class ScheduleCard(PCard):

    schedule_type = param.Selector(
        "lifetime summary",
        options=["full", "annual summary", "lifetime summary"],
        doc="Defines kind of schedule to show: full, annual summary or lifetime summary."
    )

    def __init__(self, *objs, **params):
        # remove extra params before calling super()
        card_params = {key: value for key, value in params.items() if key != "mortgage" and key != "schedule_type"}
        super().__init__(*objs, **card_params)
        tabulator = pn.widgets.Tabulator(
            params["mortgage"].repayment_schedule,
            **tabulator_settings
        )
        selector = self.param.schedule_type
        self.title = "Repayment schedule"
        self.objects = [selector, tabulator]
        self.collapsible = True
        self.collapsed = False
        self.height = 540
        self.height_policy = "min"

