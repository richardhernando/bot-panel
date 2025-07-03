def detectar_bos(df):
    bos = []
    for i in range(2, len(df)):
        high_prev = df['high'].iloc[i - 2]
        low_prev = df['low'].iloc[i - 2]
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        if high > high_prev:
            bos.append({'tipo': 'BOS Alcista', 'nivel': high, 'index': i})
        elif low < low_prev:
            bos.append({'tipo': 'BOS Bajista', 'nivel': low, 'index': i})
    return bos

def detectar_choch(df):
    choch = []
    for i in range(2, len(df)):
        high_prev = df['high'].iloc[i - 2]
        low_prev = df['low'].iloc[i - 2]
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        if high < high_prev and low > low_prev:
            choch.append({'tipo': 'CHoCH Bajista', 'index': i})
        elif high > high_prev and low < low_prev:
            choch.append({'tipo': 'CHoCH Alcista', 'index': i})
    return choch

def detectar_liquidity_sweep(df):
    sweeps = []
    for i in range(2, len(df)):
        high_prev = df['high'].iloc[i - 1]
        low_prev = df['low'].iloc[i - 1]
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        close = df['close'].iloc[i]
        if high > high_prev and close < high_prev:
            sweeps.append({'tipo': 'Sweep Alcista', 'index': i})
        elif low < low_prev and close > low_prev:
            sweeps.append({'tipo': 'Sweep Bajista', 'index': i})
    return sweeps

def volatilidad_actual(df, ventana=10):
    rangos = df['high'] - df['low']
    return rangos[-ventana:].mean()

def puntuar_senal(bos, ob, choch, sweep, prioridad, volatilidad, marco_mayor=False):
    puntaje = 0
    if bos: puntaje += 1
    if ob: puntaje += 1
    if choch: puntaje += 1
    if sweep: puntaje += 1
    if prioridad: puntaje += 1
    if volatilidad: puntaje += 1
    if marco_mayor: puntaje += 1
    return puntaje