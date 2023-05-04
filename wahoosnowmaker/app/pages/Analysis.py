import glob as glob

import streamlit as st

from wahoosnowmaker.app.domain import domain as homepage
from wahoosnowmaker.app.viz.chartsplotly import chart

if __name__ == "__main__":
    st.set_page_config(
        page_title="Analysis.",
        initial_sidebar_state="collapsed",
        layout="wide",
    )
    st.write(f"### [Home]({homepage})")
    query_parameters = st.experimental_get_query_params()
    if query_parameters is not None:
        if "folder" in query_parameters.keys():
            folder = query_parameters["folder"][0]

            chart(folder)
