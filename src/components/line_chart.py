from . import ids
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import i18n
from ..data.source import DataSource
from ..data.loader import DataSchema


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, "children"),
        [Input(ids.COUNTRY_DROPDOWN, "value"), Input(ids.YEAR_DROPDOWN, "value")],
    )
    def update_line_chart(countries: list[str], years: list[int]) -> html.Div:
        df = source.filter(countries, years, columns=["Country", "Year", "GDP in USD"])

        if not df.shape[0]:
            return html.Div(i18n.t("general.no_data"), id=ids.LINE_CHART)

        fig = px.line(
            df,
            x=DataSchema.YEAR,
            y=DataSchema.NY_GDP_MKTP_CD,
            labels={
                "Country": i18n.t("general.country"),
                "GDP in USD": i18n.t("general.gdp"),
            },
            color="Country",
            text="Year",
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
