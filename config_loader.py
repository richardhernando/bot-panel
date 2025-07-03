import json

def leer_config(ruta='config.json'):
    try:
        with open(ruta, 'r') as f:
            return json.load(f)
    except:
        return {
            "filtro_marco_mayor": True,
            "filtro_volatilidad": True,
            "filtro_rango": True,
            "probabilidad_minima": "Media",
            "modo_operacion": "Dinámico"
        }