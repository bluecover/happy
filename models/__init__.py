# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine(
    'mysql://zh:000000@rdsbi4u1v33wc6zn0w71o.mysql.rds.aliyuncs.com/alchemist?charset=utf8',
    encoding='utf-8'
)
# Base.metadata.bind = engine
# Session = sessionmaker(bind=engine)

from stock_profile import StockProfile
from hq_snapshot import HQSnapshot

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

'''
snapshot = HQSnapshot(
    code='399006',
    name=u'创业板指',
    date='20160517',
    time='15:00',
    price=2022.38,
    pre_close=2031.21,
    open=2000.1,
    low=1998,
    high=2088.03,
    volume=1000000,
    volume_money=123456789
)

session = Session()
session.add(snapshot)
session.commit()

hq_snapshots = session.query(HQSnapshot).filter(HQSnapshot.code=='399006').all()
for hq in hq_snapshots:
    print hq.name, hq.price
'''
