import streamlit as st

import glob as glob
from wahoosnowmaker.app.charts import chart


if __name__ == "__main__":
    query_parameters = st.experimental_get_query_params()
    if query_parameters is not None:
        if "folder" in query_parameters.keys():
            folder = query_parameters["folder"][0]
            chart(folder)
