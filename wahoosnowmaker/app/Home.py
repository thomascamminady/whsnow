"""Entry point to our Streamlit app."""
import glob
import os
import shutil
import webbrowser
from pathlib import Path

import streamlit as st

from wahoosnowmaker.app.create_dataset_folder import create_dataset_folder
from wahoosnowmaker.app.markdown import centered_markdown_title
from streamlit_javascript import st_javascript


if __name__ == "__main__":
    st.set_page_config(
        page_title="Upload new data.",
        initial_sidebar_state="collapsed",
        layout="wide",
    )

    # Upload new data
    st.markdown(centered_markdown_title("Create new dataset"), unsafe_allow_html=True)

    uploaded_files = st.file_uploader(" ", type=".fit", accept_multiple_files=True)
    if uploaded_files is not None:
        # create new location to store data
        folder = create_dataset_folder()

        # upload files
        for uploaded_file in uploaded_files:
            path = Path(folder, uploaded_file.name)
            if not os.path.exists(path):
                with open(path, mode="wb") as w:
                    w.write(uploaded_file.getvalue())
        # but also delete files
        for file in glob.glob(folder + "*.fit"):
            if os.path.basename(file) not in [f.name for f in uploaded_files]:
                os.remove(file)
        # redirect to analysis view
        if len(uploaded_files) > 0:
            url = f"""https://thomascamminady-whsnow-wahoosnowmakerapphome-avyfnr.streamlit.app/Analysis?folder={folder}"""
            webbrowser.open(url)

    # Inspect existing data
    st.markdown(centered_markdown_title("Inspect old dataset"), unsafe_allow_html=True)
    existing_folders = glob.glob("data/*")
    existing_folders.sort(reverse=True)
    for _i, folder in enumerate(existing_folders):
        # print(folder, len(glob.glob(folder + "/*.fit")))
        if (n := len(glob.glob(folder + "/*.fit"))) > 0:
            url = f"""https://thomascamminady-whsnow-wahoosnowmakerapphome-avyfnr.streamlit.app/Analysis?folder={folder}"""

            st.write(
                f"""[{folder.split("/")[-1].upper()}]({url}) (Dataset with {n} file{"" if n==1 else "s"}.)"""
            )

        else:
            shutil.rmtree(folder)
