import streamlit as st
import pandas as pd
import os
import json
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

# Cargar y guardar configuración
def cargar_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def guardar_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

config = cargar_config()

# Config Streamlit
st.set_page_config(page_title="📡 Terminal Richard", layout="wide")
st.title("📊 Panel de Trading Institucional - Richard")

# Side panel
st.sidebar.header("🎛️ Filtros activos")
modo = st.sidebar.radio("⚙️ Modo", ["Conservador", "Dinámico", "Scalper"], index=["Conservador", "Dinámico", "Scalper"].index(config.get("modo_operacion", "Dinámico")))
filtro_marco_mayor = st.sidebar.checkbox("Confirmar D1 y H1", value=config.get("filtro_marco_mayor", True))
filtro_volatilidad = st.sidebar.checkbox("Filtrar por volatilidad", value=config.get("filtro_volatilidad", True))
filtro_rango = st.sidebar.checkbox("OB fuera del rango", value=config.get("filtro_rango", True))
probabilidad_minima = st.sidebar.selectbox("Probabilidad mínima", ["Baja", "Media", "Alta"], index=["Baja", "Media", "Alta"].index(config.get("probabilidad_minima", "Media")))

# Guardar config
config_actualizado = {
    "modo_operacion": modo,
    "filtro_marco_mayor": filtro_marco_mayor,
    "filtro_volatilidad": filtro_volatilidad,
    "filtro_rango": filtro_rango,
    "probabilidad_minima": probabilidad_minima
}
guardar_config(config_actualizado)

# Cargar datos
RUTA_SENALES = 'senales.csv'
RUTA_RANKING = 'ranking_hoy.csv'
RUTA_GRAFICO = 'grafico.png'

# Señales
st.subheader("📬 Últimas señales")
if os.path.exists(RUTA_SENALES):
    df = pd.read_csv(RUTA_SENALES).sort_values(by='hora', ascending=False)
    niveles = {"Baja": 1, "Media": 2, "Alta": 3}
    df['nivel'] = df['probabilidad'].map(niveles)
    df = df[df['nivel'] >= niveles[probabilidad_minima]].drop(columns=['nivel'])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No se han generado señales.")

# Resumen del día
st.subheader("📌 Resumen del día")
if os.path.exists(RUTA_SENALES):
    total =