from ast import Dict

from pydantic import BaseModel
    
class JsonUserRequest(BaseModel):
    username: str
    password: str
    
def documentacion_sesion() -> Dict:

        documentation = {
        "summary": "Crear un nuevo token",
        "description": "Ejemplo de solicitud:",
        #"response_model": JsonUserRequest,
        "response_description": "Access token creado satisfactoriamente",
        "responses": {
            200: {
                "description": "Token creado satisfactoriamente",
                "content": {
                    "application/json": {
                        "example": {"access_token": "My token", "token_type": "My type"}
                    }
                }
            },
            401: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se pudo validar las credenciales"}
                    }
                }
            }
        }
    }
        return documentation

#--------------------------------------------------------------------------------
class Tarjeta(BaseModel):
    numero: str
    
def documentacion_cuentas() -> Dict:

        documentation = {
        "summary": "Obtiene cuentas",
        "description": "Ejemplo de solicitud:",
        #"response_model": JsonUserRequest,
        "response_description": "listado de cuentas asociadas a la tarjeta",
        "responses": {
            200: {
                "description": "Cuentas obtenida satisfactoriamente",
                "content": {
                    "application/json": {
                        #"example": {"access_token": "My token", "token_type": "My type"}
                        "example": {"cuentas": [{"numero": "123456789", "tipo": "CA USD"}]}
                    }
                }
            },
            401: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se ha enviado el numero de tarjeta"}
                    }
                }
            }
        }
    }
        return documentation
    
    
#--------------------------------------------------------------------------------
class Cuenta(BaseModel):
    numero: str
    
def documentacion_saldo() -> Dict:

        documentation = {
        "summary": "Obtiene saldo",
        "description": "Ejemplo de solicitud:",
        #"response_model": JsonUserRequest,
        "response_description": "Informa el saldo de la cuenta",
        "responses": {
            200: {
                "description": "saldo obtenido satisfactoriamente",
                "content": {
                    "application/json": {
                        "example": {"saldo": "My saldo"}
                    }
                }
            },
            401: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "No se ha enviado el numero de cuenta"}
                    }
                }
            }
        }
    }
        return documentation
    
        
#--------------------------------------------------------------------------------
class Movimientos(BaseModel):
    numero_cuenta: str

    
def documentacion_mov() -> Dict:

        documentation = {
        "summary": "Obtiene los movimientos por rango de fechas",
        "description": "Ejemplo de solicitud:",
        #"response_model": JsonUserRequest,
        "response_description": "Informa los movimientos de la cuenta",
        "responses": {
            200: {
                "description": "Movimientos obtenidos satisfactoriamente",
                "content": {
                    "application/json": {
                        
                        "example": {"movimientos": [{"fecha": "20230131", "tipo": "Pago", "monto": "-853.99", "descripcion": "Retiro de cajero automático"}]}
                       
                    }
                }
            },
            401: {
                "description": "Error",
                "content": {
                    "application/json": {
                        "example": {"detail": "Datos inválidos"}
                    }
                }
            }
        }
    }
        return documentation
    
