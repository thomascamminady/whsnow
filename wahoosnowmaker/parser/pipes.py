import os

import polars as pl

from wahoosnowmaker.namespace import Namespace
from wahoosnowmaker.parser.records_naming_mapping import Columns


def drop_columns_all_nans(_df: pl.DataFrame) -> pl.DataFrame:
    return _df.drop([col.name for col in _df.select(pl.all().is_null()) if col.all()])


def assign_file(_df: pl.DataFrame, file: str):
    return _df.with_columns(pl.lit(os.path.basename(file)).alias("file"))


def parse_timestamp(
    _df: pl.DataFrame,
    column: str = Namespace.column_timestamp,
    format: str = "%Y-%m-%dT%H:%M:%S.%fZ",
) -> pl.DataFrame:
    if _df[column].dtype == pl.Datetime:
        return _df
    else:
        return _df.with_columns(
            [pl.col(column).str.strptime(pl.Datetime, format=format)]
        )


def convert_semicircles_to_lat_lon(_df: pl.DataFrame):
    return _df.with_columns(
        [
            pl.col(Namespace.column_latitude) * 180 / 2**31,
            pl.col(Namespace.column_longitude) * 180 / 2**31,
        ]
    )


def compute_elapsed_seconds(_df: pl.DataFrame):
    return _df.with_columns(
        (pl.col(Namespace.column_timestamp) - pl.col(Namespace.column_timestamp).min())
        .alias(Namespace.column_elapsed_time)
        .dt.seconds()
    )


def make_column_names_consistent(_df: pl.DataFrame):
    mapping = {}
    for column in Columns:
        for key, value in column.to_dict().items():
            if key in _df.columns:
                mapping[key] = value
    if len(mapping) > 0:
        return _df.rename(mapping=mapping)
    else:
        return _df
