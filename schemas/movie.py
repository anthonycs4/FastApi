from pydantic import BaseModel, Field
from typing import  Optional, List

class sch_movie_data(BaseModel):
    id: Optional[int]=None
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
