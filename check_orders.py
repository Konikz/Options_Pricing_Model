from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stock_exchange"]
orders_collection = db["orders"]
trades_collection = db["trades"]

def show_orders():
    print("📌 Open Orders:")
    for order in orders_collection.find({}, {"_id": 0}):
        print(order)

def show_trades():
    print("\n🔥 Trade History:")
    for trade in trades_collection.find({}, {"_id": 0}):
        print(trade)

if __name__ == "__main__":
    show_orders()
    show_trades()

