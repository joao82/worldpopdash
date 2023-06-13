import pandas as pd
import numpy as np
import requests
import asyncio
import logging
from contextlib import contextmanager

BASE_URL = "http://api.worldbank.org/v2/"

INDICATOR_CODES = [
    "SP.POP.TOTL",
    "SP.POP.TOTL.FE.IN",
    "SP.POP.TOTL.MA.IN",
    "SL.IND.EMPL.ZS",
    "SL.AGR.EMPL.ZS",
    "SL.UEM.TOTL.ZS",
    "NY.GDP.MKTP.CD",
    "NY.ADJ.NNTY.PC.KD.ZG",
    "NY.GSR.NFCY.CD",
    "EG.USE.ELEC.KH.PC",
    "EG.FEC.RNEW.ZS",
    "EG.USE.COMM.FO.ZS",
]

COUNTRY_LIST = ["USA", "India", "China", "Japan", "Canada", "Great Britain", "South Africa"]

featureMap = {
    "SP.POP.TOTL": "Total Population",
    "SP.POP.TOTL.FE.IN": "Female Population",
    "SP.POP.TOTL.MA.IN": "Male Population",
    "SL.IND.EMPL.ZS": "Employment in Industry(%)",
    "SL.AGR.EMPL.ZS": "Employment in Agriculture(%)",
    "SL.UEM.TOTL.ZS": "Unemployment(%)",
    "NY.GDP.MKTP.CD": "GDP in USD",
    "NY.ADJ.NNTY.PC.KD.ZG": "National Income per Capita",
    "NY.GSR.NFCY.CD": "Net income from Abroad",
    "EG.USE.ELEC.KH.PC": "Electric Power Consumption(kWH per capita)",
    "EG.FEC.RNEW.ZS": "Renewable Energy Consumption (%)",
    "EG.USE.COMM.FO.ZS": "Fossil Fuel Consumption (%)",
}

countryMap = {
    "US": "USA",
    "IN": "India",
    "CN": "China",
    "JP": "Japan",
    "CA": "Canada",
    "GB": "Great Britain",
    "ZA": "South Africa",
}

params = dict()
params["format"] = "json"
params["per_page"] = "100"
params["date"] = "1960:2018"

JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]


def send_requests(url: str, dataList: list[JSONObject]) -> None:
    print("Sending request to: " + url)
    response = requests.get(url, params=params)
    if response.status_code == 200 and ("message" not in response.json()[0].keys()):
        indicatorVals = []
        if len(response.json()) > 1:
            for obj in response.json()[1]:
                if obj["value"] is "" or obj["value"] is None:
                    indicatorVals.append(None)
                else:
                    indicatorVals.append(float(obj["value"]))
            dataList.append(indicatorVals)
    else:
        print("Error in Loading the data. Status Code: " + str(response.status_code))


async def loadJSONData(country_code: str) -> list[JSONObject]:
    dataList = []

    for indicator in INDICATOR_CODES:
        url = BASE_URL + "countries/" + country_code.lower() + "/indicators/" + indicator
        await asyncio.to_thread(send_requests, url, dataList)
    dataList.append([year for year in range(2018, 1959, -1)])
    return dataList


async def getCountrywiseDF(country_code: str) -> pd.DataFrame:
    col_list = list(featureMap.values())
    col_list.append("Year")

    print("------Loading data for: " + countryMap[country_code] + "---------")

    dataList = await loadJSONData(country_code)
    df = pd.DataFrame(np.column_stack(dataList), columns=col_list)
    df["Country"] = countryMap[country_code]

    return df


def remove_missing_features(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        print("No DataFrame received!")
        return
    df_cp = df.copy()

    print("Removing missing features for: " + df_cp.iloc[0]["Country"])

    n_missing_vals = df.isnull().sum()
    n_missing_index_list = list(n_missing_vals.index)
    missing_percentage = n_missing_vals[n_missing_vals != 0] / df.shape[0] * 100
    cols_to_trim = []
    for i, val in enumerate(missing_percentage):
        if val > 75:
            cols_to_trim.append(n_missing_index_list[i])
    if len(cols_to_trim) > 0:
        df_cp = df_cp.drop(columns=cols_to_trim)
        print("Dropped Columns:" + str(cols_to_trim))
    else:
        print("No columns dropped")
    return df_cp


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        print("No DataFrame received")
        return
    df_cp = df.copy()

    print("Filling missing features for: " + df_cp.iloc[0]["Country"])
    cols_list = list(df_cp.columns)
    cols_list.pop()
    df_cp.fillna(value=np.nan, inplace=True)
    for col in cols_list:
        df_cp[col].fillna((df_cp[col].mean()), inplace=True)
    print("Filling missing values completed")
    return df_cp


@contextmanager
def file_manager(filename: str, mode: str) -> None:
    try:
        logging.info("Opening the file")
        file = open(filename, mode, encoding="utf8")
        yield file
    finally:
        logging.info("Closing the file")
        file.close()


def write_data(list_df: list[pd.DataFrame]) -> None:
    assert len(list(countryMap.keys())) == len(list_df)

    for country_name, df_data in zip(COUNTRY_LIST, list_df):
        print("Writing data for: " + country_name)
        file_name = "data/" + country_name + ".csv"
        logging.basicConfig(level=logging.ERROR)

        with file_manager(file_name, "w") as file:
            df_data.to_csv(file, index=False)
            print("Successfully created: " + file_name)


async def get_data_from_api() -> None:
    world_population = await asyncio.gather(*[getCountrywiseDF(country_code) for country_code in countryMap.keys()])
    US_df, IN_df, CN_df, JP_df, CA_df, GB_df, ZA_df = map(lambda x: world_population[x], range(7))
    print("Data Loading Completed")

    list_df = [US_df.copy(), IN_df.copy(), CN_df.copy(), JP_df.copy(), CA_df.copy(), GB_df.copy(), ZA_df.copy()]
    list_df = list(map(remove_missing_features, list_df))
    list_df = list(map(fill_missing_values, list_df))

    write_data(list_df)
