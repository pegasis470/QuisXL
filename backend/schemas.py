from pydantic import BaseModel,EmailStr
from typing import Optional

class Login(BaseModel):
    username:str
    password:str


class UserCreate(BaseModel):
    name: str
    phone_number: str
    email_id: EmailStr
    organization: str | None = None
    username: str
    password: str

class validateLogin(BaseModel):
    user_id: int
    auth_token: str

class options(BaseModel):
    A: str
    B: str
    C: str | None = None
    D: str | None = None

class Qustion(BaseModel):
    qus_no: int
    qustion : str
    options: list[options]
    answer : str
    marks:int

class QuizCreate(BaseModel):
    user_id: int
    quizname: str
    qustions : list[Qustion]

class Response(BaseModel):
    qus_no: int
    answer: str

class ResponseCreate(BaseModel):
    quiz_id: int
    user_id: int
    name: str
    standard: str
    data: list[Response] 