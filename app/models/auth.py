from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import Base
from app.db.database import get_db


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)


