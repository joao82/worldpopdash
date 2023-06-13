import i18n
from . import ids
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from typing import Protocol


class CountryDataSource(Protocol):
    @property
    def unique_countries(self) -> list[int]:
        ...

    @property
    def all_countries(self) -> list[int]:
        ...


def render(app: Dash, source: CountryDataSource) -> html.Div:
    @app.callback(
        Output(ids.COUNTRY_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_COUNTRIES_BUTTON, "n_clicks"),
    )
    def select_all_countries(_: int) -> list[str]:
        return source.unique_countries

    return html.Div(
        children=[
            html.H6(i18n.t("general.country")),
            dcc.Dropdown(
                id=ids.COUNTRY_DROPDOWN,
                options=[{"label": country, "value": country} for country in source.unique_countries],
                value=source.unique_countries,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["select All"],
                id=ids.SELECT_ALL_COUNTRIES_BUTTON,
                n_clicks=0,
            ),
        ]
    )
