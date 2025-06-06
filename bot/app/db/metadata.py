from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from typing import Optional


class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[Optional[str]]
    locale: Mapped[str] = mapped_column(String(2))
    level: Mapped[int] = mapped_column(Integer())
    elc: Mapped[str] = mapped_column(String(2))
    