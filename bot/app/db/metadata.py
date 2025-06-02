from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from typing import Optional


class Base(DeclarativeBase): pass

class User(MappedAsDataclass, Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), unique=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[Optional[str]]
    locale: Mapped[str] = mapped_column(String(2))
    level: Mapped[int] = mapped_column(Integer())
    elc: Mapped[str] = mapped_column(String(2))
    