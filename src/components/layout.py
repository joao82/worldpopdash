from dash import Dash, html
from . import dd_country, dd_year, bar_chart, line_chart, scatter_chart
from ..data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown_container",
                children=[dd_country.render(app, source), dd_year.render(app, source)],
            ),
            bar_chart.render(app, source),
            line_chart.render(app, source),
            scatter_chart.render(app, source),
        ],
    )
