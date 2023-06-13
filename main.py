import os
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from src.components.layout import create_layout
from src.data.loader import load_data
from src.data.api import get_data_from_api
from src.data.source import DataSource
import i18n
import asyncio

DATA_PATH = "./data"
LOCALE = "pt"


async def main() -> None:
    i18n.set("locale", LOCALE)
    i18n.load_path.append("./locales")

    if not os.listdir(DATA_PATH):
        await get_data_from_api()
    else:
        print("Data file already exists. Skipping download.")

    data = load_data(LOCALE)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, DataSource(data))
    app.run_server(debug=True)


if __name__ == "__main__":
    asyncio.run(main())
