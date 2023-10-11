import json
import random

# Función para generar un JSON con nombres de bancos y números de tarjetas ficticios
def generar_json_tarjetas():
    # Lista de nombres de bancos ficticios
    nombres_bancos = ["BANCO BAPRO", "BANCO NACION", "BANCO CIUDAD", "BANCO PIANO", "BANCO HIPOTECARIO","BANCO HSBC","BANCO DE SANTA FE","BANCO DE LA PAMPA","BANCO SANTANDER"]
    cantidad_tarjetas = random.randint(2, 4)
    tarjetas = []

    for _ in range(cantidad_tarjetas):
        tarjeta = {
            "descripcion": random.choice(nombres_bancos),  # Nombre de banco ficticio
            "numero": ''.join(random.choices('0123456789', k=12))  # Número de tarjeta ficticio de 12 dígitos
        }
        tarjetas.append(tarjeta)

    data = {
        "tarjetas": tarjetas
    }

    return data# json.dumps(data, indent=4)  # Devuelve el JSON como cadena con formato