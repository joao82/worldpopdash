from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from .loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self, countries: Optional[list[str]], years: Optional[list[int]], columns: Optional[list[str]]
    ) -> DataSource:
        filtered_data = self._data[
            self._data[DataSchema.YEAR].isin(years) & self._data[DataSchema.COUNTRY].isin(countries)
        ]
        df = filtered_data[columns]
        return df

    @property
    def all_years(self) -> list[int]:
        return self._data[DataSchema.YEAR].tolist()

    @property
    def last_10_years(self) -> list[int]:
        return self._data[DataSchema.YEAR].unique().tolist()[:10]

    @property
    def unique_years(self) -> list[int]:
        return sorted(set(self.all_years), key=int)

    @property
    def all_countries(self) -> list[str]:
        return self._data[DataSchema.COUNTRY].tolist()

    @property
    def unique_countries(self) -> list[str]:
        return sorted(set(self.all_countries), key=str)

    @property
    def all_population(self) -> list[str]:
        return self._data[DataSchema.SP_POP_TOTL].tolist()

    @property
    def all_gdp(self) -> list[str]:
        return self._data[DataSchema.NY_GDP_MKTP_CD].tolist()
