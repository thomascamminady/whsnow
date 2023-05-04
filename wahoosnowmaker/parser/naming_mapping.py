from dataclasses import dataclass

import polars as pl


@dataclass
class ColumnName:
    name: str
    dtype: pl.PolarsDataType
    aliases: list[str]

    def to_dict(self) -> dict[str, str]:
        """Returns dictionary of names and aliases."""
        return {alias: self.name for alias in self.aliases}


Columns = [
    ColumnName("active", pl.Boolean, ["active"]),
    ColumnName("timestamp", pl.Datetime, ["timestamp"]),
    ColumnName("timestamp_fit", pl.Int64, ["timestamp_fit"]),
    ColumnName("second", pl.Int32, ["sec", "seconds"]),
    ColumnName("temperature", pl.Int16, ["temp_deg_c"]),
    ColumnName("distance", pl.Float64, ["dist_m", "dist"]),
    ColumnName("fractional_cadence", pl.Float64, ["fractional_cad_rpm"]),
    ColumnName("speed", pl.Float64, ["enhanced_spd_mps", "spd_mps", "enhanced_speed"]),
    ColumnName("heartrate", pl.Int16, ["hr_bpm", "heart_rate"]),
    ColumnName("cadence", pl.Int16, ["cad_rpm"]),
    ColumnName("latitude", pl.Float64, ["lat", "lat_deg", "position_lat"]),
    ColumnName("longitude", pl.Float64, ["lon", "long", "lon_deg", "position_long"]),
    ColumnName(
        "altitude", pl.Float64, ["enhanced_alt_m", "elevation", "enhanced_altitude"]
    ),
]
