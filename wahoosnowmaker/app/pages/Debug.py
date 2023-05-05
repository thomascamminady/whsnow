import shutil

import psutil
import streamlit as st

if __name__ == "__main__":
    stat = shutil.disk_usage("/")
    # Print disk usage statistics
    st.write(f"""Disk usage: {100*stat[2]/stat[0]:.2f}% free""")
    st.write(stat)

    # you can have the percentage of used RAM
    st.write(f"""RAM usage: {psutil.virtual_memory().percent:.2f}% used""")
    st.write(dict(psutil.virtual_memory()._asdict()))
