#import hash
import gui
import pandas as pd
import streamlit as st
from database.setup import initialize_database, get_connection


# Streamlit reruns the script whenever widgets update.
# We prevent multiple database initializations by storing a flag
# in st.session_state.
if "db_initialized" not in st.session_state:
    initialize_database()
    st.session_state["db_initialized"] = True

gui.run_app()


