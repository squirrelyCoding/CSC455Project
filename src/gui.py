import streamlit as st ##Import Streamlit
import random
import string
from passwordLogic import check_strength, generate_password, generate_strong_password as pl_generate_password


def is_user():
    return st.session_state.get("user_true", False) ##Returns user as false default


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
            page_title="Password Strength Manager",  
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
    

    if "user_true" not in st.session_state:
        st.session_state["user_true"] = False
    if "saved_password" not in st.session_state:
        st.session_state["saved_password"] = ""
    if "password_input" not in st.session_state:
        st.session_state["password_input"] = ""

    # Sidebar login
    user_id = st.sidebar.text_input("Login", placeholder="User Id")
    if st.sidebar.button("Login"):
        if user_id:
            st.session_state["user_true"] = True
            st.sidebar.success(f"Logged in as {user_id}")
        else:
            st.sidebar.error("Enter a User Id to login")

    page = st.sidebar.selectbox("Page Selection", ["Password Strength", "Saved Passwords"])

    if page == "Password Strength":
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
        col1, col2, col3 = st.columns([3,1,0.5])

        with col1:
            password = st.text_input("Password:", value=st.session_state["password_input"])
            st.session_state["password_input"] = password

        with col2:
            st.markdown("<br></br>",  unsafe_allow_html=True)
            if st.button("Generate"):
                new_pass = generate_password()
                st.session_state["password_input"] = new_pass
                password = new_pass

        with col3:
            st.markdown("<br></br>",  unsafe_allow_html=True)
            if st.button("Save Password", disabled=not is_user()):
                st.session_state["saved_password"] = st.session_state["password_input"]
                st.success("Password saved!")

        if st.session_state["password_input"]:
            strength(st.session_state["password_input"])

    elif page == "Saved Passwords":
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
            <h2>Password Manager</h2>
            <p>Your personal database</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if is_user():
            st.markdown(f"Saved Password: {st.session_state['saved_password']}")
        else:
            st.warning("You must log in to view saved passwords.")
       