from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from aiogram.types import SuccessfulPayment

import os
import datetime

from db.metadata import Payment
from settings import  Settings

USER, PASSWORD = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD')
NAME, PORT = os.getenv('SERVICE_DB_NAME'), os.getenv('POSTGRES_PORT')
DB = os.getenv('POSTGRES_DB')

engine = create_engine(f'{Settings.DB_SYSTEM}+{Settings.DB_DRIVER}://{USER}:{PASSWORD}@{NAME}:{PORT}/{DB}')

def check_status(user: int):
    with Session(engine) as session:
        return True if session.execute(select(Payment.status).where(Payment.user_id == user)).scalar_one() == 'Paid' else False

def update_subscribe(payment: SuccessfulPayment, user: int):
    expiry = datetime.datetime.now() + datetime.timedelta(days=float(payment.invoice_payload))
    
    with Session(engine) as session:
        session.execute(update(Payment).where(Payment.user_id == user).values(payment_id=payment.provider_payment_charge_id,
                                                                              expiry=expiry, status='Paid'))
        session.commit()