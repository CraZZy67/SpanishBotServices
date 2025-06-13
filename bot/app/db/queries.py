from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session

import os
import datetime

from settings import Settings
from db.metadata import Base, User, Payment
from settings import Locale


USER, PASSWORD = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')
NAME, PORT = os.getenv('SERVICE_DB_NAME'), os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')

engine = create_engine(f'{Settings.DB_SYSTEM}+{Settings.DB_DRIVER}://{USER}:{PASSWORD}@{NAME}:{PORT}/{DB}')
Base.metadata.create_all(engine)

def add_user_info(user_id: int, first_name: str, locale: str, level: int, elc: str, last_name: str | None = None):
    with Session(engine) as session:
        user = User(
            user_id=user_id, first_name=first_name,
            last_name=last_name, locale=locale,
            level=level, elc=elc
        )

        session.add(user)
        session.commit()

        payment = Payment(user_id=user_id, status='Trial', expiry=datetime.datetime.now() + Settings.TRIAL_PERIOD)
        session.add(payment)

        session.commit()

def check_user(user: int):
    with Session(engine) as session:
        return session.execute(select(User).where(User.user_id == user)).one_or_none()

def get_user_locale(user: int):
    with Session(engine) as session:
        locale = session.execute(select(User.locale).where(User.user_id == user)).scalar_one()
    
    return Locale.get_locale_text(locale)

def get_user_payment_status(user: int):
    with Session(engine) as session:
        status = session.execute(select(Payment.status).join(User.user_id).where(User.user_id == user)).scalar_one()
    
    return status