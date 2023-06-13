from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids
import i18n
from typing import Protocol


class YearsDataSource(Protocol):
    @property
    def unique_years(self) -> list[int]:
        ...

    @property
    def all_years(self) -> list[int]:
        ...


def render(app: Dash, source: YearsDataSource) -> html.Div:
    return html.Div(
        children=[
            html.H6(i18n.t("general.years")),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in source.all_years],
                value=source.unique_years[-15:],
                multi=True,
            ),
        ]
    )
