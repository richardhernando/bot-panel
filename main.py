from data_loader import get_candles
from estructura import detectar_bos, detectar_choch, detectar_liquidity_sweep
from order_blocks import detectar_order_blocks, filtrar_ob_mitigados
from rangos import detectar_rango_operativo, ob_fuera_de_rango
from marcos_mayores import detectar_direccion
from telegram_alert import enviar_senal_binaria, enviar_grafico
from grafico import crear_grafico
from divergencia import detectar_divergencia_rsi, confirmar_cambio_entrega
from datetime import datetime
import json
from os.path import exists

# Configuración inicial
modo = "Dinámico"
activo = 'BTCUSDT'
tf = '15m'
duracion = 15

# Cargar datos
df = get_candles(symbol=activo, interval=tf, limit=150)

# Estructura y divergencia
bos = detectar_bos(df)
choch = detectar_choch(df)
sweep = detectar_liquidity_sweep(df)
obs_buy = detectar_order_blocks(df, tipo='buy')
obs_sell = detectar_order_blocks(df, tipo='sell')
obs = filtrar_ob_mitigados(df, obs_buy + obs_sell)

# Divergencia RSI y confirmación
df = detectar_divergencia_rsi(df)
estructura = bos + choch
df = confirmar_cambio_entrega(df, estructura)

# Validar entrada
if df['confirmacion'].iloc[-1] == 'confirmada':
    direccion = 'call' if df['divergencia'].iloc[-1] == 'alcista' else 'put'
    ob = obs_buy[-1] if direccion == 'call' else obs_sell[-1]

    # Crear señal
    senal = {
        'hora': datetime.now().strftime('%H:%M'),
        'activo': activo.replace('USDT', '/USD'),
        'estrategia': f'Divergencia RSI + CHoCH ({tf})',
        'tf': tf.upper(),
        'direccion': direccion,
        'duracion': duracion,
        'confluencia': 3,
        'prioridad': 'Alta',
        'choch': choch[-1]['tipo'] if choch else '—',
        'liquidez': sweep[-1]['tipo'] if sweep else '—',
        'puntaje': 7,
        'probabilidad': 'Alta'
    }

    crear_grafico(df, [ob])
    enviar_grafico()
    enviar_senal_binaria(senal)