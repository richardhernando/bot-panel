from telegram import Bot
import os

# 🔐 Reemplaza con tus credenciales reales
TOKEN = '7337866620:AAEIte6jI57ZJ-BDq38pMYHHayFsx3evFOE'
CHAT_ID = '5297126033'

bot = Bot(token=TOKEN)

def enviar_senal_binaria(senal):
    mensaje = f"""📡 *Nueva Señal Binaria*

🕒 Hora: {senal['hora']}
📈 Activo: {senal['activo']}
🧠 Estrategia: {senal['estrategia']}
🕓 Temporalidad: {senal['tf']}
📍 Dirección: *{senal['direccion'].upper()}*
⏱️ Duración: {senal['duracion']} min
🎯 Confluencia: {senal['confluencia']}
⚡ Prioridad: {senal['prioridad']}
🔁 CHoCH: {senal['choch']}
💧 Liquidez: {senal['liquidez']}
🏅 Puntaje: {senal['puntaje']} ({senal['probabilidad']})
"""

    bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')

def enviar_grafico(ruta='grafico.png'):
    if os.path.exists(ruta):
        with open(ruta, 'rb') as f:
            bot.send_photo(chat_id=CHAT_ID, photo=f)
    else:
        print("⚠️ No se encontró el gráfico para enviar.")

def enviar_ranking():
    archivo = 'ranking_hoy.csv'
    if os.path.exists(archivo):
        with open(archivo, 'rb') as f:
            bot.send_document(chat_id=CHAT_ID, document=f, filename=archivo, caption="🏆 Ranking diario de señales")
    else:
        print("📁 No se encontró el archivo de ranking para enviar.")