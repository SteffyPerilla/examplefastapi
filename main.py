#Python
from os import path
from typing import Optional
from enum import Enum

#Pydantic 
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException  
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example="SteffyPerilla")
    message : str =Field(default="Login Succesfully")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home():
    return {"Hello":"World"}

# Request and response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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

persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the Person ID. It's required.",
        example=123
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesnt exist!"
        )  
    return {person_id:"It Exists!"}

#Validaciones: Request Body 

@app.put(
    path="/person/{person_id}",
    tags=["Persons"]
    )
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

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username : str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#Cookies and Headers

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
)
def contact(
    first_name: str = Form(
        ...,
        max_lenght=20,
        min_lenght=1
    ),
    last_name: str = Form(
        ...,
        max_lenght=20,
        min_lenght=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_lenght=20 
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent 

# File

@app.post(
    path="/post-image",
    tags=["Documents"]   
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename:" : image.filename,
        "Format: " : image.content_type,
        "Size(kb): " : round(len(image.file.read())/1024, ndigits=2) 
    } 