from fastapi import APIRouter, Query, Depends

from sqlalchemy.orm import Session 

from typing import Annotated, List
from datetime import date

from apis.server import trade, error
from apis.store import database
from apis.server.db import get_db

router = APIRouter()

@router.get("/trades", 
    responses={
        200: {
            "model": List[trade.Trade],
            "description": "The trades corresponding to the submitted query"
        },
        400: {"model": error.Error,"description": "Trade couldn't be added due to invalid data."}
    }
)
async def list_trades(
    trader_id: Annotated[str | None, Query(
        description="Unique id of a trader (bot or team member)",
        example="MirkoT"
    )] = None,
    delivery_day: Annotated[date | None, Query(
        description="Day on which the energy has to be delivered in local time."
    )] = None,
    db: Session = Depends(get_db)
) -> List[trade.Trade]: 
    trades = database.get_trades(db, trader_id=trader_id, delivery_day = delivery_day)
    return trades

@router.post("/trades",
    responses={
        200:{
            "content": None,
            "description": "Trade successfully added."
        },
        400: {"model": error.Error, "description": "Trade couldn't be added due to invalid data."}
    }
)
async def create_trade(
    trade: trade.Trade,
    db: Session = Depends(get_db)
) -> None:
    
    database.create_trade(db, trade=trade)