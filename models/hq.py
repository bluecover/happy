# coding: utf-8

from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, UniqueConstraint
from . import Base


class HQ(Base):
    __tablename__ = 'hq'

    code = Column(String(10), primary_key=True)
    datetime_from = Column(DateTime, primary_key=True)
    datetime_to = Column(DateTime, primary_key=True)
    period = Column(String(16), nullable=False)
    name = Column(String(16))

    pre_close = Column(Numeric(precision=10, scale=2), nullable=False)
    open = Column(Numeric(precision=10, scale=2), nullable=False)
    close = Column(Numeric(precision=10, scale=2), nullable=False)
    low = Column(Numeric(precision=10, scale=2), nullable=False)
    high = Column(Numeric(precision=10, scale=2), nullable=False)

    change = Column(Numeric(precision=10, scale=2))
    change_percent = Column(Numeric(precision=5, scale=2))

    volume = Column(BigInteger, nullable=False)
    money = Column(BigInteger, nullable=False)

    turnover = Column(Numeric(precision=5, scale=2))
