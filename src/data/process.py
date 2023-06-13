import pandas as pd
from .loader import load_pop_data


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
