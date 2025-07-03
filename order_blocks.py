def detectar_order_blocks(df, tipo='buy'):
    blocks = []
    for i in range(2, len(df) - 1):
        vela_actual = df.iloc[i]
        vela_siguiente = df.iloc[i + 1]

        if tipo == 'buy' and vela_actual['close'] < vela_actual['open']:
            if vela_siguiente['close'] > vela_siguiente['high']:
                blocks.append({
                    'tipo': 'OB Alcista',
                    'open': vela_actual['open'],
                    'close': vela_actual['close'],
                    'high': vela_actual['high'],
                    'low': vela_actual['low'],
                    'index': i
                })

        elif tipo == 'sell' and vela_actual['close'] > vela_actual['open']:
            if vela_siguiente['close'] < vela_siguiente['low']:
                blocks.append({
                    'tipo': 'OB Bajista',
                    'open': vela_actual['open'],
                    'close': vela_actual['close'],
                    'high': vela_actual['high'],
                    'low': vela_actual['low'],
                    'index': i
                })
    return blocks

def filtrar_ob_mitigados(df, order_blocks):
    ob_validos = []
    for ob in order_blocks:
        zona_baja = ob['low']
        zona_alta = ob['high']
        index_inicio = ob['index'] + 1
        tocado = False
        for i in range(index_inicio, len(df)):
            low = df['low'].iloc[i]
            high = df['high'].iloc[i]
            if low <= zona_alta and high >= zona_baja:
                tocado = True
                break
        if not tocado:
            ob_validos.append(ob)
    return ob_validos

def marcar_prioridad(df, ob):
    precio_actual = df['close'].iloc[-1]
    distancia = abs(precio_actual - ob['high']) / ob['high']
    return distancia < 0.001  # menos del 0.1%