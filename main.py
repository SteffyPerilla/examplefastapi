#Python
from os import stat
from typing import Optional
from enum import Enum

#Pydantic 
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status 
from fastapi import Body, Query, Path

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
        ...,
        example="Bogotá" 
        )
    state: Optional[State] = Field(default=None)
    country: str = Field(
        ...,
        example="Colombia"
        ) 

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Cesar"
        )   
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Galindo"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=29
        )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example=HairColor.black
        )
    is_married: Optional[bool] = Field(
        default=None,
        example=False
        )

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="1234esdr"
        )

class PersonOut(PersonBase):
    pass

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello":"World"}

# Request and response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_Length=50,
        title="Person Name",
        description="This is the person name. It's between 1 a 50 characters",
        example="Nathalia"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
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
        description="This is the Person ID. It's required.",
        example=123
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
        gt=0,
        example=123
    ),
    person: Person= Body(...),
    # location: Location = Body(...) 
):
    # results = person.dict() 
    # results.update(location.dict())
    # return results
    return person 
