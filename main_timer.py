import time
import os
from datetime import datetime

INTERVALO_MINUTOS = 1  # Puedes cambiarlo a 5, 15, etc.

def ejecutar_bot():
    print(f"\n🕒 {datetime.now().strftime('%H:%M:%S')} - Ejecutando análisis...")
    os.system("python main.py")
    print(f"⏳ Esperando {INTERVALO_MINUTOS} minutos para el próximo escaneo...\n")

while True:
    ejecutar_bot()
    time.sleep(INTERVALO_MINUTOS * 60)