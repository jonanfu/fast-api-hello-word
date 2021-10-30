#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status
from fastapi import HTTPException

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

class PersonBase(BaseModel):
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

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="miguel2021"
        )

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home():
    return {"Hola":"mundo"}


#Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Person"],
    summary="Create person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation create a person in de the app and save the information in the database
    
    Parameters:
    - Request body parameters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Person"]
    )
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

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Person"]
    )
def show_person(
    person_id: int = Path(
        ...
        , gt=0,
        title="Person id",
        description="This is the person id. It's required",
        example=123
        )
    
):
    if person_id not in person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    return {person_id: "It exists"}

#Validaciones: Request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Person"]
    )
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

#forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Person", "Login"]
)
def login(
    username: str = Form(...),
    password: str = Form(...) 
    ):
    return LoginOut(username=username)

#Cookies and Headers

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contac", "Cookies"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

#Files

@app.post(
    path="/post-image",
    status_code=status.HTTP_201_CREATED,
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": len(image.file.read()/1024, ndigits=2)
    }

