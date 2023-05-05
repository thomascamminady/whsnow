import glob as glob

import numpy as np
import pandas as pd
import streamlit as st

from wahoosnowmaker.app.domain import domain as homepage
from wahoosnowmaker.app.markdown import centered_markdown_title
from wahoosnowmaker.app.saveload import (
    load_name,
    load_notes,
    save_name,
    save_notes,
)
from wahoosnowmaker.app.viz.chartsplotly import show_chart, show_map
from wahoosnowmaker.app.viz.styles import colorscales, map_styles
from wahoosnowmaker.parser.parse_folder import parse_folder


@st.cache_data  # should receive the files, not the folder
def cached_parse_folder(dataset_folder):
    return parse_folder(dataset_folder)


def show_analysis(df: pd.DataFrame, folder: str):
    st.write(
        centered_markdown_title("Wahoo .fit Inspector", homepage),
        unsafe_allow_html=True,
    )
    st.write(
        centered_markdown_title(load_name(folder), heading_level=2),
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Options", "Data", "Rename", "Download", "Notes"]
    )
    with tab1:
        default = int(np.argwhere(df.columns == "file")[0][0])
        color_by = st.selectbox("Color map trace", df.columns, default)
        if color_by is None:
            color_by = "file"
        default = int(np.argwhere(np.array(map_styles) == "carto-positron")[0][0])
        map_style = st.selectbox("Map style", map_styles, default)
        if map_style is None:
            map_style = "carto-positron"

        default = int(np.argwhere(np.array(colorscales) == "viridis")[0][0])
        colorscale = st.selectbox("Color scale", colorscales, default)
        if colorscale is None:
            colorscale = "viridis"

        options = list(set(df.columns) - {"Elapsed time (seconds)", "file"})
        default_options = [
            option
            for option in [
                "power",
                "speed",
                "altitude",
                "distance",
                "heartrate",
                "temperature",
            ]
            if option in options
        ]
        chart_options = st.multiselect("Charts", options, default_options)

    with tab2:
        st.write(df)
    with tab3:
        dataset_name = st.text_input("Rename session", load_name(folder))
        save_name(folder, dataset_name)

    with tab4:
        files = glob.glob(folder + "/*.fit")
        for file in files:
            centerleft, centerright = st.columns((4, 1))
            with centerleft:
                st.text(file)
            with centerright:
                with open(file, "rb") as f:
                    st.download_button(label="Download", data=f, file_name=file)
    with tab5:
        date = folder.split("/")[-1]
        dataset_notes = st.text_area(
            f"Notes for dataset created at {date}", value=load_notes(folder), height=300
        )
        save_notes(folder, dataset_notes)

    show_map(
        df, color_attribute=color_by, mapbox_style=map_style, color_scale=colorscale
    )

    show_chart(df, chart_options)


def app():
    query_parameters = st.experimental_get_query_params()
    if query_parameters is not None:
        if "folder" in query_parameters.keys():
            folder = query_parameters["folder"][0]

            uploaded_files = glob.glob(folder + "/*.fit")

            if uploaded_files is not None:
                if len(uploaded_files) > 0:
                    df = cached_parse_folder(folder).to_pandas()
                    show_analysis(df, folder)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Wahoo .FIT Inspector",
        initial_sidebar_state="collapsed",
        layout="wide",
    )
    app()
