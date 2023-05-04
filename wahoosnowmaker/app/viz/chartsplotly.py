import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from wahoosnowmaker import logger


@st.cache_data
def show_chart(df: pd.DataFrame) -> None:
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
    ideal_order = [
        "speed",
        "altitude",
        "heartrate",
        "cadence",
        "temperature",
        "distance",
    ]
    custom_order = []
    # take everything from the ideal order that exists in the dataframe
    for item in ideal_order:
        if item in df.columns:
            custom_order.append(item)
    # take everything from the dataframe that is not yet in the custom order
    for item in df.columns:
        if item in ["Elapsed time (seconds)", "file"]:
            continue
        if item not in custom_order:
            custom_order.append(item)

    fig = px.line(
        df_long,
        x="Elapsed time (seconds)",
        y="value",
        color="file",
        facet_row="type",
        height=4000,
        facet_row_spacing=0.01,
        width=800,
        category_orders={"type": custom_order},
    )

    fig.update_traces(mode="lines+markers")
    fig.for_each_annotation(lambda a: a.update(text=" " + a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(font={"size": 20}))
    fig.for_each_annotation(lambda a: a.update(textangle=0))
    fig.update_yaxes(matches=None)
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def show_map(df: pd.DataFrame) -> None:
    fig = go.Figure()
    for grp, dfgrp in df.groupby("file"):
        fig.add_trace(
            go.Scattermapbox(
                mode="markers+lines",
                lon=dfgrp["longitude"],
                lat=dfgrp["latitude"],
                marker={"size": 8},
                name=grp,
            )
        )

    min_lat, max_lat = df["latitude"].min(), df["latitude"].max()
    center_lat = (min_lat + max_lat) / 2
    min_lon, max_lon = df["longitude"].min(), df["longitude"].max()
    center_lon = (min_lon + max_lon) / 2
    # free_styles = [
    #     "open-street-map",
    #     "carto-positron",
    #     "carto-darkmatter",
    #     "stamen-terrain",
    #     "stamen-toner",
    #     "stamen-watercolor",
    # ]
    # mapbox_styles = [
    #     "basic",
    #     "streets",
    #     "outdoors",
    #     "light",
    #     "dark",
    #     "satellite",
    #     "satellite-streets",
    # ]

    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        height=800,
        mapbox={
            "style": "carto-positron",
            "center": go.layout.mapbox.Center(lat=center_lat, lon=center_lon),
            "pitch": 0,
            "zoom": 10,
        },
        mapbox_accesstoken=st.secrets["mapbox_api_key"],
    )

    fig.update_geos(fitbounds="locations")

    st.plotly_chart(fig, use_container_width=True)
