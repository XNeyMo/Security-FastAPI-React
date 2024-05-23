from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import jwt

from routes.product import router as product_router

app = FastAPI()

# Configura CORS
origins = [
    "http://localhost:3000",
    "https://liav.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la clave secreta del token JWT del archivo .env
JWT_SECRET = os.getenv("JWT_SECRET")

# Middleware para verificar el token JWT en las rutas protegidas
def verify_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    print(JWT_SECRET)
    print(token)
    if token != JWT_SECRET:
        raise HTTPException(status_code=401, detail="Token inválido")

# Incluye los endpoints de routes.product con la autenticación requerida
app.include_router(
    product_router,
    prefix="/product",
    dependencies=[Depends(verify_token)]
)
