import uuid
from typing import Dict, List, Optional
from datetime import datetime

from models import (
    Instrument, OrderResponse, Trade, PortfolioHolding,
    OrderType, OrderStyle, OrderStatus,
    Exchange, InstrumentType
)

class TradingStorage:
    def __init__(self):
        self.instruments: Dict[str, Instrument] = {}
        self.orders: Dict[str, OrderResponse] = {}
        self.trades: List[Trade] = []
        self.portfolio: Dict[str, PortfolioHolding] = {}
        self._init_instruments()

    def _init_instruments(self):
        instruments = [
            Instrument(
                symbol="RELIANCE",
                exchange=Exchange.NSE,
                instrumentType=InstrumentType.EQUITY,
                lastTradedPrice=2450.50
            ),
            Instrument(
                symbol="TCS",
                exchange=Exchange.NSE,
                instrumentType=InstrumentType.EQUITY,
                lastTradedPrice=3580.75
            ),
            Instrument(
                symbol="INFY",
                exchange=Exchange.NSE,
                instrumentType=InstrumentType.EQUITY,
                lastTradedPrice=1450.30
            ),
            Instrument(
                symbol="HDFCBANK",
                exchange=Exchange.NSE,
                instrumentType=InstrumentType.EQUITY,
                lastTradedPrice=1620.80
            ),
            Instrument(
                symbol="TATASTEEL",
                exchange=Exchange.BSE,
                instrumentType=InstrumentType.EQUITY,
                lastTradedPrice=145.60
            ),
            Instrument(
                symbol="NIFTY_FUT",
                exchange=Exchange.NSE,
                instrumentType=InstrumentType.FUTURES,
                lastTradedPrice=21850.00
            ),
        ]

        for inst in instruments:
            self.instruments[inst.symbol] = inst


    def get_instrument(self, symbol: str) -> Optional[Instrument]:
        return self.instruments.get(symbol)

    def execute_order(self, order: OrderResponse):
        instrument = self.get_instrument(order.symbol)
        if not instrument:
            return

        execution_price = (
            instrument.lastTradedPrice
            if order.orderStyle == OrderStyle.MARKET
            else order.price
        )

        order.status = OrderStatus.EXECUTED
        order.executedAt = datetime.utcnow()

        trade = Trade(
            tradeId=str(uuid.uuid4()),
            orderId=order.orderId,
            symbol=order.symbol,
            orderType=order.orderType,
            quantity=order.quantity,
            executedPrice=execution_price,
            executedAt=order.executedAt
        )

        self.trades.append(trade)
        self._update_portfolio(trade)

    def _update_portfolio(self, trade: Trade):
        symbol = trade.symbol

        if trade.orderType == OrderType.BUY:
            if symbol in self.portfolio:
                h = self.portfolio[symbol]
                total_cost = h.averagePrice * h.quantity + trade.executedPrice * trade.quantity
                h.quantity += trade.quantity
                h.averagePrice = total_cost / h.quantity
            else:
                self.portfolio[symbol] = PortfolioHolding(
                    symbol=symbol,
                    quantity=trade.quantity,
                    averagePrice=trade.executedPrice,
                    currentValue=0
                )
        else:
            h = self.portfolio.get(symbol)
            if h:
                h.quantity -= trade.quantity
                if h.quantity <= 0:
                    del self.portfolio[symbol]
