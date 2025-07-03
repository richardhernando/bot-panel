import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
import requests

# Telegram config
TOKEN = "7337866620:AAEIte6jI57ZJ-BDq38pMYHHayFsx3evFOE"
CHAT_ID = "5297126033"
MEMORIA = "ultima_senal.txt"
ARCHIVO = "simulador_resultados.csv"

# Función para enviar mensaje
def enviar_alerta_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(url, data=payload)

# Estilo visual
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

# Animación bienvenida
st.markdown("""
<div style='background-color:#1e222c; padding: 25px; border-radius: 8px; margin-bottom: 15px'>
    <h2 style='color:#39ff14; text-align:center;'>🟢 Terminal Táctica Iniciando...</h2>
    <p style='color:#cccccc; text-align:center;'>Autenticación validada — Usuario: <strong style='color:#00ffe6;'>richardhernando</strong></p>
    <p style='color:#cccccc; text-align:center;'>Cargando módulos tácticos y visualización 📡</p>
</div>
""", unsafe_allow_html=True)

if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
    df['hora'] = pd.to_datetime(df['hora'])

    with st.sidebar:
        st.header("🎚️ Filtros")
        activo = st.selectbox("Activo", ['Todos'] + sorted(df['activo'].unique()))
        direccion = st.selectbox("Dirección", ['Todos', 'buy', 'sell'])
        fecha_inicio = st.date_input("Desde", df['hora'].min().date())
        fecha_fin = st.date_input("Hasta", df['hora'].max().date())
        st.markdown("---")
        if st.checkbox("🧨 Quiero borrar el archivo CSV"):
            if st.button("❌ Reiniciar señales"):
                os.remove(ARCHIVO)
                if os.path.exists(MEMORIA):
                    os.remove(MEMORIA)
                st.experimental_rerun()

    df_filtrado = df.copy()
    if activo != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['activo'] == activo]
    if direccion != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['direccion'] == direccion]
    df_filtrado = df_filtrado[
        (df_filtrado['hora'].dt.date >= fecha_inicio) &
        (df_filtrado['hora'].dt.date <= fecha_fin)
    ]

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

        # --- Alerta inteligente Telegram ---
        clave_actual = f"{ultima['hora']}_{ultima['activo']}_{ultima['direccion']}_{ultima['resultado']}_{ultima['capital']}"
        clave_previa = ""
        if os.path.exists(MEMORIA):
            with open(MEMORIA, "r") as f:
                clave_previa = f.read().strip()

        if clave_actual != clave_previa:
            mensaje = f"""📢 Nueva señal detectada:
Activo: <b>{ultima['activo']}</b>
Dirección: <b>{ultima['direccion'].upper()}</b>
Resultado: <b>{ultima['resultado'].upper()}</b>
Capital actual: <b>${ultima['capital']:,.2f}</b>
⏱ Hora: {ult_hora}
"""
            enviar_alerta_telegram(mensaje)
            with open(MEMORIA, "w") as f:
                f.write(clave_actual)

    # Métricas
    total = len(df_filtrado)
    ganadoras = len(df_filtrado[df_filtrado['resultado'] == 'win'])
    winrate = round((ganadoras / total) * 100, 2) if total > 0 else 0
    capital_final = df_filtrado['capital'].iloc[-1] if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de señales", total)
    col2.metric("🏆 Winrate", f"{winrate}%")
    col3.metric("💰 Capital final", f"${capital_final:,.2f}")

    # Gráfico capital
    if total > 1:
        st.markdown("### 📈 Curva de capital")
        fig, ax = plt.subplots()
        ax.plot(df_filtrado['hora'], df_filtrado['capital'], color='lime', linewidth=2)
        ax.set_xlabel("Hora")
        ax.set_ylabel("Capital")
        ax.grid(True)
        st.pyplot(fig)

    # Exportar Excel
    st.markdown("### 📁 Exportar resultados")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.sort_values(by='hora').to_excel(writer, index=False, sheet_name='Señales')
    st.download_button(
        label="📥 Descargar Excel",
        data=output.getvalue(),
        file_name="resumen_senales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Tabla
    st.markdown("### 📋 Operaciones")
    st.dataframe(df_filtrado[['hora','activo','direccion','resultado','capital']], use_container_width=True)

else:
    st.warning("⚠️ No se encontró el archivo `simulador_resultados.csv`. Cargalo o generá nuevas señales para visualizar el panel.")

# Botón de prueba Telegram
st.markdown("## 🔔 Verificar conexión del bot")
if st.button("📡 Enviar prueba a Telegram"):
    enviar_alerta_telegram("✅ Prueba exitosa: el bot RichardBot está conectado y operativo 📲🧠")
    st.success("Mensaje enviado al Telegram ✅")