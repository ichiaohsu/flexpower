from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"

    id = Column(String, primary_key=True, index=True)
    price = Column(Integer)
    quantity = Column(Integer)
    direction = Column(String)
    delivery_day = Column(Date, index=True)
    delivery_hour = Column(Integer)
    trader_id = Column(String, nullable=False, index=True)
    execution_time = Column(DateTime)

    