from sqlalchemy import create_engine

def connect_db():
    return create_engine("postgresql+psycopg2://postgres:password@localhost:5432", echo=True)