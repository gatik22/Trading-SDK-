# Trading SDK - Wrapper API for Trading Platform

A FastAPI-based wrapper SDK for trading APIs, implementing core trading workflows including order management, portfolio tracking, and trade execution.

## Features

- **Instrument Management**: View available financial instruments with real-time prices
- **Order Management**: Place BUY/SELL orders with MARKET/LIMIT styles
- **Trade Tracking**: View executed trades history
- **Portfolio Management**: Track holdings with average price and current value
- **Built-in Validation**: Pydantic models with comprehensive validation
- **Swagger UI**: Interactive API documentation at `/docs`
- **In-Memory Storage**: Lightweight, no database setup required

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

##  Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd trading-sdk
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the application is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Instruments

- **GET** `/api/v1/instruments` - Get all tradable instruments
- **GET** `/api/v1/instruments/{symbol}` - Get specific instrument

### Orders

- **POST** `/api/v1/orders` - Place a new order
- **GET** `/api/v1/orders/{orderId}` - Get order status
- **GET** `/api/v1/orders` - Get all orders

### Trades

- **GET** `/api/v1/trades` - Get all executed trades

### Portfolio

- **GET** `/api/v1/portfolio` - Get current portfolio holdings

## Usage Examples

### 1. Get All Instruments

```bash
curl -X GET "http://localhost:8000/api/v1/instruments"
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 2450.50
  },
  {
    "symbol": "TCS",
    "exchange": "NSE",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 3580.75
  }
]
```

### 2. Place a Market Order (BUY)

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RELIANCE",
    "orderType": "BUY",
    "orderStyle": "MARKET",
    "quantity": 10
  }'
```

**Response:**
```json
{
  "orderId": "550e8400-e29b-41d4-a716-446655440000",
  "symbol": "RELIANCE",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10,
  "price": null,
  "status": "EXECUTED",
  "createdAt": "2024-01-08T10:30:00.000Z",
  "executedAt": "2024-01-08T10:30:00.100Z"
}
```

### 3. Place a Limit Order (BUY)

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "TCS",
    "orderType": "BUY",
    "orderStyle": "LIMIT",
    "quantity": 5,
    "price": 3500.00
  }'
```

### 4. Get Order Status

```bash
curl -X GET "http://localhost:8000/api/v1/orders/550e8400-e29b-41d4-a716-446655440000"
```

### 5. Get All Trades

```bash
curl -X GET "http://localhost:8000/api/v1/trades"
```

**Response:**
```json
[
  {
    "tradeId": "123e4567-e89b-12d3-a456-426614174000",
    "orderId": "550e8400-e29b-41d4-a716-446655440000",
    "symbol": "RELIANCE",
    "orderType": "BUY",
    "quantity": 10,
    "executedPrice": 2450.50,
    "executedAt": "2024-01-08T10:30:00.100Z"
  }
]
```

### 6. Get Portfolio

```bash
curl -X GET "http://localhost:8000/api/v1/portfolio"
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE",
    "quantity": 10,
    "averagePrice": 2450.50,
    "currentValue": 24505.00
  }
]
```

### 7. Place a Sell Order

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RELIANCE",
    "orderType": "SELL",
    "orderStyle": "MARKET",
    "quantity": 5
  }'
```
## Assumptions Made

1. **Authentication**: Single hardcoded user (no authentication required)
2. **Order Execution**: All MARKET orders execute immediately at last traded price
3. **Limit Orders**: Execute immediately at specified limit price (simplified)
4. **Portfolio**: Calculated using FIFO (First In First Out) method
5. **Market Hours**: Trading allowed 24/7 (no market hours restriction)
6. **Instrument Prices**: Static prices (not connected to real market data)
7. **Order Validation**: Basic validations only (quantity > 0, valid symbol, sufficient holdings for SELL)
8. **Concurrency**: In-memory storage without locks (suitable for single-user simulation)

## Project Structure

```
trading-sdk/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore
```

##  Technical Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Validation**: Pydantic 2.5.0
- **Storage**: In-memory (Python dictionaries)

##  Data Models

### Order Types
- `BUY` - Buy order
- `SELL` - Sell order

### Order Styles
- `MARKET` - Execute at current market price
- `LIMIT` - Execute at specified price or better

### Order Status
- `NEW` - Order created
- `PLACED` - Order placed in system
- `EXECUTED` - Order successfully executed
- `CANCELLED` - Order cancelled

### Instrument Types
- `EQUITY` - Stock/Equity shares
- `FUTURES` - Futures contracts
- `OPTIONS` - Options contracts

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET requests
- `201 Created` - Successful order placement
- `400 Bad Request` - Invalid input or validation errors
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

Error responses include:
```json
{
  "detail": "Error message here",
  "timestamp": "2024-01-08T10:30:00.000Z"
}
```

## Validations Implemented
1. **Quantity Validation**: Must be greater than 0
2. **Price Validation**: 
   - Mandatory for LIMIT orders
   - Must not be provided for MARKET orders
   - Must be greater than 0
3. **Symbol Validation**: Must exist in instruments list
4. **Sell Order Validation**: Checks for sufficient holdings
5. **Pydantic Validation**: Automatic type checking and conversion

## Bonus Features Implemented
Centralized exception handling  
Swagger/OpenAPI documentation (built-in with FastAPI)  
Order execution simulation (immediate for market orders)  
Clean code with type hints  
Comprehensive validation  

##  Author
Name-Gatik kaushik 
Email-gatikkaushik@gmail.com
github-gatik22



**Note**: This is a simulation system and should not be used for actual trading. No real market connectivity is implemented.
