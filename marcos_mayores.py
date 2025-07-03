def detectar_direccion(df):
    """
    Detecta la dirección institucional (alcista o bajista) en base a BOS.
    Retorna 'buy', 'sell' o None si no hay suficiente estructura.
    """
    if len(df) < 20:
        return None

    ultimos_max = df['high'].rolling(window=5).max()
    ultimos_min = df['low'].rolling(window=5).min()

    bos_alcista = df['high'].iloc[-1] > ultimos_max.iloc[-2]
    bos_bajista = df['low'].iloc[-1] < ultimos_min.iloc[-2]

    if bos_alcista:
        return 'buy'
    elif bos_bajista:
        return 'sell'
    else:
        return None