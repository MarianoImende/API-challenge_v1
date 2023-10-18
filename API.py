from ast import Dict
from typing import Union
from documentacion import Cuenta, JsonUserRequest, Movimientos, Tarjeta, documentacion_cuentas, documentacion_mov, documentacion_sesion
from genSaldo import generar_json_saldo
from genTarjetas import generar_json_tarjetas
from genCuentas import generar_json_cuentas
from genUltMovimientos import generarFechas
from fastapi import FastAPI, Header, Request, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import asyncio
from datetime import datetime, timedelta
from jose import jwt, JWTError


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer('/redlink/wallet/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "01330dc7af5264e5ef8f880486dbe52045c0c5f2b060daa372783ff10bacb2d9" # Ideal es que este en una variable de entorno bien oculto (docker@LNKUSR2291:/mnt/c/Users/imendem$ openssl rand -hex 32)
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()
# Variable para realizar un seguimiento del número de solicitudes
request_count = 0
# Estructura para almacenar tokens inhabilitados (puede ser una lista, un conjunto, o una base de datos)
disabled_tokens = set()
# Configura los datos del usuario para demostración (deberías obtener esto de una base de datos)
USERS_DB = {
    "Bhikkhu": {
        "username": "Bhikkhu",
        "hashed_password": "$2b$12$nvhGUIUSyMuQO5ZldkXNXuydM0sFjLo6qiNgaOoXbnGj2e062aUFu", #Redlink*9
        "email" : "eraclito@gmail.com",
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

@app.post('/redlink/wallet/sesion', ** documentacion_sesion())
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
    json.update(generar_json_tarjetas())
    return json

@app.post('/redlink/wallet/cuentas', **documentacion_cuentas())
async def cuentas(tarjeta: Tarjeta,user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    print(token.credentials)
    if not validate_token(token.credentials): #valido la deshabilitacion del token
           raise HTTPException(status_code=401, detail='Token inválido')
         
    if not tarjeta.numero.isdigit() or not tarjeta.numero or not isinstance(tarjeta.numero, str):
       raise HTTPException(status_code=400, detail="El campo 'numero' es inválido.")
    else:  
        return generar_json_cuentas()

@app.post('/redlink/wallet/saldo')
async def saldo(cuenta: Cuenta,user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not cuenta.numero.isdigit() or not cuenta.numero or not isinstance(cuenta.numero, str):
       raise HTTPException(status_code=400, detail="El campo 'numero' es inválido.")
    else:  
       json_generado = generar_json_saldo()
    #body = {"tarjetas":[{"numero":"125055111609","descripcion":"BANCO BICA"},{"numero":"736200459801","descripcion":"BANCO DE SALTA"},{"numero":"872000234502","descripcion":"BANCO LIBRE"}]}
    return json_generado

@app.post('/redlink/wallet/ultmovimientos', **documentacion_mov())
async def ultmovimientos(data: Movimientos, fecha_desde: str, fecha_hasta: str, user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
   
    if not data.numero_cuenta.isdigit() or not data.numero_cuenta:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    
    if len(fecha_desde) != 8 or len(fecha_hasta) != 8:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    try:
        datetime.strptime(fecha_desde, "%Y%m%d")
        datetime.strptime(fecha_hasta, "%Y%m%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    return generarFechas(fecha_desde,fecha_hasta)

@app.post('/billetera/redlink/logout')
async def logout(user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
   
    if token and token.scheme == "Bearer":
        #print("MI TOKEN: " , token)
        # Utiliza token.credentials para acceder al token
        token_value = token.credentials
        # Inhabilita el token agregándolo a la lista de tokens inhabilitados
        disabled_tokens.add(token_value)
        # Devuelve un mensaje indicando que la sesión se ha cerrado exitosamente
    return {" message": "Has cerrado sesión exitosamente"}
    
@app.post('/redlink/wallet/estado')
async def estado(user: User = Depends(get_user_disable_current),token: HTTPAuthorizationCredentials = Depends(auth_scheme)):#str = Depends(oauth2_scheme) determina que la ruta es privada
    
    return user
