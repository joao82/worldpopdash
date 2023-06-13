import pandas as pd
import i18n


class DataSchema:
    SP_POP_TOTL = "Total Population"
    SP_POP_TOTL_FE_IN = "Female Population"
    SP_POP_TOTL_MA_IN = "Male Population"
    SL_IND_EMPL_ZS = "Employment in Industry(%)"
    SL_AGR_EMPL_ZS = "Employment in Agriculture(%)"
    SL_UEM_TOTL_ZS = "Unemployment(%)"
    NY_GDP_MKTP_CD = "GDP in USD"
    NY_ADJ_NNTY_PC_KD_ZG = "National Income per Capita"
    NY_GSR_NFCY_CD = "Net income from Abroad"
    EG_USE_ELEC_KH_PC = "Electric Power Consumption(kWH per capita)"
    EG_FEC_RNEW_ZS = "Renewable Energy Consumption (%)"
    EG_USE_COMM_FO_ZS = "Fossil Fuel Consumption (%)"
    YEAR = "Year"
    COUNTRY = "Country"


def translate_countries(df: pd.DataFrame) -> pd.DataFrame:
    def translate(country: str) -> str:
        return i18n.t(f"country.{country}")

    df[DataSchema.COUNTRY] = df[DataSchema.COUNTRY].apply(translate)
    return df


def load_pop_data(path: str, locale: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    translate_countries(data)
    return data


def load_data(locale: str) -> pd.DataFrame:
    df_us = load_pop_data("data/USA.csv", locale)
    df_in = load_pop_data("data/India.csv", locale)
    df_cn = load_pop_data("data/China.csv", locale)
    df_jp = load_pop_data("data/Japan.csv", locale)
    df_ca = load_pop_data("data/Canada.csv", locale)
    df_gb = load_pop_data("data/Great Britain.csv", locale)
    df_za = load_pop_data("data/South Africa.csv", locale)
    print("Successfully read all the files")

    list_cleaned_df = [df_us, df_in, df_cn, df_jp, df_ca, df_gb, df_za]

    ## CONCATENATE
    combined_df = pd.concat(list_cleaned_df, sort=False)
    return combined_df
