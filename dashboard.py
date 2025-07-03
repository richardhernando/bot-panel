import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Ruta del archivo de resultados simulados
RUTA_SENALES = 'simulador_resultados.csv'

st.set_page_config(page_title="Terminal Institucional - Richard", layout="wide")

# 🎯 Portada
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📊 Terminal Táctica Institucional</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Bienvenido, Richard — Estrategia activada ⚔️</h4>", unsafe_allow_html=True)
st.markdown("---")

# Cargar señales si existen
if os.path.exists(RUTA_SENALES):
    df = pd.read_csv(RUTA_SENALES)
    df['hora'] = pd.to_datetime(df['hora'])

    # 🔍 Filtros
    with st.sidebar:
        st.header("🎛️ Filtros")
        activo = st.selectbox("Activo", options=['Todos'] + sorted(df['activo'].unique().tolist()))
        direccion = st.selectbox("Dirección", options=['Todos', 'buy', 'sell'])
        fecha_inicio = st.date_input("Desde", value=df['hora'].min().date())
        fecha_fin = st.date_input("Hasta", value=df['hora'].max().date())

    # Aplicar filtros
    df_filtrado = df.copy()
    if activo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['activo'] == activo]
    if direccion != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['direccion'] == direccion]
    df_filtrado = df_filtrado[(df_filtrado['hora'].dt.date >= fecha_inicio) & (df_filtrado['hora'].dt.date <= fecha_fin)]

    # 📊 Métricas
    total = len(df_filtrado)
    ganadoras = len(df_filtrado[df_filtrado['resultado'] == 'win'])
    perdedoras = len(df_filtrado[df_filtrado['resultado'] == 'loss'])
    winrate = round((ganadoras / total) * 100, 2) if total > 0 else 0
    capital_final = df_filtrado['capital'].iloc[-1] if total > 0 else None

    st.metric("Total de señales", total)
    st.metric("🏆 Winrate", f"{winrate}%")
    if capital_final:
        st.metric("📈 Capital actual simulado", f"${capital_final:,.2f}")

    # 📈 Gráfico de capital
    st.markdown("### 📉 Curva de Capital")
    fig, ax = plt.subplots()
    ax.plot(df_filtrado['hora'], df_filtrado['capital'], color='green')
    ax.set_xlabel("Hora")
    ax.set_ylabel("Capital")
    ax.grid(True)
    st.pyplot(fig)

    # 📋 Tabla de señales
    st.markdown("### 📋 Detalle de Señales Registradas")
    st.dataframe(df_filtrado[['hora', 'activo', 'direccion', 'resultado', 'capital']].sort_values(by='hora', ascending=False), use_container_width=True)

else:
    st.info("🚫 Aún no se han generado señales simuladas. Activa el simulador para comenzar.")