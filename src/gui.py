import streamlit as st


def run_app():
    st.title("My First Web App")
    name = st.text_input("Enter your name:")
    if st.button("Greet"):
        st.write(f"Hello, {name}!")
    