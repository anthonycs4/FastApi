from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import  JSONResponse
from typing import   List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import sch_movie_data
movie_router=APIRouter()



@movie_router.get("/movies", tags=["movies"], response_model=list[sch_movie_data], status_code=200,dependencies=[Depends(JWTBearer())])
def movies()->list[sch_movie_data]:
    
    db=Session()
    result=MovieService(db).get_movies()
    
    return JSONResponse(content=jsonable_encoder(result),status_code=200)

@movie_router.get("/movies/{id}",tags=["movies"], response_model=sch_movie_data,status_code=404)
def get_movies(id: int=Path(ge=1,le=10))->sch_movie_data:
   db=Session()
   result=MovieService(db).get_movie(id)
   if not result:
       return JSONResponse(content={"message":"no encontrado"}, status_code=404)

   # for item in movies_data:
    #    if item["id"]==id:
     #       return JSONResponse(content=item)
   return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/",tags=["movies"], response_model=list[sch_movie_data], status_code=200)
def get_movies_by_category(category:str= Query(min_length=5,max_length=15))->list[sch_movie_data]:
    #es una linea for "item" es lo que devolvera y de ahi todo esta conectado por order high
    #data=[item for item in movies_data if item["category"]==category]
    db=Session()
    result=MovieService(db).get_movie_by_category(category)
    return JSONResponse(content=jsonable_encoder(result),status_code=200)

@movie_router.post("/movies",tags=["movies"], response_model=dict,status_code=201)
def create_movie(movie: sch_movie_data)->dict:
    db=Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"mensaje": "Se agrego correctamente"},status_code=201)

@movie_router.delete("/movies",tags=["movies"], response_model=dict,status_code=200)
def delete_movie(id:int)->dict:
    db=Session()
    result:MovieModel=  db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message": "no encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"mensaje": "Seborro correctamente"},status_code=200)
    '''
    OTRA OPCION:

    global movies_data
    movies_data=[item for item in movies_data if item["id"]!=id]
    return movies_data
    '''
    


@movie_router.put("/movies",tags=["movies"],response_model=dict,status_code=200)
def update_movie(id:int, movie: sch_movie_data )->dict:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message": "no encontrado"})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(content={"mensaje": "Se modifico correctamente"},status_code=200)
