def detectar_rango_operativo(df, max_velas=50):
    """
    Detecta el rango operativo más reciente basado en los últimos máximos y mínimos.
    - max_velas: número de velas que se analizarán para construir el rango
    Devuelve:
        - high: nivel superior del rango
        - low: nivel inferior del rango
        - sweep_arriba: bool que indica si el precio barrió el alto del rango
        - sweep_abajo: bool que indica si el precio barrió el bajo del rango
        - precio: precio de cierre más reciente
    """
    if len(df) < max_velas:
        return None

    max_high = df['high'][-max_velas:].max()
    min_low = df['low'][-max_velas:].min()

    precio_actual = df['close'].iloc[-1]
    sweep_arriba = df['high'].iloc[-1] > max_high
    sweep_abajo = df['low'].iloc[-1] < min_low

    rango = {
        'high': max_high,
        'low': min_low,
        'sweep_arriba': sweep_arriba,
        'sweep_abajo': sweep_abajo,
        'precio': precio_actual
    }

    return rango

def ob_fuera_de_rango(order_block, rango):
    """
    Verifica si un Order Block está fuera del rango operativo.
    Retorna True si el OB está fuera del rango (válido), o False si está dentro (rechazado).
    """
    if not rango:
        return True  # Si no hay rango definido, aceptamos el OB

    return (
        order_block['high'] > rango['high'] or
        order_block['low'] < rango['low']
    )