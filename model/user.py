from sqlalchemy import Table, Column, BigInteger, String, DateTime

from config.db import engine, metadata


users = Table("users", metadata,
    Column("id", BigInteger, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("password", String(255), nullable=False),
    Column("email_verified_at", DateTime, nullable=True),
    Column("remember_token", String(255), nullable=True),
    Column("ultimo_login_new", DateTime, nullable=True),
    Column("ultimo_cambio_password", DateTime, nullable=True),
    Column("created_at", DateTime, nullable=True),
    Column("updated_at", DateTime, nullable=True),
    Column("ultimo_login", DateTime, nullable=True),
)

metadata.create_all(engine)
