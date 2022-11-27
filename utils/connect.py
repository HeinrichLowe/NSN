from sqlalchemy import create_engine

def connect_db():
    return create_engine("sqlite+pysqlite:///database/nsn.db", echo=False)