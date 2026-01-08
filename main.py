from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid

from models import OrderRequest, OrderResponse, OrderType, OrderStatus
from storage import TradingStorage

app = FastAPI(
    title="Trading SDK API",
    description="Wrapper SDK for Trading APIs - Bajaj Broking Assignment",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = TradingStorage()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )

@app.get("/api/v1/instruments")
def get_instruments():
    return list(storage.instruments.values())

@app.post("/api/v1/orders", response_model=OrderResponse, status_code=201)
def place_order(req: OrderRequest):
    instrument = storage.get_instrument(req.symbol)
    if not instrument:
        raise HTTPException(status_code=404, detail="Invalid symbol")

    if req.orderType == OrderType.SELL:
        holding = storage.portfolio.get(req.symbol)
        if not holding or holding.quantity < req.quantity:
            raise HTTPException(status_code=400, detail="Insufficient holdings")

    order = OrderResponse(
        orderId=str(uuid.uuid4()),
        symbol=req.symbol,
        orderType=req.orderType,
        orderStyle=req.orderStyle,
        quantity=req.quantity,
        price=req.price,
        status=OrderStatus.PLACED,
        createdAt=datetime.utcnow()
    )

    storage.orders[order.orderId] = order
    storage.execute_order(order)
    return order

@app.get("/api/v1/orders/{order_id}")
def get_order(order_id: str):
    order = storage.orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/api/v1/trades")
def get_trades():
    return storage.trades

@app.get("/api/v1/portfolio")
def get_portfolio():
    result = []
    for h in storage.portfolio.values():
        instrument = storage.get_instrument(h.symbol)
        if instrument:
            h.currentValue = h.quantity * instrument.lastTradedPrice
        result.append(h)
    return result
