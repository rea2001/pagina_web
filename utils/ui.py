import streamlit as st
from textwrap import dedent


def hide_streamlit_pages_menu(keep_sidebar=True):
    css = dedent(
        """
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    </style>
    """
    )

    if not keep_sidebar:
        css += dedent(
            """
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        button[kind="header"] { display: none !important; }
        </style>
        """
        )

    st.markdown(css, unsafe_allow_html=True)
