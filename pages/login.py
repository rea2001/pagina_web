import os

import streamlit as st
from dotenv import load_dotenv

from utils.auth import authenticate
from utils.ui import hide_streamlit_pages_menu


def _load_env_once() -> None:
    # Safe: does nothing if .env doesn't exist
    load_dotenv()


def _init_session() -> None:
    st.session_state.setdefault("auth_ok", False)
    st.session_state.setdefault("auth_user", None)


def main() -> None:
    # IMPORTANT: must be first Streamlit call in the script
    st.set_page_config(
        page_title="Login - Sertecpet", page_icon="🔐", layout="centered"
    )

    # Hide Streamlit's built-in multipage navigation and the sidebar (login should be clean)
    hide_streamlit_pages_menu(keep_sidebar=False)

    _load_env_once()
    _init_session()
    st.session_state["_current_page"] = "login"

    # If already logged in, jump to dashboard
    if st.session_state.get("auth_ok"):
        st.switch_page("app.py")

    # Header
    col_logo, col_title = st.columns([1, 2])
    with col_logo:
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=120)

    with col_title:
        st.title("🔐 Iniciar sesión")
        st.caption("Ingresa con tu correo y contraseña")

    # Form
    with st.form("login_form", clear_on_submit=False):
        correo = st.text_input("Correo", placeholder="tu_correo@uta.edu.ec")
        contrasena = st.text_input(
            "Contraseña", type="password", placeholder="Tu contraseña"
        )
        submitted = st.form_submit_button("Entrar")

    if submitted:
        ok, user, msg = authenticate(correo, contrasena)
        if ok and user:
            st.session_state.auth_ok = True
            st.session_state.auth_user = {
                "id_usuario": user.id_usuario,
                "nombre": user.nombre,
                "correo": user.correo,
                "rol": user.rol,
            }
            st.success(f"✅ Bienvenido/a, {user.nombre} ({user.rol})")
            st.switch_page("app.py")
        else:
            st.error(msg or "No se pudo iniciar sesión")


if __name__ == "__main__":
    main()
