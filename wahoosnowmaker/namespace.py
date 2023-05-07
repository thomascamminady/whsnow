from dataclasses import dataclass

import plotly.express as px


@dataclass
class Namespace:
    app_name = "Wahoo .fit Inspector"
    domain = """https://wahoofit.streamlit.app"""
    # domain = """http://localhost:8501"""

    name_file_name = "name.txt"
    notes_file_name = "notes.txt"
    column_elapsed_time = "Elapsed time [s]"
    column_second = "Second [s]"
    column_power = "Power [W]"
    column_speed = "Speed [mps]"
    column_altitude = "Altitude [m]"
    column_distance = "Distance [m]"
    column_heartrate = "Heartrate [bpm]"
    column_temperature = "Temperature [°C]"
    column_cadence = "Cadence [spm]"
    column_latitude = "Latitude [°]"
    column_longitude = "Longitude [°]"
    column_timestamp_fit = "Timestamp fit"
    column_timestamp = "Timestamp"
    column_active = "Active"
    column_fractional_cadence = "Fractional Cadence"
    standard_charts_to_display = [
        column_power,
        column_speed,
        column_cadence,
        column_altitude,
        column_distance,
        column_heartrate,
        column_temperature,
    ]
    default_map_style = "carto-positron"
    default_color_by = "file"
    default_colorscale = "viridis"

    streamlit_layout = "centered"
    streamlit_initial_sidebar_state = "collapsed"
    free_styles = [
        "open-street-map",
        "carto-positron",
        "carto-darkmatter",
        "stamen-terrain",
        "stamen-toner",
        "stamen-watercolor",
    ]
    mapbox_styles = [
        "basic",
        "streets",
        "outdoors",
        "light",
        "dark",
        "satellite",
        "satellite-streets",
    ]

    map_styles = free_styles + mapbox_styles

    colorscales = px.colors.named_colorscales()


DefaultNamespace = Namespace()
