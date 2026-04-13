from fastapi import APIRouter
from schema.user_schema import UserSchema

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hello I am the root of the API"}


@user.post("/api/user")
def create_user(data_user: UserSchema):
    return {"message": "User created successfully", "user": data_user}
