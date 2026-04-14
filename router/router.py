from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from schema.user_schema import UserSchema
from model.user import users
from config.db import engine
import bcrypt

BCRYPT_ROUNDS = 10

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hello I am the root of the API"}


@user.post("/api/user")
def create_user(data_user: UserSchema):
    try:
        with engine.connect() as conn:  
            conn.execute(users.insert(), {
                "nombre": data_user.nombre,
                "email": data_user.email,
                "password": bcrypt.hashpw(
                    data_user.password.encode("utf-8"),
                    bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
                ).decode("utf-8"),
            })
            conn.commit()
        # Response() solo admite texto o bytes; un dict hay que devolverlo como JSON.
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={
                "message": "User created successfully",
                "user": {
                    "nombre": data_user.nombre,
                    "email": data_user.email,
                },
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error creating user", "error": str(e)},
        )
