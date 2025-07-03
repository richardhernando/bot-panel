import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def crear_grafico(df, order_blocks=None):
    plt.figure(figsize=(10, 5))
    plt.plot(df['close'], label='Precio', color='black')

    # Marcar divergencias RSI
    if 'divergencia' in df.columns:
        for i in range(len(df)):
            if df['divergencia'].iloc[i] == 'alcista':
                plt.scatter(i, df['close'].iloc[i], color='green', marker='^', label='🔁 Alcista' if i == 0 else "")
            elif df['divergencia'].iloc[i] == 'bajista':
                plt.scatter(i, df['close'].iloc[i], color='red', marker='v', label='🔁 Bajista' if i == 0 else "")

    # Confirmación con CHoCH o BOS
    if 'confirmacion' in df.columns:
        for i in range(len(df)):
            if df['confirmacion'].iloc[i] == 'confirmada':
                plt.annotate('🔁', (i, df['close'].iloc[i]), color='purple', fontsize=12)

    # Dibujar order blocks
    if order_blocks:
        for ob in order_blocks:
            color = 'green' if 'Alcista' in ob['tipo'] else 'red'
            plt.axhline(ob['precio'], color=color, linestyle='--', alpha=0.6)
            plt.text(len(df) - 20, ob['precio'], ob['tipo'], color=color)

    plt.title("📈 Divergencia RSI + Cambio Estructural")
    plt.xlabel("Velas")
    plt.ylabel("Precio")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('grafico.png')
    plt.close()