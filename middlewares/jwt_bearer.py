from fastapi.security import HTTPBearer
from utils.jwt_manager import create_token, validate_token
from fastapi import Request, HTTPException

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
       auth=  await super().__call__(request)
       data= validate_token(auth.credentials)
       if data["email"]!="admin@gmail.com":
           raise HTTPException (status_code=403, detail="las credenciales son invalidas")
       