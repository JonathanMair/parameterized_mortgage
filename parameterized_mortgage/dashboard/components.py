import panel as pn
from bokeh.models import NumberFormatter

class PCard(pn.Card):

    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        self.collapsible = False
        self.objects.append(pn.VSpacer())
        # self.sizing_mode = "stretch_both"


class Settings(pn.Param):

    def __init__(self, **params):
        params["widgets"] = params["object"].custom_widgets()
        super().__init__(**params)
        self.collapsible = False
        # self.sizing_mode = "stretch_both"


class SettingsCard(PCard):

    def __init__(self, *objs, **params):
        card_params = {key: value for key, value in params.items() if key != "mortgage"}
        card_params["title"] = "Mortgage Settings"
        super().__init__(*objs, **card_params)
        obj = [Settings(object=params["mortgage"])]
        self.objects = obj

class ScheduleCard(PCard):

    def __init__(self, *objs, **params):
        super().__init__(*objs, **params)
        tabulator = pn.widgets.Tabulator(
            params["mortgage"].repayment_schedule,
            disabled=True,
            formatters={
                "payment": NumberFormatter(format="0,0", text_align="right"),
                "interest": NumberFormatter(format="0,0", text_align="right"),
                "capital repayment": NumberFormatter(format="0,0", text_align="right"),
                "balance": NumberFormatter(format="0,0", text_align="right"),
            },
            text_align="right"
        )
        self.title = "Repayment schedule"
        self.objects=[tabulator]
