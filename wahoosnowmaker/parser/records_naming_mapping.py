import polars as pl

from wahoosnowmaker.namespace import Namespace


class ColumnName:
    def __init__(self, name: str, dtype: pl.PolarsDataType, aliases: list[str]):
        self.name = name
        self.dtype = dtype
        self.aliases = aliases
        if self.name not in self.aliases:
            self.aliases.append(self.name)

    def to_dict(self) -> dict[str, str]:
        """Returns dictionary of names and aliases."""
        return {alias: self.name for alias in self.aliases}


Columns = [
    ColumnName(
        Namespace.column_active,
        pl.Boolean,
        ["active"],
    ),
    ColumnName(
        Namespace.column_timestamp,
        pl.Datetime,
        ["timestamp"],
    ),
    ColumnName(
        Namespace.column_timestamp_fit,
        pl.Int64,
        ["timestamp_fit"],
    ),
    ColumnName(
        Namespace.column_second,
        pl.Int32,
        ["sec", "seconds", "second"],
    ),
    ColumnName(
        Namespace.column_temperature,
        pl.Int16,
        ["temp_deg_c", "temperature"],
    ),
    ColumnName(
        Namespace.column_distance,
        pl.Float64,
        ["dist_m", "dist", "distance"],
    ),
    ColumnName(
        Namespace.column_fractional_cadence,
        pl.Float64,
        ["fractional_cad_rpm", "fractional_cadence"],
    ),
    ColumnName(
        Namespace.column_speed,
        pl.Float64,
        ["spd_mps", "speed"],
    ),
    ColumnName(
        Namespace.column_enhanced_speed,
        pl.Float64,
        ["enhanced_spd_mps", "enhanced_speed"],
    ),
    ColumnName(
        Namespace.column_heartrate,
        pl.Int16,
        ["hr_bpm", "heart_rate", "heartrate"],
    ),
    ColumnName(
        Namespace.column_cadence,
        pl.Int16,
        ["cad_rpm", "cadence"],
    ),
    ColumnName(
        Namespace.column_latitude,
        pl.Float64,
        ["lat", "lat_deg", "position_lat", "latitude"],
    ),
    ColumnName(
        Namespace.column_longitude,
        pl.Float64,
        ["lon", "long", "lon_deg", "position_long", "longitude"],
    ),
    ColumnName(
        Namespace.column_altitude,
        pl.Float64,
        ["elevation", "altitude"],
    ),
    ColumnName(
        Namespace.column_enhanced_altitude,
        pl.Float64,
        ["enhanced_alt_m", "enhanced_altitude"],
    ),
]
