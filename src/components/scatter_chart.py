from . import ids
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import i18n
from ..data.source import DataSource
from ..data.loader import DataSchema
import pandas as pd


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.SCATTER_CHART, "children"),
        [Input(ids.COUNTRY_DROPDOWN, "value"), Input(ids.YEAR_DROPDOWN, "value")],
    )
    def update_scatter_chart(countries: list[str], years: list[int]) -> html.Div:
        df = source.filter(
            countries, years, ["Total Population", "Electric Power Consumption(kWH per capita)", "Country"]
        )

        if not df.shape[0]:
            return html.Div(i18n.t("general.no_data"), id=ids.SCATTER_CHART)

        fig = px.scatter(
            df,
            x=DataSchema.SP_POP_TOTL,
            y=DataSchema.EG_USE_ELEC_KH_PC,
            labels={
                "Country": i18n.t("general.country"),
                "Electric Power Consumption(kWH per capita)": i18n.t("general.electric"),
            },
            color="Country",
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.SCATTER_CHART)

    return html.Div(id=ids.SCATTER_CHART)
