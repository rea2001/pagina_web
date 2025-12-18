import streamlit as st
from dotenv import load_dotenv

from utils.auth import require_login, logout
from utils.ui import hide_streamlit_pages_menu

# Configuración de página (LO PRIMERO)
st.set_page_config(
    page_title="Sertecpet - Monitoreo Predictivo",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit's built-in multipage navigation (keep our sidebar)
hide_streamlit_pages_menu(keep_sidebar=True)

# Load env (optional)
load_dotenv()

# Protect the dashboard
st.session_state["_current_page"] = "app"
require_login()

# Inicializar variables de sesión
if "despliegue_seleccionado" not in st.session_state:
    st.session_state.despliegue_seleccionado = None
if "variables_seleccionadas" not in st.session_state:
    st.session_state.variables_seleccionadas = []


# CSS personalizado (estilo ABB)
def load_css():
    st.markdown(
        """
    <style>
    /* Estilos generales */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Tarjetas de KPIs */
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0068c9;
    }
    
    /* Botones estilo ABB */
    .stButton button {
        background-color: #0068c9;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #0056a3;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    # Cargar CSS
    load_css()

    # Sidebar (navegación)
    with st.sidebar:
        st.image("assets/logo.png", width=200)
        st.title("🔧 Sistema de Monitoreo")

        # Navegación entre páginas
        page = st.radio(
            "Navegación",
            ["🏠 Inicio", "📊 Despliegues", "🔍 Análisis", "⚙️ Configuración"],
            label_visibility="collapsed",
        )

        st.divider()

        # Información del usuario
        user = st.session_state.get("auth_user") or {}
        nombre = user.get("nombre", "Operador")
        rol = user.get("rol", "")
        st.caption(f"👤 Usuario: {nombre} {f'({rol})' if rol else ''}")
        st.caption(f"🕐 Última actualización: Hoy")

        # Cerrar sesión
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            logout()
            st.switch_page("pages/login.py")

        st.divider()

        # Botones de acción rápida
        if st.button("🔄 Actualizar todos los datos", use_container_width=True):
            st.info("Actualizando...")
            # Lógica de actualización

        if st.button("📥 Exportar reporte", use_container_width=True):
            st.info("Generando reporte...")

    # Contenido principal basado en página seleccionada
    if page == "🏠 Inicio":
        show_home_page()
    elif page == "📊 Despliegues":
        show_despliegues_page()
    elif page == "🔍 Análisis":
        show_analisis_page()
    elif page == "⚙️ Configuración":
        show_config_page()


def show_home_page():
    """Página de inicio / dashboard principal"""
    st.title("🏠 Dashboard de Monitoreo - Sertecpet")

    # 3 columnas para KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Despliegues Activos", "15", "↑ 2")

    with col2:
        st.metric("Equipos Monitoreados", "8", "→")

    with col3:
        st.metric("Alertas Activas", "3", "↓ 1")

    with col4:
        st.metric("Eficiencia Promedio", "94.2%", "↑ 0.5%")

    st.divider()

    # Lista de despliegues recientes
    st.subheader("📋 Despliegues Recientes")

    # Tabla de despliegues (placeholder)
    despliegues_data = [
        {
            "ID": 101,
            "Motor": "Bomba A",
            "Fecha": "2024-01-15",
            "Puntos": "50,243",
            "Estado": "✅ Procesado",
        },
        {
            "ID": 102,
            "Motor": "Bomba B",
            "Fecha": "2024-01-14",
            "Puntos": "48,512",
            "Estado": "✅ Procesado",
        },
        {
            "ID": 103,
            "Motor": "Motor 1",
            "Fecha": "2024-01-13",
            "Puntos": "52,100",
            "Estado": "⏳ Procesando",
        },
        {
            "ID": 104,
            "Motor": "Motor 2",
            "Fecha": "2024-01-12",
            "Puntos": "47,850",
            "Estado": "❌ Sin procesar",
        },
    ]

    # Mostrar como dataframe con botones de acción
    for d in despliegues_data:
        cols = st.columns([1, 2, 2, 2, 2, 2])
        with cols[0]:
            st.write(f"**{d['ID']}**")
        with cols[1]:
            st.write(d["Motor"])
        with cols[2]:
            st.write(d["Fecha"])
        with cols[3]:
            st.write(d["Puntos"])
        with cols[4]:
            status_color = {
                "✅ Procesado": "green",
                "⏳ Procesando": "orange",
                "❌ Sin procesar": "red",
            }
            st.markdown(
                f"<span style='color:{status_color[d['Estado']]}'>{d['Estado']}</span>",
                unsafe_allow_html=True,
            )
        with cols[5]:
            if d["Estado"] == "✅ Procesado":
                if st.button("📊 Ver", key=f"view_{d['ID']}"):
                    st.session_state.despliegue_seleccionado = d["ID"]
                    st.switch_page("pages/02_📊_Despliegues.py")
            elif d["Estado"] == "❌ Sin procesar":
                if st.button("🔄 Procesar", key=f"process_{d['ID']}"):
                    st.info(f"Iniciando procesamiento del despliegue {d['ID']}...")
                    # Llamar al pipeline


def show_despliegues_page():
    """Página principal de visualización de despliegues"""
    from pages.despliegue import show_despliegue_page

    show_despliegue_page()


def show_analisis_page():
    """Página de análisis detallado"""
    st.title("🔍 Análisis Detallado")
    st.write("Funcionalidad en desarrollo...")


def show_config_page():
    """Página de configuración"""
    st.title("⚙️ Configuración del Sistema")
    st.write("Funcionalidad en desarrollo...")


if __name__ == "__main__":
    main()
