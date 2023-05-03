import glob

import polars as pl

from wahoosnowmaker import logger
from wahoosnowmaker.parser.fitparser import FitParser
from wahoosnowmaker.parser.fitparser import GarminFitSDKParser as Parser
from wahoosnowmaker.parser.pipes import (
    assign_file,
    compute_elapsed_seconds,
    convert_semicircles_to_lat_lon,
    drop_columns_all_nans,
    make_column_names_consistent,
    parse_timestamp,
)


def parse_folder(
    session_folder: str,
    fitparser: FitParser | None = None,
    fit_ending: str = "/*.fit",
) -> pl.DataFrame:
    df_list = []
    if fitparser is None:
        fitparser = Parser()
    for fitfile in glob.glob(session_folder + fit_ending):
        try:
            df_list.append(
                fitparser.fit_to_records_df(fitfile)
                .collect()
                .pipe(assign_file, file=fitfile)
                .pipe(drop_columns_all_nans)
                .pipe(make_column_names_consistent)
                .pipe(parse_timestamp)
                .pipe(convert_semicircles_to_lat_lon)
                .pipe(compute_elapsed_seconds)
            )
        except Exception as e:
            logger.error(f"Could not parse {fitfile}: {e}")

    if len(df_list) > 0:
        return pl.concat(df_list, how="diagonal")
    else:
        return pl.DataFrame()
