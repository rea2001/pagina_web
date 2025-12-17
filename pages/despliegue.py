import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from utils.api_client import APIClient

# Título de la página
st.set_page_config(
    page_title="Visualización de Despliegue",
    page_icon="📊"
)

def main():
    st.title("📊 Visualización de Despliegue")
    
    # Verificar si hay un despliegue seleccionado
    if not st.session_state.get('despliegue_seleccionado'):
        st.warning("⚠️ No hay despliegue seleccionado. Ve a Inicio y selecciona uno.")
        if st.button("🏠 Ir a Inicio"):
            st.switch_page("app.py")
        return
    
    despliegue_id = st.session_state.despliegue_seleccionado
    
    # Header con información del despliegue
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"Despliegue #{despliegue_id}")
    with col2:
        st.metric("Estado", "✅ Procesado")
    with col3:
        if st.button("🔄 Reprocesar"):
            st.info(f"Reprocesando despliegue {despliegue_id}...")
            # Llamar al pipeline
    
    st.divider()
    
    # Sidebar de controles
    with st.sidebar:
        st.subheader("🎛️ Controles de Visualización")
        
        # 1. Selección de variables
        variables = obtener_variables_despliegue(despliegue_id)
        variables_seleccionadas = st.multiselect(
            "Variables a visualizar",
            options=variables,
            default=variables[:2] if len(variables) >= 2 else variables
        )
        
        # 2. Tipo de datos
        tipo_datos = st.radio(
            "Tipo de datos",
            ["Crudos", "Procesados", "Ambos"],
            horizontal=True
        )
        
        # 3. Rango temporal
        fecha_min, fecha_max = obtener_rango_fechas(despliegue_id)
        rango_fechas = st.slider(
            "Rango temporal",
            min_value=fecha_min,
            max_value=fecha_max,
            value=(fecha_min, fecha_max),
            format="YYYY-MM-DD HH:mm"
        )
        
        # 4. Filtro de calidad (solo para crudos)
        if tipo_datos in ["Crudos", "Ambos"]:
            st.subheader("🎚️ Filtros de Calidad")
            calidad_filtro = st.multiselect(
                "Códigos de calidad a incluir",
                options=[0, 1, 2, 3, 4],
                default=[0, 1],
                format_func=lambda x: f"Código {x}: {obtener_descripcion_calidad(x)}"
            )
        
        # 5. Botones de acción
        st.divider()
        if st.button("📥 Exportar gráfico como PNG", use_container_width=True):
            st.info("Exportando...")
        
        if st.button("📊 Generar reporte PDF", use_container_width=True):
            st.info("Generando reporte...")
    
    # Contenido principal - Pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Gráficos de Tendencias", 
        "🔍 Análisis de Calidad", 
        "📋 Datos Tabulares",
        "⚙️ Configuración Avanzada"
    ])
    
    with tab1:
        mostrar_graficos_tendencia(
            despliegue_id, 
            variables_seleccionadas, 
            tipo_datos, 
            rango_fechas
        )
    
    with tab2:
        mostrar_analisis_calidad(despliegue_id)
    
    with tab3:
        mostrar_datos_tabulares(despliegue_id, variables_seleccionadas)
    
    with tab4:
        mostrar_configuracion_avanzada(despliegue_id)

def obtener_variables_despliegue(despliegue_id):
    """Obtiene variables disponibles para un despliegue"""
    # TODO: Conectar con API de Marcelo
    return ["temperatura", "presion", "vibracion", "corriente", "voltaje"]

def obtener_rango_fechas(despliegue_id):
    """Obtiene rango de fechas para un despliegue"""
    # TODO: Conectar con API de Marcelo
    from datetime import datetime, timedelta
    return datetime.now() - timedelta(days=7), datetime.now()

def obtener_descripcion_calidad(codigo):
    """Descripción de códigos de calidad"""
    descripciones = {
        0: "Válido",
        1: "Faltante",
        2: "Outlier",
        3: "Físicamente imposible",
        4: "Error de categoría"
    }
    return descripciones.get(codigo, "Desconocido")

