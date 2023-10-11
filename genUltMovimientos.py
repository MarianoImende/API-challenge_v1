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
        
        # Crear un diccionario para el movimiento
        movimiento = {
            "fecha": fecha_formateada,
            "tipo": random.choice(["Depósito", "Retiro", "Transferencia", "Pago"]),
            "monto": round(random.uniform(-1000, 1000), 2),
            "descripcion": random.choice(["Depósito en efectivo", "Retiro de cajero automático", "Transferencia a otra cuenta", "Pago de impuestos y servicios"])
        }
        
        # Agregar el movimiento a la lista de fechas generadas
        fechas_generadas.append(movimiento)
    
    # Crear el JSON final
    json_generado = {"movimientos": fechas_generadas}
    
    return json_generado

#modelo argentino
# import locale
# import random
# from datetime import datetime, timedelta

# def generarFechas(fecha_desde, fecha_hasta):
    
#     locale.setlocale(locale.LC_TIME, 'es_AR.UTF-8')
#     # Convertir las fechas de cadena a objetos datetime

#     fecha_desde_str = datetime.strptime(fecha_desde, "%d/%m/%Y")
#     fecha_hasta_str = datetime.strptime(fecha_hasta, "%d/%m/%Y")
#     fechas_generadas = []
    
#     for _ in range(5):  # Generar cinco fechas
#         # Generar un número aleatorio de días entre fecha_desde y fecha_hasta
#         diferencia_dias = (fecha_hasta_str - fecha_desde_str).days
#         dias_aleatorios = random.randint(0, diferencia_dias)
        
#         # Calcular la fecha aleatoria
#         fecha_generada = fecha_desde_str + timedelta(days=dias_aleatorios)
        
#         # Formatear la fecha como "dd-mm-yyyy"
#         fecha_formateada = fecha_generada.strftime("%d-%m-%Y")
        
#         # Crear un diccionario para el movimiento
#         movimiento = {
#             "fecha": fecha_formateada,
#             "tipo": random.choice(["Depósito", "Retiro", "Transferencia", "Pago"]),
#             "monto": round(random.uniform(-1000, 1000), 2),
#             "descripcion": random.choice(["Depósito en efectivo", "Retiro de cajero automático", "Transferencia a otra cuenta", "Pago de impuestos y servicios"])
#         }
        
#         # Agregar el movimiento a la lista de fechas generadas
#         fechas_generadas.append(movimiento)
    
#     # Crear el JSON final
#     json_generado = {"movimientos": fechas_generadas}
    
#     return json_generado

# # fecha_desde_str = "01/01/2023"
# # fecha_hasta_str = "30/01/2023"
# # print(generarFechas(fecha_desde_str,fecha_hasta_str))