from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
app=FastAPI()
app.version = "0.1.0"
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

@app.get("/movies", tags=["movies"])
def movies():
    return movies

@app.get("/movies/{id}",tags=["movies"])
def get_movies(id: int):
    for item in movies_data:
        if item["id"]==id:
            return item
    return []

@app.get("/movies/",tags=["movies"])
def get_movies_by_category(category:str, year: int):
    #es una linea for "item" es lo que devolvera y de ahi todo esta conectado por order high
    return[item for item in movies_data if item["category"]==category]

@app.post("/movies",tags=["movies"])
def create_movie(id:int=Body(), title:str=Body(), overview:str=Body(), year:int=Body(), rating:float=Body(), category: str=Body() ):
    movies_data.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies_data

@app.delete("/movies",tags=["movies"])
def delete_movie(id:int):
    for items in movies_data:
        if items["id"]==id:
            movies_data.remove(items)
        return movies_data
    '''
    global movies_data
    movies_data=[item for item in movies_data if item["id"]!=id]
    return movies_data
    '''
    


@app.put("/movies",tags=["movies"])
def update_movie(id:int, title:str=Body(), overview:str=Body(), year:int=Body(), rating:float=Body(), category: str=Body() ):
    for items in movies_data:
        if items["id"]==id:
            items["title"]=title,
            items["overview"]=overview,
            items["year"]=year,
            items["rating"]=rating,
            items["category"]=category
        return movies_data

