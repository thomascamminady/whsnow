import glob

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from wahoosnowmaker import logger
from wahoosnowmaker.parser.parse_folder import parse_folder


@st.cache_data
def show_chart(df):
    logger.info("Creating chart.")

    df_long = (
        pd.melt(
            df,
            id_vars=["Elapsed time (seconds)", "file"],
            value_name="value",
            var_name="type",
        )
        .dropna()
        .reset_index()
        .drop(columns=["index"])
    )
    fig = px.line(
        df_long,
        x="Elapsed time (seconds)",
        y="value",
        color="file",
        facet_row="type",
        height=3600,
        width=800,
    ).update_traces(mode="lines+markers")

    # Set the y-axis scale to be independent for each facet
    fig.update_yaxes(matches=None)
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data  # should receive the files, not the folder
def cached_parse_folder(dataset_folder):
    return parse_folder(dataset_folder)


def chart(dataset_folder: str):
    uploaded_files = glob.glob(dataset_folder + "/*.fit")
    # st.write(uploaded_files)

    if uploaded_files is not None:
        if len(uploaded_files) > 0:
            df = cached_parse_folder(dataset_folder).to_pandas()

            # fig = px.line_mapbox(
            #     df.to_pandas(),
            #     lat="latitude",
            #     lon="longitude",
            #     color="file",
            #     zoom=3,
            #     height=1000,
            # )

            fig = go.Figure()
            for grp, dfgrp in df.groupby("file"):
                fig.add_trace(
                    go.Scattermapbox(
                        mode="markers+lines",
                        lon=dfgrp["longitude"],
                        lat=dfgrp["latitude"],
                        marker={"size": 3},
                        text=dfgrp["file"],
                        name=grp,
                    )
                )

            # meanlon = np.nanmean(df.to_pandas()["longitude"])
            # meanlat = np.nanmean(df.to_pandas()["latitude"])
            min_lat, max_lat = df["latitude"].min(), df["latitude"].max()
            min_lon, max_lon = df["longitude"].min(), df["longitude"].max()
            center_lat = (min_lat + max_lat) / 2
            center_lon = (min_lon + max_lon) / 2
            max_bound = max(abs(max_lon - min_lon), abs(max_lat - min_lat)) * 111
            zoom = 11.5 - np.log(max_bound)

            fig.update_geos(fitbounds="locations")
            fig.update_layout(
                margin={"l": 0, "t": 0, "b": 0, "r": 0},
                mapbox={
                    "center": {"lon": center_lon, "lat": center_lat},
                    "style": "open-street-map",
                    # "style": "stamen-terrain",
                    # "center": {"lon": -20, "lat": -20},
                    "zoom": zoom,
                },
            )

            st.plotly_chart(fig, use_container_width=True)

            show_chart(df)
