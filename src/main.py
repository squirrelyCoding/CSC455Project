#import hash
import gui
import pandas as pd
import gui
import streamlit as st
from database.setup import initialize_database, get_connection

#To run go to terminal and write streamlit run main.py
gui.run_app()

#creates the database tables if they are missing
initialize_database()

#hash.HashPassword()
