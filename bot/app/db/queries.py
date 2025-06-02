from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

import os

from settings import Settings
from db.metadata import Base, User
from settings import Locale


USER, PASSWORD = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')
HOST, PORT = os.getenv('POSTGRES_HOST'), os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')

engine = create_engine(f'{Settings.DB_SYSTEM}+{Settings.DB_DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')
Base.metadata.create_all(engine)

def add_user_info(user_id: int, first_name: str, last_name: str | None, locale: str, level: int, elc: str):
    with Session(engine) as session:
        if session.execute(select(User).where(User.user_id == user_id)).one_or_none():
            stmt = update(User).where(User.user_id == user_id).values(locale=locale, elc=elc, level=level)
            
            session.execute(stmt)
        else:
            user = User(
                user_id=user_id, first_name=first_name,
                last_name=last_name, locale=locale,
                level=level, elc=elc
            )

            session.add(user)
            
        session.commit()

def get_user_locale(user: int):
    with Session(engine) as session:
        locale = session.execute(select(User.locale).where(User.user_id == user)).scalar_one()
    
    return Locale.get_locale_text(locale)