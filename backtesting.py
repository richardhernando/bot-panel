import pandas as pd
import matplotlib.pyplot as plt
import ccxt
from datetime import datetime
from estructura import detectar_bos, detectar_choch, detectar_liquidity_sweep
from order_blocks import detectar_order_blocks, filtrar_ob_mitigados
from rangos import detectar_rango_operativo, ob_fuera_de_rango
from marcos_mayores import detectar_direccion
import time
import os

# 🧠 Configuración
symbol = 'BTC/USDT'
timeframe = '15m'
exchange = ccxt.binance()
desde = exchange.parse8601('2023-01-01T00:00:00Z')
capital_inicial = 10000
riesgo_por_trade = 100
rango_captura = 10  # velas futuras para simular SL/TP
spread = 0.0        # puedes simular spread aquí si quieres
modo = 'Dinámico'

# 🕒 Descargar velas
ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=desde, limit=1500)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# 📊 Inicializar variables
equity = [capital_inicial]
trades = []

for i in range(60, len(df) - rango_captura):
    sub_df = df.iloc[i - 50:i + 1].copy()

    try:
        bos = detectar_bos(sub_df)
        choch = detectar_choch(sub_df)
        sweep = detectar_liquidity_sweep(sub_df)
        obs_buy = detectar_order_blocks(sub_df, tipo='buy')
        obs_sell = detectar_order_blocks(sub_df, tipo='sell')
        obs = filtrar_ob_mitigados(sub_df, obs_buy + obs_sell)

        if not bos and not choch:
            continue

        direccion = None
        tipo_senal = None
        if bos:
            direccion = 'buy' if bos[-1]['tipo'] == 'BOS Alcista' else 'sell'
            tipo_senal = 'BOS'
        elif choch:
            direccion = 'buy' if choch[-1]['tipo'] == 'CHoCH Alcista' else 'sell'
            tipo_senal = 'CHoCH'

        ob_direccion = [ob for ob in obs if ob['tipo'] == ('OB Alcista' if direccion == 'buy' else 'OB Bajista')]
        if not ob_direccion:
            continue

        ob = ob_direccion[-1]
        entry_price = ob['precio']
        stop_loss = entry_price - 0.005 if direccion == 'buy' else entry_price + 0.005
        take_profit = entry_price + 0.005 if direccion == 'buy' else entry_price - 0.005

        future = df.iloc[i + 1:i + 1 + rango_captura]
        result = 'loss'
        for price in future['close']:
            if direccion == 'buy':
                if price >= take_profit:
                    result = 'win'
                    break
                elif price <= stop_loss:
                    break
            else:
                if price <= take_profit:
                    result = 'win'
                    break
                elif price >= stop_loss:
                    break

        pnl = +riesgo_por_trade if result == 'win' else -riesgo_por_trade
        equity.append(equity[-1] + pnl)

        trades.append({
            'fecha': sub_df.index[-1],
            'activo': symbol,
            'tipo': tipo_senal,
            'direccion': direccion,
            'entrada': entry_price,
            'tp': take_profit,
            'sl': stop_loss,
            'resultado': result
        })

    except Exception as e:
        print(f"❌ Error en índice {i}: {e}")
        time.sleep(1)
        continue

# 📈 Resultados
df_trades = pd.DataFrame(trades)
df_trades.to_csv("resultado_backtest.csv", index=False)

wins = df_trades[df_trades["resultado"] == "win"].shape[0]
losses = df_trades[df_trades["resultado"] == "loss"].shape[0]
total = wins + losses
winrate = round((wins / total) * 100, 1) if total > 0 else 0

print(f"✅ Ganadas: {wins} | ❌ Perdidas: {losses}")
print(f"🎯 Winrate: {winrate}%")
print(f"📈 Capital final: {equity[-1]:.2f} USDT")

# 📉 Guardar curva de capital
plt.figure(figsize=(10, 5))
plt.plot(equity, linewidth=2, color='blue')
plt.title("📈 Curva de capital - Backtest SMC")
plt.xlabel("Operaciones")
plt.ylabel("Capital")
plt.grid()
plt.tight_layout()
plt.savefig("equity_curve.png")
plt.close()