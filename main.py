#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models


class HairColor(Enum):
    white = "white"
    brown = "bron"
    black = "yellow"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="El Angel"
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Carchi"
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Ecuador"
        )

class PersonBase(BaseModel);
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Jona"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Urresta"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=21
        )
    hair_color: Optional[HairColor] = Field(default=None, example="yellow")
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    
    password: str = Field(...,min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name" : "Jonathan",
    #             "last_name": "Narvaez Urresta",
    #             "age": 22,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }


class PersonOut(PersonBase):
    pass

@app.get("/")
def home():
    return {"Hola": "mundo"}


#Request and Response Body

@app.post("/person/new", response_mode=PersonOut)
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Jessie"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
):
    return {name: age}

#Valaciaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...
        , gt=0,
        title="Person id",
        description="This is the person id. It's required",
        example=123
        )
    
):
    return {person_id: "It exists"}

#Validaciones: Request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description = "This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person