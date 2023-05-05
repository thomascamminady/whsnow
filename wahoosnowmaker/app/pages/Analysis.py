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
from wahoosnowmaker.app.viz.map_styles import styles
from wahoosnowmaker.parser.parse_folder import parse_folder


@st.cache_data  # should receive the files, not the folder
def cached_parse_folder(dataset_folder):
    return parse_folder(dataset_folder)


def app(df: pd.DataFrame, folder: str):
    st.write(
        centered_markdown_title("Wahoo .fit Inspector", homepage),
        unsafe_allow_html=True,
    )
    st.write(
        centered_markdown_title(load_name(folder), heading_level=2),
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Notes", "Data", "Rename", "Download"])
    with tab1:
        dataset_notes = st.text_area(" ", value=load_notes(folder), height=300)
        save_notes(folder, dataset_notes)
    with tab2:
        st.write(df)
    with tab3:
        dataset_name = st.text_input(" ", load_name(folder))
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

    col1, col2 = st.columns(2)
    with col1:
        default = int(np.argwhere(df.columns == "file")[0][0])
        color_by = st.selectbox("Color map trace", df.columns, default)
        if color_by is None:
            color_by = "file"
    with col2:
        default = int(np.argwhere(np.array(styles) == "carto-positron")[0][0])
        map_style = st.selectbox("Map style", styles, default)
        if map_style is None:
            map_style = "carto-positron"
    show_map(df, color_attribute=color_by, mapbox_style=map_style)
    show_chart(df)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Wahoo .FIT Inspector",
        initial_sidebar_state="collapsed",
        layout="wide",
    )
    query_parameters = st.experimental_get_query_params()
    if query_parameters is not None:
        if "folder" in query_parameters.keys():
            folder = query_parameters["folder"][0]

            uploaded_files = glob.glob(folder + "/*.fit")

            if uploaded_files is not None:
                if len(uploaded_files) > 0:
                    df = cached_parse_folder(folder).to_pandas()
                    app(df, folder)
