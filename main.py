from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app=FastAPI()
app.version = "0.1.0"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) :
       auth=  await super().__call__(request)
       data= validate_token(auth.credentials)
       if data["email"]!="admin@gmail.com":
           raise HTTPException (status_code=403, detail="las credenciales son invalidas")
       
           

class User(BaseModel):
    email: str 
    password: str 

#Eschema
class sch_movie_data(BaseModel):
    id: int
    title: str= Field(min_length=5, max_length=15)
    overview: str= Field(min_length=10, max_length=30)
    year: int = Field(le=2024)
    rating: float= Field(ge=1,le=10)
    category: str= Field(min_length=5, max_length=10)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "MiPelicula",
                    "overview": "MiDescripcion",
                    "year": 2022,
                    "rating": 9.8,
                    "category": "action"
                }
            ]
        }
    }

movies_data = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }, {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Comedia"
    }, {
        "id": 3,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Terror"
    }
]

@app.get ("/",tags=["hola"])
async def run():
    return {"hola":"hola"}

@app.get("/movies", tags=["movies"], response_model=list[sch_movie_data], status_code=200,dependencies=[Depends(JWTBearer())])
def movies()->list[sch_movie_data]:
    return JSONResponse(content=movies_data,status_code=200)

@app.get("/movies/{id}",tags=["movies"], response_model=sch_movie_data,status_code=404)
def get_movies(id: int=Path(ge=1,le=10))->sch_movie_data:
    for item in movies_data:
        if item["id"]==id:
            return JSONResponse(content=item)
    return JSONResponse(content=[], status_code=404)

@app.get("/movies/",tags=["movies"], response_model=list[sch_movie_data], status_code=200)
def get_movies_by_category(category:str= Query(min_length=5,max_length=15))->list[sch_movie_data]:
    #es una linea for "item" es lo que devolvera y de ahi todo esta conectado por order high
    data=[item for item in movies_data if item["category"]==category]
    return JSONResponse(content=data,status_code=200)

@app.post("/movies",tags=["movies"], response_model=dict,status_code=201)
def create_movie(movie: sch_movie_data)->dict:
    movies_data.append(movie)
    return JSONResponse(content={"mensaje": "Se agrego correctamente"},status_code=201)

@app.delete("/movies",tags=["movies"], response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    for items in movies_data:
        if items["id"]==id:
            movies_data.remove(items)
        return JSONResponse(content={"mensaje": "Seborro correctamente"},status_code=200)
    '''
    OTRA OPCION:

    global movies_data
    movies_data=[item for item in movies_data if item["id"]!=id]
    return movies_data
    '''
    


@app.put("/movies",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int, movie: sch_movie_data )->dict:
    for items in movies_data:
        if items["id"]==id:
            items["title"]=movie.title
            items["overview"]=movie.overview
            items["year"]=movie.year
            items["rating"]=movie.rating
            items["category"]=movie.category
        return JSONResponse(content={"mensaje": "Se modifico correctamente"},status_code=200)

#Logeo
@app.post("/login",tags=["auth"])
def login(user:User):
    if user.email=="admin@gmail.com" and user.password=="admin":
        token: str=create_token(user.dict())
        return JSONResponse(status_code=200,content=token)