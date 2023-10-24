from typing import Union
from documentacion import Cuenta, JsonUserRequest, Movimientos, Tarjeta, documentacion_cuentas, documentacion_mov, documentacion_sesion
from genSaldo import generar_json_saldo
from genTarjetas import generar_json_tarjetas
from genCuentas import generar_json_cuentas
from genUltMovimientos import generarFechas
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import asyncio
from datetime import datetime, timedelta
from jose import jwt, JWTError

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer('/wallet/sesion')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "01330dc7af5264e5ef8f880486dbe52045c0c5f2b060daa372783ff10bacb2d9" # Ideal es que este en una variable de entorno bien oculto (openssl rand -hex 32)
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()
# Variable para realizar un seguimiento del número de solicitudes
request_count = 0
# Estructura para almacenar tokens inhabilitados (puede ser una lista, un conjunto, o una base de datos)
disabled_tokens = set()
# Configura los datos del usuario para demostración (deberías obtener esto de una base de datos)
USERS_DB = {
    "challenge": {
        "username": "challenge",
        "hashed_password": "$2b$12$NLrNyrG528pi3U7f42FnJuxOV3pA61f5u.0bvkI/xoJ3cOAEmTLDG", #
        "email" : "challenge@challenge.com.ar",
        "disabled" : False,
        
    },
    "prueba": {
        "username": "prueba",
        "hashed_password": "$2b$12$NLrNyrG528pi3U7f42FnJuxOV3pA61f5u.0bvkI/xoJ3cOAEmTLDG", #
        "email" : "prueba@challenge.com.ar",
        "disabled" : False,
        
    }
}

#esquema para los usuarios generales
class User(BaseModel):
  username:str
  email:Union[str, None] = None
  disabled:Union[bool, None] = None

#para los usuarios existentes
class UserInDB(User):
  hashed_password:str

  
def get_user(db,username):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    return[]

 
def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)
    

#valida la existencia del usuario y password
def autenticate_user(db,username,password):
    user = get_user(db, username)
    if isinstance(user, User) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    if verify_password(password, user.hashed_password) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)#valor predeterminado
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_JWT = jwt.encode(data_copy, key=SECRET_KEY,algorithm=ALGORITHM)
    return token_JWT

#función que obtiene el username dentro del token JWT
def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
             raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
             raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    user = get_user(USERS_DB,username)     
    if not user:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

#garantiza que el token no haya expirado
def get_user_disable_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user

# Middleware para validar el token en rutas protegidas
def validate_token(token: str):
    if token in disabled_tokens:
        # El token se encuentra en la lista de tokens inhabilitados, se considera inválido
        return False
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
            return False
    except JWTError:
        return False
    return True

@app.post('/wallet/sesion', ** documentacion_sesion())
async def token(data: JsonUserRequest):
#async def token(data: dict, da: TokenRequest):
    username = data.username # data.get("username")
    password = data.password #data.get("password")
    
    user = autenticate_user(USERS_DB, username,password)
#     async def token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = autenticate_user(USERS_DB, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_JWT = create_token({"sub": user.username}, access_token_expires)
    json = {
            "access_token": access_token_JWT,
            "token_type": "bearer",
            "access_token_expires": access_token_expires}
    if username == "challenge":
        json.update({"tarjetas": [{"descripcion": "BANCO HIPOTECARIO", "numero": "825840853443"}, {"descripcion": "BANCO HSBC", "numero": "423455721156"}, {"descripcion": "BANCO DE LA PROVINCIA DE BUENOS AIRES", "numero": "595278769781"}]})
    else:
        json.update(generar_json_tarjetas())
        
    return json

