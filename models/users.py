from .base import Base
from sqlalchemy import String, Integer, Column, Date, Boolean

class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    username: str = Column(String(64), nullable=False, unique=True)
    password: str = Column(String(32), nullable=False)
    full_name: str = Column(String(128), nullable=False)
    birthday: str = Column(Date)
    active: bool = Column(Boolean, default=True)
