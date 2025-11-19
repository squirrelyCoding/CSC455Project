import streamlit as st ##Import Streamlit
import random
import string
from passwordLogic import check_strength, generate_password, generate_strong_password as pl_generate_password

def is_logged_in():
    # Replace this logic with actual authentication check
    return st.session_state.get("logged_in", False)

# Replace with  actual strength check

def strength(password):
    result = check_strength(password)
    score = result.get("score", 0)
    rating = result.get("rating", "")
    suggestions = result.get("suggestions", [])

    if rating == "Strong":
        st.success(f"{rating} password — {score}%")
    elif rating == "Medium":
        st.info(f"{rating} password — {score}%")
    else:
        st.warning(f"{rating} password — {score}%")

    if suggestions:
        with st.expander("Suggestions"):
            for s in suggestions:
                st.write(f"- {s}")
 
def run_app():
    ##Page setup
    st.set_page_config(
        page_title="Password Manager",  
        page_icon=":closed_lock_with_key:",              
        layout="wide",             
        initial_sidebar_state="expanded"  
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f8ff; 
        }""", 
        unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="
            padding: 40px;
            background-color: #f0f2f6;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            color: #000000;
        ">
        <h2>Password Strength</h2>
        <p>Enter your potential password below</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([3, 1, 0.5])

    with col1:
        password = st.text_input("Password:", placeholder="Type your password here...")
        col2.markdown("<br><br>", unsafe_allow_html=True)
    with col2:
        if st.button("Check Strength"):
           st.session_state["saved_password"] = password #Saves password as variable for now until db made  
        col3.markdown("<br><br>", unsafe_allow_html=True)
    with col3:
        if st.button("Save Password", disabled= not is_logged_in()):
            st.session_state["saved_password"] = password #Saves password as variable for now until db made
            print(password)



  
