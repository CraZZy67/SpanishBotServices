from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

import os

from settings import Settings
from db.metadata import Base, User, Payment
from settings import Locale


USER, PASSWORD = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')
NAME, PORT = os.getenv('SERVICE_DB_NAME'), os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')

engine = create_engine(f'{Settings.DB_SYSTEM}+{Settings.DB_DRIVER}://{USER}:{PASSWORD}@{NAME}:{PORT}/{DB}')

def get_user(user: int):
    with Session(engine) as session:
        return session.execute(select(User).where(User.user_id == user)).one_or_none()
    
def get_users():
    with Session(engine) as session:
        return session.execute(select(User)).all()

def update_status(user: int, status: str):
    with Session(engine) as session:
        session.execute(update(User).where(User.user_id == user).values(status=status))
        session.commit()