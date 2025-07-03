import pandas as pd
import time
from datetime import datetime
from data_loader import get_candles
from estructura import detectar_bos, detectar_choch, detectar_liquidity_sweep
from order_blocks import detectar_order_blocks, filtrar_ob_mitigados
from divergencia import detectar_divergencia_rsi, confirmar_cambio_entrega
import os

# ⚙️ Configuración
activo = 'BTCUSDT'
tf = '15m'
duracion = 15
capital_inicial = 10000
riesgo_por_trade = 100
rango_futuro = 5  # velas para medir TP/SL
resultado_path = 'simulador_resultados.csv'

# Inicializar resultados
equity = [capital_inicial]
if not os.path.exists(resultado_path):
    pd.DataFrame(columns=['hora', 'activo', 'tipo', 'direccion', 'resultado', 'capital']).to_csv(resultado_path, index=False)

while True:
    try:
        df = get_candles(symbol=activo, interval=tf, limit=150)
        df = detectar_divergencia_rsi(df)
        estructura = detectar_choch(df) + detectar_bos(df)
        df = confirmar_cambio_entrega(df, estructura)
        sweep = detectar_liquidity_sweep(df)
        obs_buy = detectar_order_blocks(df, tipo='buy')
        obs_sell = detectar_order_blocks(df, tipo='sell')
        obs = filtrar_ob_mitigados(df, obs_buy + obs_sell)

        if df['confirmacion'].iloc[-1] == 'confirmada':
            direccion = 'buy' if df['divergencia'].iloc[-1] == 'alcista' else 'sell'
            ob = obs_buy[-1] if direccion == 'buy' else obs_sell[-1]
            entrada = ob['precio']
            tp = entrada + 0.005 if direccion == 'buy' else entrada - 0.005
            sl = entrada - 0.005 if direccion == 'buy' else entrada + 0.005

            # Buscar en futuro
            future = df.iloc[-rango_futuro:]
            resultado = 'loss'
            for precio in future['close']:
                if direccion == 'buy' and precio >= tp:
                    resultado = 'win'
                    break
                elif direccion == 'buy' and precio <= sl:
                    break
                elif direccion == 'sell' and precio <= tp:
                    resultado = 'win'
                    break
                elif direccion == 'sell' and precio >= sl:
                    break

            pnl = +riesgo_por_trade if resultado == 'win' else -riesgo_por_trade
            equity.append(equity[-1] + pnl)

            # Guardar resultado
            registro = {
                'hora': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'activo': activo,
                'tipo': 'Divergencia RSI + CHoCH',
                'direccion': direccion,
                'resultado': resultado,
                'capital': equity[-1]
            }

            df_reg = pd.read_csv(resultado_path)
            df_reg = pd.concat([df_reg, pd.DataFrame([registro])])
            df_reg.to_csv(resultado_path, index=False)

            print(f"[{registro['hora']}] ✅ Señal simulada: {direccion.upper()} | Resultado: {resultado} | Capital: {equity[-1]}")

        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No se generó señal válida.")

        time.sleep(60 * 15)  # Espera el próximo cierre de vela

    except Exception as e:
        print(f"⚠️ Error en simulador: {e}")
        time.sleep(60)