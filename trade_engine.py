from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_exchange"]
orders_collection = db["orders"]
trades_collection = db["trades"]

def place_order(order):
    """Insert order into MongoDB"""
    orders_collection.insert_one(order)
    print(f"✅ Order placed: {order}")

def match_orders():
    """Match buy/sell orders and execute trades"""
    buy_orders = list(orders_collection.find({"type": "buy"}).sort("price", -1))  # Highest buy first
    sell_orders = list(orders_collection.find({"type": "sell"}).sort("price", 1))  # Lowest sell first

    for buy_order in buy_orders:
        for sell_order in sell_orders:
            if buy_order["price"] >= sell_order["price"]:  # Match found!
                execute_trade(buy_order, sell_order)
                return  # Exit after executing one trade to avoid double-matching

def execute_trade(buy_order, sell_order):
    """Execute trade and update MongoDB"""
    trade_quantity = min(buy_order["quantity"], sell_order["quantity"])
    trade_price = sell_order["price"]  # Use seller's price

    trade = {
        "buy_order_id": buy_order["order_id"],
        "sell_order_id": sell_order["order_id"],
        "symbol": buy_order["symbol"],
        "price": trade_price,
        "quantity": trade_quantity
    }
    
    trades_collection.insert_one(trade)  # Save trade in MongoDB
    print(f"🔥 Trade executed: {trade}")

    # Update order quantities or remove if fully filled
    if buy_order["quantity"] > trade_quantity:
        orders_collection.update_one({"order_id": buy_order["order_id"]}, {"$inc": {"quantity": -trade_quantity}})
    else:
        orders_collection.delete_one({"order_id": buy_order["order_id"]})

    if sell_order["quantity"] > trade_quantity:
        orders_collection.update_one({"order_id": sell_order["order_id"]}, {"$inc": {"quantity": -trade_quantity}})
    else:
        orders_collection.delete_one({"order_id": sell_order["order_id"]})

# Testing the system
if __name__ == "__main__":
    orders_collection.delete_many({})  # Clear orders before running
    trades_collection.delete_many({})  # Clear trade history

    place_order({"order_id": 1, "type": "buy", "symbol": "AAPL", "price": 150, "quantity": 10})
    place_order({"order_id": 2, "type": "sell", "symbol": "AAPL", "price": 145, "quantity": 5})

    match_orders()  # Should trigger a trade
