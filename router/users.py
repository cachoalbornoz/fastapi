from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from sqlalchemy import select
from schema.user_schema import UserSchema
from model.user import users
from config.db import engine
import bcrypt

BCRYPT_ROUNDS = 10

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello I am the root of the API"}


@router.post("/api/user")
def create_user(data_user: UserSchema):
    try:
        with engine.connect() as conn:
            conn.execute(
                users.insert(),
                {
                    "nombre": data_user.nombre,
                    "email": data_user.email,
                    "password": bcrypt.hashpw(
                        data_user.password.encode("utf-8"),
                        bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
                    ).decode("utf-8"),
                },
            )
            conn.commit()
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


@router.get("/api/users")
def get_users():
    try:
        with engine.connect() as conn:
            stmt = select(users.c.id, users.c.nombre, users.c.email, users.c.ultimo_login)
            result = conn.execute(stmt).fetchall()
            user_list = [dict(row._mapping) for row in result]
            return JSONResponse(
                status_code=HTTP_200_OK,
                content={"users": jsonable_encoder(user_list)},
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error getting users", "error": str(e)},
        )