def mostrar_graficos_tendencia(despliegue_id, variables, tipo_datos, rango_fechas):
    """Muestra gráficos de tendencia"""
    st.subheader("📈 Gráficos de Tendencias")
    
    if not variables:
        st.warning("Selecciona al menos una variable para visualizar")
        return
    
    # Para cada variable seleccionada
    for var in variables:
        st.write(f"### Variable: `{var}`")
        
        # Crear gráfico con Plotly
        fig = go.Figure()
        
        # Datos crudos (si se seleccionó)
        if tipo_datos in ["Crudos", "Ambos"]:
            datos_crudos = obtener_datos_crudos(despliegue_id, var, rango_fechas)
            if datos_crudos:
                fig.add_trace(go.Scatter(
                    x=datos_crudos['timestamp'],
                    y=datos_crudos['valor'],
                    name=f"{var} (Crudos)",
                    line=dict(color='red', dash='dash', width=1),
                    mode='lines+markers'
                ))
        
        # Datos procesados (si se seleccionó)
        if tipo_datos in ["Procesados", "Ambos"]:
            datos_procesados = obtener_datos_procesados(despliegue_id, var, rango_fechas)
            if datos_procesados:
                fig.add_trace(go.Scatter(
                    x=datos_procesados['timestamp'],
                    y=datos_procesados['valor'],
                    name=f"{var} (Procesados)",
                    line=dict(color='blue', width=2),
                    mode='lines'
                ))
        
        # Configurar layout
        fig.update_layout(
            title=f"Tendencia de {var}",
            xaxis_title="Fecha/Hora",
            yaxis_title="Valor",
            hovermode="x unified",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def mostrar_analisis_calidad(despliegue_id):
    """Muestra análisis de calidad de datos"""
    st.subheader("🔍 Análisis de Calidad de Datos")
    
    # Obtener estadísticas de calidad
    # TODO: Conectar con tu pipeline para obtener estas métricas
    estadisticas = {
        "total_puntos": 50243,
        "validos": 48500,
        "outliers": 125,
        "faltantes": 47,
        "imposibles": 12,
        "gaps": 3
    }
    
    # Mostrar métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Datos Válidos", f"{estadisticas['validos']}", 
                 f"{(estadisticas['validos']/estadisticas['total_puntos'])*100:.1f}%")
    
    with col2:
        st.metric("Outliers", estadisticas['outliers'], 
                 f"{(estadisticas['outliers']/estadisticas['total_puntos'])*100:.1f}%")
    
    with col3:
        st.metric("Valores Faltantes", estadisticas['faltantes'],
                 f"{(estadisticas['faltantes']/estadisticas['total_puntos'])*100:.1f}%")
    
    with col4:
        st.metric("Gaps Temporales", estadisticas['gaps'])
    
    # Gráfico de distribución de calidad
    fig = go.Figure(data=[go.Pie(
        labels=['Válidos', 'Outliers', 'Faltantes', 'Imposibles'],
        values=[estadisticas['validos'], estadisticas['outliers'], 
                estadisticas['faltantes'], estadisticas['imposibles']],
        hole=.3
    )])
    
    fig.update_layout(title="Distribución de Calidad de Datos")
    st.plotly_chart(fig, use_container_width=True)

def mostrar_datos_tabulares(despliegue_id, variables):
    """Muestra datos en formato tabular"""
    st.subheader("📋 Datos Tabulares")
    
    # Selector de qué datos mostrar
    tipo_tabla = st.radio(
        "Mostrar datos:",
        ["Crudos", "Procesados", "Ambos"],
        horizontal=True,
        key="tabla_selector"
    )
    
    # Filtros adicionales
    col1, col2 = st.columns(2)
    with col1:
        limite_filas = st.number_input("Límite de filas", min_value=100, max_value=10000, value=1000)
    with col2:
        if st.button("📥 Exportar a CSV"):
            st.info("Exportando...")
    
    # Obtener datos
    # TODO: Conectar con API de Marcelo
    datos = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='15min'),
        'temperatura': np.random.normal(85, 5, 100),
        'presion': np.random.normal(100, 10, 100)
    })
    
    # Mostrar tabla
    st.dataframe(
        datos,
        use_container_width=True,
        height=400
    )

def mostrar_configuracion_avanzada(despliegue_id):
    """Configuración avanzada para reprocesamiento"""
    st.subheader("⚙️ Configuración de Reprocesamiento")
    
    st.warning("⚠️ Cambiar estos parámetros requiere reprocesar el despliegue completo.")
    
    # Parámetros configurables
    with st.form("config_reproceso"):
        col1, col2 = st.columns(2)
        
        with col1:
            metodo_imputacion = st.selectbox(
                "Método de imputación",
                ["Lineal", "Forward Fill", "KNN", "Media"]
            )
            
            umbral_outliers = st.selectbox(
                "Umbral para outliers",
                ["IQR Automático", "2σ", "3σ", "Personalizado"]
            )
            
            if umbral_outliers == "Personalizado":
                st.number_input("Valor personalizado (σ)", min_value=1.0, max_value=5.0, value=3.0)
        
        with col2:
            freq_resample = st.selectbox(
                "Frecuencia de resample",
                ["15 minutos", "30 minutos", "1 hora", "Mantener original"]
            )
            
            tratamiento_gaps = st.selectbox(
                "Tratamiento de gaps largos",
                ["Interpolar", "Dejar como NaN", "Rellenar con último valor"]
            )
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        with col1:
            reprocesar = st.form_submit_button("🔄 Reprocesar con esta configuración", type="primary")
        with col2:
            guardar_config = st.form_submit_button("💾 Guardar configuración")
        with col3:
            cargar_default = st.form_submit_button("↩️ Cargar valores por defecto")
        
        if reprocesar:
            st.success(f"Reprocesando despliegue {despliegue_id} con nueva configuración...")
            # Llamar al pipeline con nueva configuración

def obtener_datos_crudos(despliegue_id, variable, rango_fechas):
    """Obtiene datos crudos de la API"""
    # TODO: Implementar usando API de Marcelo
    return None

def obtener_datos_procesados(despliegue_id, variable, rango_fechas):
    """Obtiene datos procesados de la API"""
    # TODO: Implementar usando API de Marcelo
    return None

if __name__ == "__main__":
    main()