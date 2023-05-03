import warnings
from abc import ABC, abstractmethod

import polars as pl

from wahoosnowmaker.utils.logger import logger

with warnings.catch_warnings():  # Garmin has a SyntaxWarning in the decoder.py file
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    from garmin_fit_sdk import Decoder, Stream


class FitParsingError(Exception):
    def __init__(self, fit_file: str, message: str):
        self.fit_file = fit_file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[FIT Parsing] Error parsing {self.fit_file}: {self.message}"


class FitParser(ABC):
    def fit_to_records_df(self, fit_file: str) -> pl.LazyFrame:
        try:
            return self._fit_to_records_df(fit_file)
        except Exception as e:
            logger.error(f"[FIT Parsing] Error parsing {fit_file}: {e}")
            raise FitParsingError(fit_file, str(e))

    @abstractmethod
    def _fit_to_records_df(self, fit_file: str) -> pl.LazyFrame:
        pass


class GarminFitSDKParser(FitParser):
    def _fit_to_records_df(self, fit_file: str) -> pl.LazyFrame:
        stream = Stream.from_file(fit_file)
        decoder = Decoder(stream)

        messages, errors = decoder.read(
            apply_scale_and_offset=True,
            convert_datetimes_to_dates=True,
            convert_types_to_strings=True,
            expand_sub_fields=True,
            expand_components=True,
            merge_heart_rates=True,
            mesg_listener=None,
        )
        # logger.info(messages)
        records = messages["record_mesgs"]

        # Convert integer keys to string keys
        records = [
            {
                str(key): value
                for key, value in record.items()
                if not isinstance(value, dict)
            }
            for record in records
        ]

        # pl.DataFrame(records).to_pandas().to_csv(fit_file + ".csv")
        return pl.DataFrame(records).lazy()
