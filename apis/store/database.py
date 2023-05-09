from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from datetime import date

from apis.store import schemas
from apis.server.trade import Trade
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_trades(db: Session, trader_id: str, delivery_day: date | None = None):
    res = db.query(schemas.Trade)
    
    if trader_id is not None:
        res = res.filter(schemas.Trade.trader_id == trader_id)
    
    if delivery_day is not None:
        res = res.filter(schemas.Trade.delivery_day == delivery_day)
    return res.all()

def create_trade(db: Session, trade: Trade):
    db_trade = schemas.Trade(**trade.dict())
    # commit
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    return db_trade