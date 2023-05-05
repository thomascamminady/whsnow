import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def get_center_lat_lon(df: pd.DataFrame, lat: str = "latitude", lon: str = "longitude"):
    min_lat, max_lat = df[lat].min(), df[lat].max()
    min_lon, max_lon = df[lon].min(), df[lon].max()
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    return {"lat": center_lat, "lon": center_lon}


# See: https://community.plotly.com/t/dynamic-zoom-for-mapbox/32658/10
@st.cache_data
def get_zoom_level(longitudes=None, latitudes=None, fudge: float = 1):
    """
    Basic framework adopted from Krichardson.

    Under the following thread:
    https://community.plotly.com/t/dynamic-zoom-for-mapbox/32658/7
    THIS IS A TEMPORARY SOLUTION UNTIL THE DASH TEAM IMPLEMENTS DYNAMIC ZOOM
    in their plotly-functions associated with mapbox, such as go.Densitymapbox() etc.
    Returns the appropriate zoom-level for these plotly-mapbox-graphics along with
    the center coordinate tuple of all provided coordinate tuples.
    """
    # Check whether both latitudes and longitudes have been passed,
    # or if the list lenghts don't match
    if (latitudes is None or longitudes is None) or (len(latitudes) != len(longitudes)):
        # Otherwise, return the default values of 0 zoom and the coordinate origin as center point
        return 0, (0, 0)

    # Get the boundary-box
    b_box = {}
    b_box["height"] = latitudes.max() - latitudes.min()
    b_box["width"] = longitudes.max() - longitudes.min()
    b_box["center"] = (np.mean(longitudes), np.mean(latitudes))

    # get the area of the bounding box in order to calculate a zoom-level
    area = b_box["height"] * b_box["width"]

    # * 1D-linear interpolation with numpy:
    # - Pass the area as the only x-value and not as a list, in order to return a scalar as well
    # - The x-points "xp" should be in parts in comparable order of magnitude of the given area
    # - The zoom-levels are adapted to the areas, i.e. start with the smallest area possible of 0
    # which leads to the highest possible zoom value 20, and so forth decreasing with increasing areas
    # as these variables are antiproportional
    zoom = np.interp(
        x=fudge * area,
        xp=[0, 5**-10, 4**-10, 3**-10, 2**-10, 1**-10, 1**-5],
        fp=[20, 15, 14, 13, 12, 7, 5],
    )

    return zoom
