#Python
from _typeshed import SupportsRDivMod
from typing import Optional, get_type_hints
from enum import Enum

#Pydantic 
from pydantic import BaseModel
from pydantic import Field, EmailStr, HttpUrl

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
from pydantic.schema import field_schema 

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class State(Enum):
    Sur = "Sur"
    Este = "Este"
    Oeste = "Oeste"
    Norte = "Norte"

class Location(BaseModel):
    city: str = Field(
        ... 
    )
    state: Optional[State] = Field(default=None)
    country: str = Field(
        ...
    ) 

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )   
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    email : EmailStr = Field(...)
    website_Url : Optional[HttpUrl] = Field(default=None)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

@app.get("/")
def home():
    return {"Hello":"World"}

# Request and response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_Length=50,
        title="Person Name",
        description="This is the person name. It's between 1 a 50 characters"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
):
    return {name:age}

#Validaciones: Path Parameters 

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the Person ID. It's required."
        )
):
    return {person_id:"It Exists!"}

#Validaciones: Request Body 

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person Id",
        description="This is the person ID",
        gt=0
    ),
    person: Person= Body(...),
    location: Location = Body(...) 
):
    results = person.dict() 
    results.update(location.dict())
    return results 