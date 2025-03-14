from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_exchange"]
orders_collection = db["orders"]
trades_collection = db["trades"]

def match_orders():
    buy_orders = list(orders_collection.find({"type": "buy"}).sort("order_id", 1))  # FIFO buy orders
    sell_orders = list(orders_collection.find({"type": "sell"}).sort("order_id", 1))  # FIFO sell orders

    for buy in buy_orders:
        for sell in sell_orders:
            if buy["symbol"] == sell["symbol"] and buy["price"] >= sell["price"]:
                trade_qty = min(buy["quantity"], sell["quantity"])  # Partial fill support

                trade = {
                    "buy_order_id": buy["order_id"],
                    "sell_order_id": sell["order_id"],
                    "symbol": buy["symbol"],
                    "price": sell["price"],  # Trade price is the sell price
                    "quantity": trade_qty,
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                }
                trades_collection.insert_one(trade)
                print(f"🔥 Trade executed: {trade}")

                # Update order quantities or remove fully filled orders
                if buy["quantity"] > trade_qty:
                    orders_collection.update_one({"order_id": buy["order_id"]}, {"$inc": {"quantity": -trade_qty}})
                else:
                    orders_collection.delete_one({"order_id": buy["order_id"]})

                if sell["quantity"] > trade_qty:
                    orders_collection.update_one({"order_id": sell["order_id"]}, {"$inc": {"quantity": -trade_qty}})
                else:
                    orders_collection.delete_one({"order_id": sell["order_id"]})

                return  # Exit after processing one trade to maintain FIFO

# Run matching engine
match_orders()
