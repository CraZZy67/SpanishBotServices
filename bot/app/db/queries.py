from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from aiogram.types import SuccessfulPayment

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

def get_user_elc(user: int):
    with Session(engine) as session:
        elc = session.execute(select(User.elc).where(User.user_id == user)).scalar_one()
    
    return elc

def get_user_payment_status(user: int):
    with Session(engine) as session:
        status = session.execute(select(Payment.status).where(Payment.user_id == user)).scalar_one()
    
    return status

def get_user_expiry(user: int):
    with Session(engine) as session:
        expiry = session.execute(select(Payment.expiry).where(Payment.user_id == user)).scalar_one()
    
    return expiry

def update_value_user(value, user: int, field: str):
    with Session(engine) as session:
        session.execute(update(User).where(User.user_id == user).values(**{field: value}))
        session.commit()

def check_status(user: int):
    with Session(engine) as session:
        return True if session.execute(select(Payment.status).where(Payment.user_id == user)).scalar_one() == 'Paid' else False

def update_subscribe(payment: SuccessfulPayment, user: int):
    expiry = datetime.datetime.now() + datetime.timedelta(days=float(payment.invoice_payload))
    
    with Session(engine) as session:
        if payment.ttotal_amount == 20000:
            session.execute(update(Payment).where(Payment.user_id == user).values(payment_id=payment.provider_payment_charge_id,
                                                                                  expiry=expiry, status='Basic'))
        elif payment.ttotal_amount == 30000:
            session.execute(update(Payment).where(Payment.user_id == user).values(payment_id=payment.provider_payment_charge_id,
                                                                                  expiry=expiry, status='Premium'))
        else:
            session.execute(update(Payment).where(Payment.user_id == user).values(payment_id=payment.provider_payment_charge_id,
                                                                                  expiry=expiry, status='Max'))
        
        session.commit()