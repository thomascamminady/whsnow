"""Entry point to our Streamlit app."""
import glob
import os
import shutil
from pathlib import Path

import streamlit as st

from wahoosnowmaker import logger
from wahoosnowmaker.app.domain import domain as home
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
    # Very crude way to redirect to base page without parameters
    st.experimental_set_query_params()

    def centered_markdown_title(text: str) -> str:
        return f"""<h1 style='text-align: center; color: grey;'>{text}</h1>"""

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
            url = f"""{home}/Analysis?folder={folder}"""
            # webbrowser.open(url)

    # Inspect existing data
    st.markdown(centered_markdown_title("Inspect old dataset"), unsafe_allow_html=True)
    existing_folders = glob.glob("data/*")
    existing_folders.sort(reverse=True)
    for _i, folder in enumerate(existing_folders):
        # print(folder, len(glob.glob(folder + "/*.fit")))

        files = glob.glob(folder + "/*.fit")
        if (n := len(files)) > 0:
            _, center, right = st.columns(3)
            with center:
                url = f"""{home}/Analysis?folder={folder}"""

                st.write(
                    f"""[{folder.split("/")[-1].upper()}]({url}) (Dataset with {n} file{"" if n==1 else "s"}.)"""
                )
                with st.expander(".FIT files"):
                    for file in files:
                        centerleft, centerright = st.columns(2)
                        with centerleft:
                            st.text(file)
                        with centerright:
                            with open(file, "rb") as f:
                                st.download_button(
                                    label="Download",
                                    data=f,
                                    file_name=file,
                                    # mime="image/png"
                                )

            with right:
                button_delete = st.button("Delete", key=f"Delete {_i}")
                if button_delete:
                    shutil.rmtree(folder)
                    st.experimental_rerun()

            st.divider()

        else:
            try:
                shutil.rmtree(folder)
            except Exception as e:
                logger.warning(e)


st.set_page_config(
    page_title="Upload new data.",
    initial_sidebar_state="collapsed",
    layout="wide",
)
if check_password():
    app()