@app.post('/wallet/cuentas', **documentacion_cuentas())
async def cuentas(tarjeta: Tarjeta,user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
         
    if not tarjeta.numero_tarjeta.isdigit() or not tarjeta.numero_tarjeta or not isinstance(tarjeta.numero_tarjeta, str):
       raise HTTPException(status_code=400, detail="El campo 'numero_tarjeta' es inválido.")
    
    
    if user.username == "challenge":    
     
      if tarjeta.numero_tarjeta == "825840853443":
            return {"cuentas": [{"numero_cuenta": "99083422", "tipo": "CC $"}, {"numero_cuenta": "96703737", "tipo": "CC $"}, {"numero_cuenta": "93125576", "tipo": "CA USD"}]}
      elif tarjeta.numero_tarjeta == "423455721156":
            return {"cuentas": [{"numero_cuenta": "1209383422", "tipo": "CA $"}]}
      elif tarjeta.numero_tarjeta == "595278769781":
            return {"cuentas": [{"numero_cuenta": "34948473811", "tipo": "CC $"},{"numero_cuenta": "102033534534521", "tipo": "CA $"}]}
          #else:
        # si sale por aui, devuelve null, es un error apropósito.
    else:
     return generar_json_cuentas()

@app.post('/wallet/saldo')
async def saldo(cuenta: Cuenta,user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
    
    if not cuenta.numero_cuenta.isdigit() or not cuenta.numero_cuenta or not isinstance(cuenta.numero_cuenta, str):
       raise HTTPException(status_code=400, detail="El campo 'numero' es inválido.")
    
    if user.username == "challenge":
        if cuenta.numero_cuenta == "99083422":
            return {"saldo": "$1.966,78"}
        elif cuenta.numero_cuenta == "96703737":
            return {"saldo": "$7.246,18"}
        elif cuenta.numero_cuenta == "93125576":
            return {"saldo": "USD109.940,00"}#-------------
        elif cuenta.numero_cuenta == "1209383422":
            return {"saldo": "$19.209,19"}
        elif cuenta.numero_cuenta == "34948473811":
            return {"saldo": "$0.000,00"}
        elif cuenta.numero_cuenta == "102033534534521":
            return {"saldo": "$150498.000,00"}
    else:
        json_generado = generar_json_saldo()
        return json_generado
    
    
@app.post('/wallet/ultmovimientos', **documentacion_mov())
async def ultmovimientos(mov: Movimientos, fecha_desde: str, fecha_hasta: str, user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
   
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
       
    if not mov.numero_cuenta.isdigit() or not mov.numero_cuenta:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    
    if len(fecha_desde) != 8 or len(fecha_hasta) != 8:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    try:
        datetime.strptime(fecha_desde, "%Y%m%d")
        datetime.strptime(fecha_hasta, "%Y%m%d")
    except ValueError:
            raise HTTPException(status_code=400, detail="Datos inválidos")
    
    if user.username == "challenge":
        if mov.numero_cuenta == "99083422":
            return {"movimientos": [{"fecha": "20230931", "monto": -2878.73, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230831", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20231201", "monto": -2818.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230702", "monto": 3375.00, "descripcion": "Transferencia Credito"}, {"fecha": "20230131", "monto": -9009.80, "descripcion": "Compra"}]}
        elif mov.numero_cuenta == "96703737":
            return {"movimientos": [{"fecha": "20230123", "monto": 10828.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230831", "monto": -1182.17, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230121", "monto": 2575.53, "descripcion": "Compra"}, {"fecha": "20230111", "monto": -9339.8, "descripcion": "Compra"}]}
        elif mov.numero_cuenta == "93125576":
            return {"movimientos": [{"fecha": "20231005", "monto": -118.00, "descripcion": "Retiro de cajero automático"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25575.43, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -9339.00, "descripcion": "Pago de impuestos y servicio"}]}
        elif mov.numero_cuenta == "1209383422":
            return {"movimientos": [{"fecha": "20231205", "monto": 5578.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25575.43, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -9339.00, "descripcion": "Pago de impuestos y servicio"}]}   
        elif mov.numero_cuenta == "34948473811":
            return {"movimientos": [{"fecha": "20231205", "monto": 78.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230114", "monto": -2808.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -1.16, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -28158.21, "descripcion": "Retiro de cajero automático"},{"fecha": "20230114", "monto": -28308.10, "descripcion": "Ingreso en efectivo"}, {"fecha": "20231121", "monto": -31.56, "descripcion": "Ingreso en efectivo"}, {"fecha": "20230131", "monto": -818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230131", "monto": 25075.40, "descripcion": "Depósito en efectivo"}, {"fecha": "20221028", "monto": -7399.00, "descripcion": "Pago de impuestos y servicio"}]}      
        elif mov.numero_cuenta == "102033534534521":
            return {"movimientos": [{"fecha": "20230123", "monto": 10828.00, "descripcion": "Plazo Fijo ingreso"},{"fecha": "20230831", "monto": -1182.17, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2382.16, "descripcion": "Compra"}, {"fecha": "20230131", "monto": -2818.21, "descripcion": "Retiro de cajero automático"}, {"fecha": "20230121", "monto": 2575.53, "descripcion": "Compra"}, {"fecha": "20230111", "monto": -9339.8, "descripcion": "Compra"}]}
    else:    
            return generarFechas(fecha_desde,fecha_hasta)

@app.post('/wallet/logout')
async def logout(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')  
       
    if token and token.scheme == "Bearer":
        # Utiliza token.credentials para acceder al token
        token_value = token.credentials
        # Inhabilita el token agregándolo a la lista de tokens inhabilitados
        disabled_tokens.add(token_value)
        # Devuelve un mensaje indicando que la sesión se ha cerrado exitosamente
    return {" message": "Has cerrado sesión exitosamente"}
    
@app.get('/wallet/estado')
async def estado(user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):#str = Depends(oauth2_scheme) determina que la ruta es privada
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
    return user
