"""Auth helpers for Streamlit using PostgreSQL.

Expected table:
  iot.usuarios(correo UNIQUE, contrasena TEXT, rol, nombre)

Supports:
- Plain text passwords (compatibility)
- bcrypt hashes (recommended)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import streamlit as st

import psycopg2
import psycopg2.extras

try:
    import bcrypt  # type: ignore
except Exception:
    bcrypt = None


@dataclass
class AuthUser:
    id_usuario: int
    nombre: str
    correo: str
    rol: str


def _db_params_from_env() -> dict:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "Base22"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "12345678"),
    }


@st.cache_resource(show_spinner=False)
def get_conn():
    params = _db_params_from_env()
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    return conn


def _is_bcrypt_hash(value: str) -> bool:
    return (
        value.startswith("$2a$") or value.startswith("$2b$") or value.startswith("$2y$")
    )


def verify_password(plain_password: str, stored_password: str) -> bool:
    if stored_password is None:
        return False

    if _is_bcrypt_hash(stored_password):
        if bcrypt is None:
            return False
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), stored_password.encode("utf-8")
            )
        except Exception:
            return False

    return plain_password == stored_password


def authenticate(email: str, password: str) -> Tuple[bool, Optional[AuthUser], str]:
    email = (email or "").strip().lower()
    if not email or not password:
        return False, None, "Ingresa correo y contraseña."

    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                SELECT id_usuario, nombre, correo, rol, contrasena
                FROM iot.usuarios
                WHERE lower(correo) = %s
                """,
                (email,),
            )
            row = cur.fetchone()

        if not row:
            return False, None, "Usuario o contraseña incorrectos."

        if not verify_password(password, row["contrasena"]):
            return False, None, "Usuario o contraseña incorrectos."

        user = AuthUser(
            id_usuario=int(row["id_usuario"]),
            nombre=str(row["nombre"]),
            correo=str(row["correo"]),
            rol=str(row["rol"]),
        )
        return True, user, ""
    except Exception as e:
        return False, None, f"Error conectando a la BD: {e}"


def require_login() -> None:
    """Protect pages: if user not authenticated, redirect to login and stop."""
    if not st.session_state.get("auth_ok"):
        current = st.session_state.get("_current_page", "")
        if "login" not in str(current).lower():
            st.switch_page("pages/login.py")
        st.stop()


def logout() -> None:
    for k in ["auth_ok", "auth_user"]:
        if k in st.session_state:
            del st.session_state[k]
