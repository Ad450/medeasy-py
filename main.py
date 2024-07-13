from fastapi import FastAPI
from pydantic import BaseModel


class UserDto(BaseModel):
    username: str
    age: int | None
    email: str
    profile_picture: str | None


app = FastAPI()

users: list[UserDto] = []


@app.get(path="/hello")
def greet_hello():
    return {"Greeting": "hello"}


@app.get(path="/hello/{name}")
def greet_you(name: str, age: int | None = None):
    return {
        "Greeting": f"Hellow {name}",
        "Age": age if age is not None else "No age given"
    }


@app.get(path="/process")
def greet_you(name: str | None = None):
    if name:
        return {"Process": f"Processing {name}"}
    return {"Process": "oops no name"}


@app.post(path="/user")
def create_user(user: UserDto):
    users.append(user)
    return {"result": "user created"}
