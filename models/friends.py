from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey


class Friends(Base):
    __tablename__ = "friends"

    id: int =Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    friend_id: int = Column(Integer, ForeignKey("users.id"))