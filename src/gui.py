#import streamlit as st  # Import Streamlit
import streamlit as st  # Import Streamlit
from .passwordLogic import check_strength, generate_strong_password, generate_password as pl_generate_password

def is_logged_in():
    # Replace this logic with actual authentication check
    return st.session_state.get("logged_in", False)

def is_user():
    return st.session_state.get("user_true", False)  # Returns user as false default

def run_app():

def strength(password: str):
    """Display strength using the logic in passwordLogic.check_strength."""
    result = check_strength(password)
    score = result.get("score", 0)
    rating = result.get("rating", "")
    suggestions = result.get("suggestions", [])

    # show a simple progress bar (0-100 mapped to 0.0-1.0)
    st.progress(score / 100)
    if rating:
        st.markdown(f"**Strength:** {rating} ({score}%)")
    if suggestions:
        st.markdown("**Suggestions to improve:**")
        for s in suggestions:
            st.write(f"- {s}")


def generate_password(length=12):
    # keep compatibility with a simple wrapper to the passwordLogic generator
    return pl_generate_password(length)


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


    col1, col2, col3 = st.columns([3, 1, 0.5])

        with col2:
            st.markdown("<br></br>",  unsafe_allow_html=True)
            if st.button("Generate"):
                new_pass = generate_strong_password()
                st.session_state["password_input"] = new_pass
                password = new_pass



    import streamlit as st
    from passwordLogic import check_strength, generate_strong_password, generate_password as pl_generate_password


    def is_logged_in() -> bool:
        return st.session_state.get("logged_in", False)


    def is_user() -> bool:
        return st.session_state.get("user_true", False)


    def strength(password: str) -> None:
        result = check_strength(password)
        score = result.get("score", 0)
        rating = result.get("rating", "")
        suggestions = result.get("suggestions", [])

        st.progress(score / 100)
        if rating:
            st.markdown(f"**Strength:** {rating} ({score}%)")
        if suggestions:
            st.markdown("**Suggestions to improve:**")
            for s in suggestions:
                st.write(f"- {s}")


    def generate_password(length: int = 12) -> str:
        return pl_generate_password(length)


    def run_app() -> None:
        st.set_page_config(page_title="Password Strength Manager", page_icon=":closed_lock_with_key:", layout="wide")

        st.title("Password Strength Manager")

        col1, col2 = st.columns([3, 1])

        with col1:
            pwd_in = st.text_input("Enter a password to check", key="password_input")
            if st.button("Check Strength"):
                strength(pwd_in)

        with col2:
            if st.button("Generate Strong Password"):
                new_pass = generate_strong_password()
                st.session_state["password_input"] = new_pass
                st.success("Generated strong password and placed it in the input field.")

        # Saved passwords demo area
        st.markdown("---")
        if st.checkbox("Show saved password area"):
            if is_user():
                st.write(st.session_state.get("saved_password", "(none)"))
            else:
                st.info("You must log in to view saved passwords.")
