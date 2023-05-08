from pydantic import BaseModel, Field
from datetime import date, datetime

from enum import Enum

class DirectionEnum(str, Enum):
    buy = "buy"
    sell = "sell"

class Trade(BaseModel):
    id: str = Field(description="Unique id of the trade as defined by the exchange")
    price: int = Field(description="Price in eurocent/MWh.")
    quantity: int = Field(description="Quantity in MW.")
    direction: DirectionEnum = Field(description="Direction of the trade from the perspective of flew-power, can be either buy or sell.")
    delivery_day: date = Field(description="Day on which the energy has to be delivered in local time.")
    delivery_hour: int = Field(description="Hour during which the energy has to be delivered in local time.")
    trader_id: str = Field(description="Unique id of a trader (bot or team member).")
    execution_time: datetime = Field(description="UTC datetime at which the trade occured on the exchange.")

    class Config:
        orm_mode = True

