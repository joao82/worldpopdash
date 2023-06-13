from . import ids
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import i18n
from ..data.source import DataSource
from ..data.loader import DataSchema


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [Input(ids.COUNTRY_DROPDOWN, "value"), Input(ids.YEAR_DROPDOWN, "value")],
    )
    def update_bar_chart(countries: list[str], years: list[int]) -> html.Div:
        df = source.filter(countries, years, ["Total Population", "Country", "Year"])

        if not df.shape[0]:
            return html.Div(i18n.t("general.no_data"), id=ids.BAR_CHART)

        fig = px.bar(
            df,
            x=DataSchema.COUNTRY,
            y=DataSchema.SP_POP_TOTL,
            color="Year",
            labels={
                "Country": i18n.t("general.country"),
                "Total Population": i18n.t("general.population"),
            },
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
