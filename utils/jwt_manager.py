from jwt import encode
from jwt import decode
def create_token(data:dict):
    token: str=encode(payload=data,key="my_secrete_key",algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    
        # Decodifica el token utilizando la clave secreta
        data = decode(token, key="my_secrete_key", algorithms=["HS256"])
        return data
    
