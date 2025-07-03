import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(page_title="Terminal Táctica - Richard", layout="wide")

# 🟢 Animación de bienvenida estilo terminal
with st.container():
    st.markdown("""
        <div style='background-color:#0e1117; padding: 30px; border-radius: 10px; margin-bottom: 20px'>
            <h2 style='color:#39ff14; text-align:center;'>🟢 Terminal táctica Richard iniciando...</h2>
            <p style='color:#cccccc; text-align:center;'>Sistema operativo cargando módulos de análisis 📡</p>
            <p style='color:#cccccc; text-align:center;'>Autenticación verificada... <strong style='color:#00ffcc;'>Usuario: richardhernando</strong></p>
            <p style='color:#cccccc; text-align:center;'>Panel institucional preparado. Ejecutando protocolos visuales 📊</p>
        </div>
        """, unsafe_allow_html=True)

# Archivo de señales
RUTA_SENALES = 'simulador_resultados.csv'

# Verificación y carga de datos
if os.path.exists(RUTA_SENALES):
    df = pd.read_csv(RUTA_SENALES)
    df['hora'] = pd.to_datetime(df['hora'])

    # 🎛️ Filtros
    with st.sidebar:
        st.header("🎚️ Filtros de visualización")
        activos = ['Todos'] + sorted(df['activo'].unique().tolist())
        activo = st.selectbox("Activo", activos)
        direccion = st.selectbox("Dirección", ['Todos', 'buy', 'sell'])
        fecha_inicio = st.date_input("Desde", value=df['hora'].min().date())
        fecha_fin = st.date_input("Hasta", value=df['hora'].max().date())

    # Aplicar filtros
    df_filtrado = df.copy()
    if activo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['activo'] == activo]
    if direccion != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['direccion'] == direccion]
    df_filtrado = df_filtrado[
        (df_filtrado['hora'].dt.date >= fecha_inicio) &
        (df_filtrado['hora'].dt.date <= fecha_fin)
    ]

    # 📊 Métricas principales
    total = len(df_filtrado)
    ganadoras = len(df_filtrado[df_filtrado['resultado'] == 'win'])
    winrate = round((ganadoras / total) * 100, 2) if total > 0 else 0
    capital_final = df_filtrado['capital'].iloc[-1] if total > 0 else 0

    st.markdown("## 📌 Resumen operativo")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de señales", total)
    col2.metric("🏆 Winrate", f"{winrate}%")
    col3.metric("💰 Capital actual", f"${capital_final:,.2f}")

    # 📉 Gráfico de capital
    if total > 1:
        st.markdown("### 📈 Curva de capital simulada")
        fig, ax = plt.subplots()
        ax.plot(df_filtrado['hora'], df_filtrado['capital'], color='lime')
        ax.set_xlabel("Hora")
        ax.set_ylabel("Capital")
        ax.grid(True)
        st.pyplot(fig)

    # 📋 Tabla de operaciones
    st.markdown("### 📋 Detalle de señales")
    st.dataframe(
        df_filtrado[['hora', 'activo', 'direccion', 'resultado', 'capital']].sort_values(by='hora', ascending=False),
        use_container_width=True
    )

else:
    st.info("🚫 Aún no se han generado señales. Cargá el archivo `simulador_resultados.csv` o activa tu simulador para ver resultados.")