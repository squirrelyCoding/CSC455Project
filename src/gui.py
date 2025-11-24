import streamlit as st
from passwordLogic import (
    check_strength,
    generate_password,
    generate_strong_password as pl_generate_password,
)
from database.db_logic import (
    register_user,
    login_user,
    save_user_password,
    get_saved_passwords,
)

# ---------------- Helper Functions ---------------- #


def is_logged_in():
    # Returns True if user is logged in, False otherwise
    return st.session_state.get("logged_in", False)


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
        initial_sidebar_state="expanded",
    )

    # Background color
    st.markdown(
        """
        <style>
        .stApp { background-color: #f0f8ff; }
        .saved-password {
            color: black !important;
            font-size: 18px;
            font-weight: 600;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session state keys
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "stored_master" not in st.session_state:
        st.session_state["stored_master"] = None  # holds hashed master password from DB

    # ---------------- Sidebar ---------------- #
    with st.sidebar:
        st.header("Account")

        # If not logged in, show login
        if not is_logged_in():

            username = st.text_input("Username")

            if st.button("Login"):

                if username:

                    # Try to log in to existing account
                    exists, stored_master = login_user(username)

                    if exists:
                        # Login successful for existing user
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["stored_master"] = stored_master
                        st.success(f"Logged in as {username}")

                    else:
                        # Username does NOT exist — auto-create account
                        created = register_user(username)
                        if created:
                            st.success(f"New user created: {username}")
                            st.info(
                                "Your FIRST saved password will become your master password."
                            )

                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.session_state["stored_master"] = None
                        else:
                            st.error("Error creating user.")

                else:
                    st.error("Enter a username.")

        else:
            # Show login state and logout
            st.success(f"Logged in as {st.session_state['username']}")
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.session_state["stored_master"] = None
                st.info("Logged out")

        st.markdown("---")
        page = st.selectbox("Page Selection", ["Password Strength", "Saved Passwords"])

    # ---------------- Main Pages ---------------- #
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
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            password = st.text_input(
                "Password:", placeholder="Type your password here..."
            )

        with col2:
            if st.button("Generate Password"):
                password = pl_generate_password()
                st.success("Generated a new password!")
                st.write(password)

            if st.button("Check Strength"):
                strength(password)

            # Save encrypted password (no label required)
            if st.button("Save Password", disabled=not is_logged_in()):
                if not password:
                    st.error("Enter a password before saving.")
                else:
                    ok = save_user_password(st.session_state["username"], password)
                    if ok:
                        st.success("Password saved securely!")

                        # Reload stored_master (in case this was the first saved password)
                        exists, stored_master = login_user(st.session_state["username"])
                        st.session_state["stored_master"] = stored_master
                    else:
                        st.error("Error saving password.")

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
            unsafe_allow_html=True,
        )

        if is_logged_in():
            passwords = get_saved_passwords(
                st.session_state["username"], st.session_state["stored_master"]
            )

            if passwords:
                # Option A: Numbered list
                for idx, pw in enumerate(passwords[1:], start=1):
                   st.markdown(f"<p class='saved-password'>Password {idx}: {pw}</p>", unsafe_allow_html=True)

            else:
                st.info("No saved passwords yet.")

        else:
            st.warning("You must log in to view saved passwords.")
