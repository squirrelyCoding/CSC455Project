import streamlit as st
from passwordLogic import check_strength, generate_password, generate_strong_password as pl_generate_password

# ---------------- Helper Functions ---------------- #

def is_logged_in():
    # Returns True if user is logged in, False otherwise
    return st.session_state.get("user_true", False)

def strength(password):
    # Replace with actual strength check
    result = check_strength(password)
    score = result.get("score", 0)
    rating = result.get("rating", "")
    suggestions = result.get("suggestions", [])

    # Display rating with color
    if rating == "Strong":
        st.success(f"{rating} password — {score}%")
    elif rating == "Medium":
        st.info(f"{rating} password — {score}%")
    else:
        st.warning(f"{rating} password — {score}%")

    # Display suggestions if any
    if suggestions:
        with st.expander("Suggestions"):
            for s in suggestions:
                st.write(f"- {s}")

# ---------------- Main App ---------------- #

def run_app():
    ## Page setup
    st.set_page_config(
        page_title="Password Manager",  
        page_icon=":closed_lock_with_key:",              
        layout="wide",             
        initial_sidebar_state="expanded"  
    )

    # Background color
    st.markdown("""
        <style>
        .stApp { background-color: #f0f8ff; }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state keys if they don't exist
    if "user_true" not in st.session_state:
        st.session_state["user_true"] = False
    if "saved_password" not in st.session_state:
        st.session_state["saved_password"] = ""
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = ""

    # ---------------- Sidebar ---------------- #
    with st.sidebar:
        st.header("Account")
        # Login form if not logged in
        if not is_logged_in():
            user_id = st.text_input("User Id", value=st.session_state.get("user_id", ""))
            st.session_state["user_id"] = user_id
            if st.button("Login"):
                if user_id:
                    st.session_state["user_true"] = True
                    st.success(f"Logged in as {user_id}")
                else:
                    st.error("Enter a User Id to login")
        else:
            # Show logged in user
            st.success(f"Logged in as {st.session_state['user_id']}")
            if st.button("Logout"):
                st.session_state["user_true"] = False
                st.session_state["user_id"] = ""
                st.info("Logged out")

        st.markdown("---")
        # Page selection
        page = st.selectbox("Page Selection", ["Password Strength", "Saved Passwords"])

    # ---------------- Main Pages ---------------- #
    if page == "Password Strength":
        # Page header
        st.markdown("""
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
        """, unsafe_allow_html=True)

        # Columns for input and buttons
        col1, col2 = st.columns([3, 1])

        with col1:
            # Password input
            password = st.text_input(
                "Password:", 
                value=st.session_state.get("saved_password", ""), 
                placeholder="Type your password here..."
            )
            st.session_state["saved_password"] = password

        with col2:
            # Button to generate a strong password
            if st.button("Generate Password"):
                generated = pl_generate_password()
                st.session_state["saved_password"] = generated
                password = generated  # Update local variable too
                st.success("Generated a new password!")

            # Button to check password strength
            if st.button("Check Strength"):
                strength(password)

            # Button to save password
            if st.button("Save Password", disabled=not is_logged_in()):
                st.session_state["saved_password"] = password
                st.success("Password saved!")

    elif page == "Saved Passwords":
        # Saved passwords page header
        st.markdown("""
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
        """, unsafe_allow_html=True)

        # Display saved password if logged in
        if is_logged_in():
            st.markdown(f"Saved Password: {st.session_state['saved_password']}")
        else:
            st.warning("You must log in to view saved passwords.")

