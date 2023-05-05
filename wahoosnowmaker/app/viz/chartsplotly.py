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
    fig.update_traces(marker={"size": 4})
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    for i in range(len(df_long["type"].unique())):
        annotation = fig.layout.annotations[i].text  # type: ignore
        fig.layout[  # type: ignore
            f"""yaxis{"" if i==0 else str(i+1)}"""  # type: ignore
        ].title.text = annotation  # type: ignore
        fig.layout.annotations[i].text = ""  # type: ignore
    # fig.for_each_annotation(lambda a: a.update(font={"size": 20}))
    # fig.for_each_annotation(lambda a: a.update(textangle=0))
    fig.update_yaxes(matches=None)
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def get_center_lat_lon(df: pd.DataFrame, lat: str = "latitude", lon: str = "longitude"):
    min_lat, max_lat = df[lat].min(), df[lat].max()
    min_lon, max_lon = df[lon].min(), df[lon].max()
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    return {"lat": center_lat, "lon": center_lon}


@st.cache_data
def show_map(
    df: pd.DataFrame,
    color_attribute: str = "file",
    mapbox_style: str = "carto-positron",
    color_scale: str = "viridis",
) -> None:
    if color_attribute != "file":
        fig = px.scatter_mapbox(
            data_frame=df,
            lon="longitude",
            lat="latitude",
            color=color_attribute,
            color_continuous_scale=color_scale,
        )

        fig.add_traces(
            px.line_mapbox(df, lat="latitude", lon="longitude", color="file").data
        )

        # We first have to create the scatter mapbox component of the plot before
        # adding the line. Otherwise, we can't control the color scale.
        # But this does not look good because the line should be below the scatter points
        # So we now switch order.
        # first take the the second n/2 elements of the fig.data array and then the first n/2
        n = len(fig.data)
        fig.data = [fig.data[(i + n // 2) % n] for i in range(n)]
    else:
        fig = px.line_mapbox(df, lat="latitude", lon="longitude", color="file")

    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        height=800,
        mapbox={
            "style": mapbox_style,
            "center": go.layout.mapbox.Center(**get_center_lat_lon(df)),
            "pitch": 0,
            "zoom": 10,
        },
        mapbox_accesstoken=st.secrets["mapbox_api_key"],
    )
    fig.update_layout(
        coloraxis_colorbar={
            "len": 0.5,
            "xanchor": "right",
            "x": 1,
            "yanchor": "bottom",
            "y": 0.1,
            "thickness": 10,
        }
    )

    fig.update_geos(
        fitbounds="locations"
    )  # I don't think this is actually doing anything

    st.plotly_chart(fig, use_container_width=True)
