# dashboard/utils/api_client.py
import requests
import pandas as pd
from datetime import datetime
import streamlit as st

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    @st.cache_data(ttl=300)  # Cache de 5 minutos
    def get_despliegues(_self):
        """Obtiene lista de despliegues disponibles"""
        try:
            response = _self.session.get(f"{_self.base_url}/api/despliegues")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def get_trend_data(self, despliegue_id, variable, ts_from=None, ts_to=None, 
                       tabla="mediciones", limit=10000):
        """Obtiene datos de tendencia para gráficos"""
        params = {
            "despliegue_id": despliegue_id,
            "variables": [variable],
            "limit": limit
        }
        
        if ts_from:
            params["ts_from"] = ts_from.isoformat()
        if ts_to:
            params["ts_to"] = ts_to.isoformat()
        
        # TODO: Necesitarás que Marcelo agregue parámetro "tabla"
        response = self.session.post(
            f"{self.base_url}/api/analytics/trend",
            json=params
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("series"):
                points = data["series"][0]["points"]
                return pd.DataFrame(points)
        
        return pd.DataFrame()
    
    def get_quality_stats(self, despliegue_id):
        """Obtiene estadísticas de calidad para un despliegue"""
        # TODO: Implementar endpoint específico
        return {}
    
    def iniciar_procesamiento(self, despliegue_id, config=None):
        """Inicia procesamiento de un despliegue"""
        payload = {
            "despliegue_id": despliegue_id,
            "configuracion": config or {}
        }
        
        response = self.session.post(
            f"{self.base_url}/api/pipeline/procesar",
            json=payload
        )
        
        return response.json()