from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from datetime import date

from app.store import schemas
from app.server.trade import Trade
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_trades(db: Session, trader_id: str, delivery_date: date | None = None):
    res = db.query(schemas.Trade)
    
    if trader_id is not None:
        print("trader_id {}".format(trader_id))
        res = res.filter(schemas.Trade.trader_id == trader_id)
    
    if delivery_date is not None:
        res = res.filter(schemas.Trade.delivery_day == delivery_date)
    
    return res.all()

def create_trade(db: Session, trade: Trade):
    db_trade = schemas.Trade(**trade.dict())
    # commit
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    return db_trade