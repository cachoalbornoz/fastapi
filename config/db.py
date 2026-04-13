from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://galbornoz:Cervantes69@localhost:3306/guard_db_desarrollo")

metadata = MetaData()

metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
