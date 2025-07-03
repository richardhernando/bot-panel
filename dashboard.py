import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO

# Configuración del modo oscuro y página
st.set_page_config(page_title="Terminal Richard", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    .stMetric {
        background-color: #1e222c;
        border-radius: 6px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Animación de bienvenida
st.markdown("""
<div style='background-color:#1e222c; padding: 25px; border-radius: 8px; margin-bottom: 15px'>
    <h2 style='color:#39ff14; text-align:center;'>🟢 Terminal Táctica Iniciando...</h2>
    <p style='color:#cccccc; text-align:center;'>Autenticación validada — Usuario: <strong style='color:#00ffe6;'>richardhernando</strong></p>
    <p style='color:#cccccc; text-align:center;'>Cargando módulos de análisis, métricas y visualización 📊</p>
</div>
""", unsafe_allow_html=True)

# Ruta al archivo CSV
ARCHIVO = 'simulador_resultados.csv'

# Verificar si existe el archivo de señales
if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
    df['hora'] = pd.to_datetime(df['hora'])

    # Filtros
    with st.sidebar:
        st.header("🎛️ Filtros")
        activo = st.selectbox("Activo", ['Todos'] + sorted(df['activo'].unique()))
        direccion = st.selectbox("Dirección", ['Todos', 'buy', 'sell'])
        fecha_inicio = st.date_input("Desde", df['hora'].min().date())
        fecha_fin = st.date_input("Hasta", df['hora'].max().date())
        st.markdown("---")

        # Botón de reinicio del CSV
        if st.checkbox("🧨 Quiero borrar el archivo CSV"):
            if st.button("❌ Reiniciar señales"):
                os.remove(ARCHIVO)
                st.experimental_rerun()

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

    # Resumen inteligente
    if not df_filtrado.empty:
        ultima = df_filtrado.sort_values(by='hora').iloc[-1]
        ult_senal = f"{ultima['direccion'].upper()} {ultima['activo']} — {ultima['resultado'].upper()}"
        ult_hora = ultima['hora'].strftime('%H:%M')
        df_hoy = df_filtrado[df_filtrado['hora'].dt.date == pd.Timestamp.now().date()]
        winrate_hoy = round((len(df_hoy[df_hoy['resultado']=='win']) / len(df_hoy))*100, 2) if len(df_hoy) > 0 else 0
        ganancia_neta = df_filtrado['capital'].iloc[-1] - df_filtrado['capital'].iloc[0]

        st.markdown(f"""
        ### 🧠 Resumen del sistema
        - Última señal: **{ult_senal}** a las **{ult_hora}**
        - Winrate del día: **{winrate_hoy}%**
        - Ganancia neta: **${ganancia_neta:,.2f}**
        - Señales filtradas: **{len(df_filtrado)}**
        """)

    # Métricas principales
    total = len(df_filtrado)
    ganadoras = len(df_filtrado[df_filtrado['resultado'] == 'win'])
    winrate = round((ganadoras / total) * 100, 2) if total > 0 else 0
    capital_final = df_filtrado['capital'].iloc[-1] if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de señales", total)
    col2.metric("🏆 Winrate", f"{winrate}%")
    col3.metric("💰 Capital final", f"${capital_final:,.2f}")

    # Curva de capital
    if total > 1:
        st.markdown("### 📈 Curva de capital")
        fig, ax = plt.subplots()
        ax.plot(df_filtrado['hora'], df_filtrado['capital'], color='lime', linewidth=2)
        ax.set_xlabel("Hora")
        ax.set_ylabel("Capital")
        ax.grid(True)
        st.pyplot(fig)

    # Exportar a Excel
    st.markdown("### 📤 Exportar resultados")
    df_exportar = df_filtrado.sort_values(by='hora')
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exportar.to_excel(writer, index=False, sheet_name='Señales')
    st.download_button(
        label="📁 Descargar Excel",
        data=output.getvalue(),
        file_name="resumen_senales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Tabla de datos
    st.markdown("### 📋 Operaciones")
    st.dataframe(df_exportar[['hora','activo','direccion','resultado','capital']], use_container_width=True)

else:
    st.warning("⚠️ No se encontró el archivo `simulador_resultados.csv`. Cargalo o generá nuevas señales para visualizar el panel.")
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