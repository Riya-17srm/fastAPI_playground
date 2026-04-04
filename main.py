from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

@app.get("/")
def read_root():
    return {
        "Message":"Hello World"
        }

@app.get("/greet")
def greet():
    return {"Message":"Hello Sam"}

@app.get("/greet/{name}")
def greet_name(name:str, age:Optional[int]=None):
    return {"Message":f"Hello {name}, you are {age} years old"}

@app.get("/try_query")
def greet_query(name:Optional[str]=None, age:Optional[int]=None):
    return {"Message":f"Hello {name}, you are {age} years old"}


class Student(BaseModel):
    name:str
    age:int
    roll:int

@app.post("/create_student")
def create_student(student: Student):
    return {
        "name":student.name,
        "age":student.age,
        "roll":student.roll

    }