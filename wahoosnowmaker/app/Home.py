"""Entry point to our Streamlit app."""
import glob
import os
import shutil
from pathlib import Path

import streamlit as st

from wahoosnowmaker import logger
from wahoosnowmaker.app.domain import domain as home
from wahoosnowmaker.app.markdown import centered_markdown_title
from wahoosnowmaker.app.saveload import load_name
from wahoosnowmaker.utils.create_dataset_folder import create_dataset_folder


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def app():
    st.write(centered_markdown_title("Wahoo .FIT Inspector"), unsafe_allow_html=True)

    # Very crude way to redirect to base page without parameters
    st.experimental_set_query_params()

    # Upload new data
    st.markdown(
        centered_markdown_title("Create new dataset", heading_level=2),
        unsafe_allow_html=True,
    )
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
            url = f"""{home}/Analysis?folder={folder}"""
            # webbrowser.open(url)

    # Inspect existing data
    st.markdown(
        centered_markdown_title("Inspect old dataset", heading_level=2),
        unsafe_allow_html=True,
    )
    existing_folders = glob.glob("data/*")
    existing_folders.sort(reverse=True)
    for _i, folder in enumerate(existing_folders):
        # print(folder, len(glob.glob(folder + "/*.fit")))

        files = glob.glob(folder + "/*.fit")
        if (len(files)) > 0:
            url = f"""{home}/Analysis?folder={folder}"""

            left, right = st.columns((4, 1))
            with left:
                name = load_name(folder)
                st.write(f"""#### [{name}]({url})""")
            with right:
                button_delete = st.button("Delete", key=f"Delete {_i}")
                if button_delete:
                    shutil.rmtree(folder)
                    st.experimental_rerun()
            # with st.expander(f"""See {n} .fit file{"" if n==1 else "s"}"""):
            #     for file in files:
            #         centerleft, centerright = st.columns((4, 1))
            #         with centerleft:
            #             st.text(file)
            #         with centerright:
            #             with open(file, "rb") as f:
            #                 st.download_button(
            #                     label="Download",
            #                     data=f,
            #                     file_name=file,
            #                     # mime="image/png"
            #                 )

        else:
            try:
                shutil.rmtree(folder)
            except Exception as e:
                logger.warning(e)


st.set_page_config(
    page_title="Wahoo .FIT Inspector",
    initial_sidebar_state="collapsed",
    layout="centered",
)
if check_password():
    app()
