
import streamlit as st
import sqlite3
import hashlib
import os
import hmac

st.set_page_config(
    page_title="The Caregiver Circle | Account",
    page_icon="🌿"
)

DB_PATH = r"C:\Users\tuf81\discussion_board.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    salt, original_hash = stored_hash.split(":")

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        600000
    )

    return hmac.compare_digest(
        new_hash.hex(),
        original_hash
    )


def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        password_hash = hash_password(password)

        cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
        """, (username.strip().lower(), email, password_hash))

        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, password_hash
    FROM users
    WHERE username = ? COLLATE NOCASE
    """, (username,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False, None

    if verify_password(password, result[1]):
        return True, result[0]

    return False, None


# ACCOUNT PAGE

st.title("🌿 The Caregiver Circle")
st.header("Your Account")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None


if st.session_state.user_id is None:

    create_tab, login_tab = st.tabs(
        ["Create Account", "Login"]
    )

    with create_tab:

        st.subheader("Join the Community")

        with st.form("registration_form"):

            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Create Account"
            )

            if register_button:

                if not username.strip() or not email.strip() or not password:
                    st.warning("Please complete all fields.")

                elif len(password) < 8:
                    st.warning("Password must be at least 12 characters.")

                elif password != confirm_password:
                    st.warning("Passwords do not match.")

                else:
                    success, message = register_user(
                        username.strip(),
                        email.strip().lower(),
                        password
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    with login_tab:

        st.subheader("Welcome Back")

        with st.form("login_form"):

            login_username = st.text_input("Username")
            login_password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

            if login_button:

                success, user_id = login_user(
                    login_username.strip(),
                    login_password
                )

                if success:
                    st.session_state.user_id = user_id
                    st.session_state.username = login_username.strip()
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

else:

    st.success(
        f"Welcome back, {st.session_state.username}!"
    )

    if st.button("Log Out"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
