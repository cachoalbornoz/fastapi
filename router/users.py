from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from sqlalchemy import select
from typing import List
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
        row = {
            "nombre": data_user.nombre,
            "email": data_user.email,
            "password": bcrypt.hashpw(
                data_user.password.encode("utf-8"),
                bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
            ).decode("utf-8"),
        }
        for key in (
            "email_verified_at",
            "remember_token",
            "ip_acceso",
            "user_agent",
            "ultimo_login_new",
            "ultimo_cambio_password",
            "created_at",
            "updated_at",
            "ultimo_login",
        ):
            value = getattr(data_user, key)
            if value is not None:
                row[key] = value

        with engine.connect() as conn:
            conn.execute(users.insert(), row)
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


@router.get("/api/user/{id}", response_model=UserSchema)
def get_user(id: int):
    try:
        with engine.connect() as conn:
            stmt = select(users).where(users.c.id == id)
            result = conn.execute(stmt).fetchone()
            if result is None:
                return JSONResponse(
                    status_code=HTTP_404_NOT_FOUND,
                    content={"detail": "User not found"},
                )
            user_dict = dict(result._mapping)
            return JSONResponse(
                status_code=HTTP_200_OK,
                content={"user": jsonable_encoder(user_dict)},
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error getting user", "error": str(e)},
        )

@router.get("/api/users", response_model=List[UserSchema])
def get_users():
    try:
        with engine.connect() as conn:
            stmt = select(
                users.c.id,
                users.c.nombre,
                users.c.email,
                users.c.ultimo_login,
                users.c.ip_acceso,
                users.c.user_agent,
                users.c.created_at,
                users.c.updated_at,
            )
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
