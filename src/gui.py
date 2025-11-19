import streamlit as st

# Import password logic robustly: try package-style, relative, then top-level fallback.
try:
    # If the project is installed or run from repository root, this should work
    from src.passwordLogic import (
        check_strength,
        generate_strong_password,
        generate_password as pl_generate_password,
    )
except Exception:
    try:
        # When running as a module inside `src` (rare with streamlit), use relative import
        from .passwordLogic import (
            check_strength,
            generate_strong_password,
            generate_password as pl_generate_password,
        )
    except Exception:
        # Fallback for simpler dev runs where a top-level `passwordLogic.py` exists
        from passwordLogic import (
            check_strength,
            generate_strong_password,
            generate_password as pl_generate_password,
        )


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
