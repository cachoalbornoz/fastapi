from sqlalchemy import Table, Column, Integer, String, DateTime

from config.db import engine, metadata


users = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("password", String(255), nullable=False),
)

metadata.create_all(engine)
