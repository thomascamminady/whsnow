import glob
import os
from pathlib import Path

import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from streamlit_folium import st_folium

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
            df = cached_parse_folder(dataset_folder)

            fig = px.line_mapbox(
                df.to_pandas(),
                lat="latitude",
                lon="longitude",
                color="file",
                zoom=3,
                height=1000,
            )

            fig.update_layout(
                mapbox_style="stamen-terrain",
                mapbox_zoom=10,
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
            )

            st.plotly_chart(fig, use_container_width=True)

            show_chart(df.to_pandas())
