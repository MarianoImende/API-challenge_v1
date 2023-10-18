import random
from babel.numbers import format_currency

# Función para generar un JSON con un saldo aleatorio en formato de dinero
def generar_json_saldo():
    #saldo = random.uniform(100, 1000000)  # Generar un número aleatorio entre 100 y 1,000,000
    saldo = random.uniform(-100000, 1000000)
    #saldo_formateado = format_currency(saldo, 'ARS', locale='es_AR')  # Formatear el número como dinero en dólares (puedes ajustar la moneda si es diferente)
    saldo_formateado = format_currency(abs(saldo), 'ARS', locale='es_AR')
    
    # Devolver el JSON con el saldo, asegurándose de que el saldo sea una cadena en formato de dinero con signo
    return {"saldo": f"{'-' if saldo < 0 else ''}{saldo_formateado}"}
    # data = {
    #     "saldo": saldo_formateado
    # }

    return data  # Devuelve el JSON como cadena con formato

# import random
# import locale

# # Establecer la configuración regional para el formato de dinero (por ejemplo, es-ES para español)
# locale.setlocale(locale.LC_ALL, 'es-AR')

# # Función para generar un JSON con un saldo aleatorio en formato de dinero
# def generar_json_saldo():
#     saldo = random.uniform(100, 1000000)  # Generar un número aleatorio entre 100 y 1,000,000
#     saldo_formateado = locale.currency(saldo, grouping=True)  # Formatear el número como dinero

#     data = {
#         "saldo": saldo_formateado
#     }

#     return data  # Devuelve el JSON como cadena con formato

