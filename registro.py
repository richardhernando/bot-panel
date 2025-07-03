import csv
import os
import pandas as pd
from datetime import datetime

def guardar_senal_csv(senal):
    archivo = 'senales.csv'
    existe = os.path.isfile(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=senal.keys())
        if not existe:
            writer.writeheader()
        writer.writerow(senal)

def generar_ranking_csv():
    archivo = 'senales.csv'
    if not os.path.isfile(archivo):
        print("📂 No hay señales registradas aún.")
        return

    df = pd.read_csv(archivo)
    hoy = datetime.now().strftime('%Y-%m-%d')
    df['fecha'] = hoy
    df_hoy = df[df['fecha'] == hoy]

    if df_hoy.empty:
        print("📭 No hay señales para hoy.")
        return

    ranking = df_hoy.sort_values(by='puntaje', ascending=False)
    ranking.to_csv('ranking_hoy.csv', index=False)
    print("🏆 Ranking generado: ranking_hoy.csv")