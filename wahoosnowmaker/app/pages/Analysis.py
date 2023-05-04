import glob as glob

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
        centered_markdown_title(load_name(folder), homepage),
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Notes", "Data", "Rename"])
    with tab1:
        dataset_notes = st.text_area(" ", value=load_notes(folder), height=300)
        save_notes(folder, dataset_notes)
        # st.button("Save notes")
    with tab2:
        st.write(df)
    with tab3:
        dataset_name = st.text_input(" ", load_name(folder))
        save_name(folder, dataset_name)

    show_map(df)
    show_chart(df)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Analysis.",
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
