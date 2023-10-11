# ALTO RENDIMIENTO
# GENERA DOCUMENTACIÓN AUTOMÁTICA
# VALIDACIÓN DE DATOS (PARÁMETROS OPCIONALES)

from typing import Union
from genSaldo import generar_json_saldo
from genTarjetas import generar_json_tarjetas
from genCuentas import generar_json_cuentas
from genUltMovimientos import generarFechas

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
# Variable para realizar un seguimiento del número de solicitudes
request_count = 0

# Configura los datos del usuario para demostración (deberías obtener esto de una base de datos)
USERS_DB = {
    "empedocles": {
        "username": "empedocles",
        "hashed_password": "$2b$12$nvhGUIUSyMuQO5ZldkXNXuydM0sFjLo6qiNgaOoXbnGj2e062aUFu", #Redlink*9
        "email" : "lola@gmail.com",
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

def get_User(db, username):
  if username in db:
       user_data = db[username]
       return UserInDB(**user_data)
  else:
       return[]
   
def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)
    
#trae el usuario propiamente dicho
def get_user(db,username):
    if username in db:
        user_data = db[username]
        return User(**user_data)
    return[]

#valida la existencia del usuario y password
def autenticate_user(db,username,password):
    user = get_User(db, username)
    if isinstance(user, User) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    if verify_password(password, user.hashed_password) == False:
        raise HTTPException(status_code=401, detail='No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    print(time_expire)
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
        print("get_user_current:" + username)
        if username is None:
             raise HTTPException(status_code=401, detail='1-No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
             raise HTTPException(status_code=401, detail='2-No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    user = get_user(USERS_DB,username)     
    if not user:
        raise HTTPException(status_code=401, detail='3-No se pudo validar las credenciales', headers={"WWW-Authenticate": "Bearer"})
    return user

#garantiza que el token no haya expirado
def get_user_disable_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user

@app.post('/redlink/wallet/sesion')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticate_user(USERS_DB, form_data.username, form_data.password)
    print(user.username)
    access_token_expires = timedelta(minutes=30)
    access_token_JWT = create_token({"sub": user.username}, access_token_expires)
    return {
            "access_token": access_token_JWT,
            "token_type": "bearer"}

@app.post('/redlink/wallet/estado')
async def estado(user: User = Depends(get_user_disable_current)):#str = Depends(oauth2_scheme) determina que la ruta es privada
    
    return User 
    # global request_count  # Accede a la variable global, es la que esta afuera.
    # request_count += 1  # Incrementar el conteo de solicitudes
    # base_delay = 0.2  # Tiempo de demora inicial en segundos
    # exponential_factor = 0.001  # Factor exponencial para ajustar la velocidad de aumento
    # # Calcular el tiempo de demora utilizando una fórmula exponencial
    # delay_seconds = base_delay * (2 ** (exponential_factor * request_count))
    # # Aplica la demora utilizando asyncio.sleep
    # await asyncio.sleep(delay_seconds)
    # json_generado = generar_json_tarjetas()
    # return json_generado

@app.post('/redlink/wallet/cuentas')
async def cuentas(request: Request,user: User = Depends(get_user_disable_current), nrotarjeta: str = None):
    # global request_count  # Accede a la variable global
    # request_count += 1  # Incrementar el conteo de solicitudes
    # base_delay = 0.2  # Tiempo de demora inicial en segundos
    # exponential_factor = 0.002  # Factor exponencial para ajustar la velocidad de aumento
    # # Calcular el tiempo de demora utilizando una fórmula exponencial
    # delay_seconds = base_delay * (2 ** (exponential_factor * request_count))
    # # Aplica la demora utilizando asyncio.sleep
    # await asyncio.sleep(delay_seconds)
    # Verifica si 'nrotarjeta' está presente en los datos
    if nrotarjeta is not None:
        return generar_json_cuentas()
        #return {"nrotarjeta": nrotarjeta}
    else:
        return {"error": "El parámetro 'nrotarjeta' no está presente en la URL"}

@app.post('/redlink/wallet/saldo')
async def saldo(request: Request,user: User = Depends(get_user_disable_current)):
    # global request_count  # Accede a la variable global
    # request_count += 1  # Incrementar el conteo de solicitudes
    # base_delay = 0.3  # Tiempo de demora inicial en segundos
    # exponential_factor = 0.003  # Factor exponencial para ajustar la velocidad de aumento
    # # Calcular el tiempo de demora utilizando una fórmula exponencial
    # delay_seconds = base_delay * (2 ** (exponential_factor * request_count))
    # # Aplica la demora utilizando asyncio.sleep
    # await asyncio.sleep(delay_seconds)
    # # print(request.headers)
    json_generado = generar_json_saldo()
    #body = {"tarjetas":[{"numero":"125055111609","descripcion":"BANCO BICA"},{"numero":"736200459801","descripcion":"BANCO DE SALTA"},{"numero":"872000234502","descripcion":"BANCO LIBRE"}]}
    return json_generado

@app.post('/redlink/wallet/ultmovimientos')
async def ultmovimientos(fecha_desde: str, fecha_hasta: str, user: User = Depends(get_user_disable_current)):
    # global request_count  # Accede a la variable global
    # request_count += 1  # Incrementar el conteo de solicitudes
    # base_delay = 0.1  # Tiempo de demora inicial en segundos
    # exponential_factor = 0.004  # Factor exponencial para ajustar la velocidad de aumento
    # # Calcular el tiempo de demora utilizando una fórmula exponencial
    # delay_seconds = base_delay * (2 ** (exponential_factor * request_count))
    # # Aplica la demora utilizando asyncio.sleep
    # await asyncio.sleep(delay_seconds)
    
    # bodyjson = await request.json()
    # fecha_desde = bodyjson["fecha desde"]
    # fecha_hasta = bodyjson["fecha hasta"]
    return generarFechas(fecha_desde,fecha_hasta)

@app.post('/billetera/redlink/logout')
async def logout(user: User = Depends(get_user_disable_current)):
    # global request_count  # Accede a la variable global
    # request_count += 1  # Incrementar el conteo de solicitudes
    # base_delay = 0.01  # Tiempo de demora inicial en segundos
    # exponential_factor = 0.001  # Factor exponencial para ajustar la velocidad de aumento
    # # Calcular el tiempo de demora utilizando una fórmula exponencial
    # delay_seconds = base_delay * (2 ** (exponential_factor * request_count))
    # # Aplica la demora utilizando asyncio.sleep
    # await asyncio.sleep(delay_seconds)
    #raise HTTPException(status_code=500, detail="Error interno del servidor")
    return {"message": "Has cerrado sesion exitosamente"}
    


