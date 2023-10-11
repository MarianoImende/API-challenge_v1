import random
# Función para generar un JSON con cuentas aleatorias
def generar_json_cuentas():
    cuentas = []

    tipos = ["CA $", "CC $", "CA USD", "CC USD"]
    cantidad_cuentas = random.randint(2, 5)

    for _ in range(cantidad_cuentas):
        cuenta = {
            "numero": ''.join(random.choices('0123456789', k=8)),  # Número de cuenta ficticio de 8 dígitos
            "tipo": random.choice(tipos)  # Tipo de cuenta aleatorio
        }
        cuentas.append(cuenta)

    data = {
        "cuentas": cuentas
    }

    return data # Devuelve el JSON como cadena con formato