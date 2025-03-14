from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stock_exchange"]
orders_collection = db["orders"]
trades_collection = db["trades"]

# Fetch open orders
open_orders = list(orders_collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal ID
print("\n📌 Open Orders:")
for order in open_orders:
    print(order)

# Fetch trade history
trade_history = list(trades_collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal ID
print("\n🔥 Trade History:")
for trade in trade_history:
    print(trade)
