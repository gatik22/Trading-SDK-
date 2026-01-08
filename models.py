from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum
from datetime import datetime

# ==================== Enums ====================

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderStatus(str, Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"

class Exchange(str, Enum):
    NSE = "NSE"
    BSE = "BSE"

# ==================== Models ====================

class Instrument(BaseModel):
    symbol: str
    exchange: Exchange
    instrumentType: InstrumentType
    lastTradedPrice: float = Field(gt=0)

class OrderRequest(BaseModel):
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int = Field(gt=0)
    price: Optional[float] = Field(default=None, gt=0)

    @validator("price")
    def validate_price(cls, v, values):
        if values.get("orderStyle") == OrderStyle.LIMIT and v is None:
            raise ValueError("Price is mandatory for LIMIT orders")
        if values.get("orderStyle") == OrderStyle.MARKET and v is not None:
            raise ValueError("Price should not be provided for MARKET orders")
        return v

class OrderResponse(BaseModel):
    orderId: str
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int
    price: Optional[float]
    status: OrderStatus
    createdAt: datetime
    executedAt: Optional[datetime] = None

class Trade(BaseModel):
    tradeId: str
    orderId: str
    symbol: str
    orderType: OrderType
    quantity: int
    executedPrice: float
    executedAt: datetime

class PortfolioHolding(BaseModel):
    symbol: str
    quantity: int
    averagePrice: float
    currentValue: float
