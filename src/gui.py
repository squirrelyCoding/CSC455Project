import streamlit as st

def is_logged_in():
    # Replace this logic with actual authentication check
    return st.session_state.get("logged_in", False)

# Replace with  actual strength check
def strength():
    return st.session_state["check_strength"]

def run_app():

    #Sample login for save password
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "saved_password" not in st.session_state:
        st.session_state["saved_password"] = ""

    if st.sidebar.button("Login"):
        st.session_state["logged_in"] = True

    if st.sidebar.button("Passwords",  disabled= not is_logged_in()):
        ##want to bring up new page with the db for the passwords
        return True

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



  