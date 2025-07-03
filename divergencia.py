import pandas as pd
import numpy as np

def calcular_rsi(df, periodo=14):
    delta = df['close'].diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)
    media_ganancia = ganancia.rolling(window=periodo).mean()
    media_perdida = perdida.rolling(window=periodo).mean()
    rs = media_ganancia / media_perdida
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi
    return df

def detectar_divergencia_rsi(df, ancho=5):
    """
    Detecta divergencias RSI simples:
    - Divergencia alcista: precio hace mínimo más bajo, RSI hace mínimo más alto
    - Divergencia bajista: precio hace máximo más alto, RSI hace máximo más bajo
    """
    df = calcular_rsi(df)
    df['divergencia'] = None

    for i in range(ancho, len(df) - ancho):
        precio_actual = df['close'].iloc[i]
        rsi_actual = df['RSI'].iloc[i]

        # Divergencia alcista
        precio_antes = df['close'].iloc[i - ancho]
        rsi_antes = df['RSI'].iloc[i - ancho]
        if precio_actual < precio_antes and rsi_actual > rsi_antes:
            df.at[df.index[i], 'divergencia'] = 'alcista'

        # Divergencia bajista
        if precio_actual > precio_antes and rsi_actual < rsi_antes:
            df.at[df.index[i], 'divergencia'] = 'bajista'

    return df

def confirmar_cambio_entrega(df, estructura):
    """
    Confirma si hay CHoCH o BOS reciente que coincida con la divergencia
    """
    df = df.copy()
    df['confirmacion'] = None

    for i in range(len(df)):
        if 'divergencia' in df.columns and pd.notna(df['divergencia'].iloc[i]):
            tipo_div = df['divergencia'].iloc[i]
            ventana = estructura[-5:]  # últimos eventos de estructura

            for evento in ventana:
                if tipo_div == 'alcista' and 'CHoCH Alcista' in evento['tipo']:
                    df.at[df.index[i], 'confirmacion'] = 'confirmada'
                elif tipo_div == 'bajista' and 'CHoCH Bajista' in evento['tipo']:
                    df.at[df.index[i], 'confirmacion'] = 'confirmada'

    return df