import random
from datetime import datetime, timedelta

import random
from datetime import datetime, timedelta


def generarFechas(fecha_desde, fecha_hasta):
    # Convertir las fechas de cadena a objetos datetime
    fecha_desde_dt = datetime.strptime(fecha_desde, "%Y%m%d")
    fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y%m%d")
    fechas_generadas = []
    
    for _ in range(5):  # Generar cinco fechas
        # Generar un número aleatorio de días entre fecha_desde y fecha_hasta
        diferencia_dias = (fecha_hasta_dt - fecha_desde_dt).days
        dias_aleatorios = random.randint(0, diferencia_dias)
        
        # Calcular la fecha aleatoria
        fecha_generada = fecha_desde_dt + timedelta(days=dias_aleatorios)
        
        # Formatear la fecha como "yyyymmdd"
        fecha_formateada = fecha_generada.strftime("%Y%m%d")
        
        # Elegir una descripción aleatoria
        descripcion = random.choice(["Compra", "Plazo Fijo ingreso", "Ingreso en efectivo", "Transferencia Credito", "Depósito en efectivo", "Retiro de cajero automático", "Transferencia a otra cuenta", "Pago de impuestos y servicios"])
        
        # Determinar si el monto debe ser negativo
        if descripcion in ["Retiro de cajero automático", "Transferencia a otra cuenta", "Compra", "Pago de impuestos y servicios"]:
            monto = round(random.uniform(-10000, -1), 2)  # Monto negativo
        else:
            monto = round(random.uniform(1, 10000), 2)  # Monto positivo
        
        # Crear un diccionario para el movimiento
        movimiento = {
            "fecha": fecha_formateada,
            "monto": monto,
            "descripcion": descripcion
        }
        
        # Agregar el movimiento a la lista de fechas generadas
        fechas_generadas.append(movimiento)
    
    # Crear el JSON final
    json_generado = {"movimientos": fechas_generadas}
    
    return json_generado


# def generarFechas(fecha_desde, fecha_hasta):
#     # Convertir las fechas de cadena a objetos datetime
#     fecha_desde_dt = datetime.strptime(fecha_desde, "%Y%m%d")
#     fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y%m%d")
#     fechas_generadas = []
    
#     for _ in range(5):  # Generar cinco fechas
#         # Generar un número aleatorio de días entre fecha_desde y fecha_hasta
#         diferencia_dias = (fecha_hasta_dt - fecha_desde_dt).days
#         dias_aleatorios = random.randint(0, diferencia_dias)
        
#         # Calcular la fecha aleatoria
#         fecha_generada = fecha_desde_dt + timedelta(days=dias_aleatorios)
        
#         # Formatear la fecha como "yyyymmdd"
#         fecha_formateada = fecha_generada.strftime("%Y%m%d")
        
#         # Crear un diccionario para el movimiento
#         movimiento = {
#             "fecha": fecha_formateada,
#             "tipo": random.choice(["Depósito", "Retiro", "Transferencia", "Pago"]),
#             "monto": round(random.uniform(-10000, 10000), 2),
#             "descripcion": random.choice(["Depósito en efectivo", "Retiro de cajero automático", "Transferencia a otra cuenta", "Pago de impuestos y servicios"])
#         }
        
#         # Agregar el movimiento a la lista de fechas generadas
#         fechas_generadas.append(movimiento)
    
#     # Crear el JSON final
#     json_generado = {"movimientos": fechas_generadas}
    
#     return json_generado
