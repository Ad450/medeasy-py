from fastapi import FastAPI
from pydantic import BaseModel

from application.dto import RegisterUserDto
from application.services.auth_service import AuthenticationService

app = FastAPI()


@app.post(path="/auth/register")
def greet_hello(userDto: RegisterUserDto):
    return AuthenticationService().register(dto=userDto)


# @app.get(path="/hello/{name}")
# def greet_you(name: str, age: int | None = None):
#     return {
#         "Greeting": f"Hellow {name}",
#         "Age": age if age is not None else "No age given"
#     }


# @app.get(path="/process")
# def greet_you(name: str | None = None):
#     if name:
#         return {"Process": f"Processing {name}"}
#     return {"Process": "oops no name"}


# @app.post(path="/user")
# def create_user(user: UserDto):
#     users.append(user)
#     return {"result": "user created"}
