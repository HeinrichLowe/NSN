from models.users import Users
from models.friends import Friends

def create_tables(conn):
    """
    function to create the database tables
    """
    with conn.connect() as cur:
        Users.metadata.create_all(cur)
        Friends.metadata.create_all(cur)