import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Setup workspace directory in sys.path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

async def seed():
    print("Seed Process Started...")
    print(f"Connecting to MongoDB at: {settings.MONGODB_URI}...")
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    
    # 1. Seed Shopping Hubs
    hubs_path = os.path.join("seed", "shopping_hubs.json")
    if not os.path.exists(hubs_path):
        print(f"Error: shopping hubs seed file '{hubs_path}' not found.")
        client.close()
        return
        
    with open(hubs_path, "r", encoding="utf-8") as f:
        hubs = json.load(f)
        
    print(f"Loaded {len(hubs)} shopping hubs.")
    
    hubs_inserted = 0
    hubs_skipped = 0
    
    for hub in hubs:
        existing = await db.shopping_hubs.find_one({"_id": hub["_id"]})
        if existing:
            hubs_skipped += 1
            continue
            
        hub["created_at"] = datetime.utcnow()
        await db.shopping_hubs.insert_one(hub)
        hubs_inserted += 1
        
    # 2. Seed Stores
    stores_path = os.path.join("seed", "stores.json")
    if not os.path.exists(stores_path):
        print(f"Error: stores seed file '{stores_path}' not found.")
        client.close()
        return
        
    with open(stores_path, "r", encoding="utf-8") as f:
        stores = json.load(f)
        
    print(f"Loaded {len(stores)} stores.")
    
    stores_inserted = 0
    stores_skipped = 0
    
    for store in stores:
        existing = await db.stores.find_one({"name": store["name"], "city": store["city"]})
        if existing:
            stores_skipped += 1
            continue
            
        store["created_at"] = datetime.utcnow()
        store["updated_at"] = datetime.utcnow()
        await db.stores.insert_one(store)
        stores_inserted += 1
        
    print("=================== Seeding Summary ===================")
    print(f"Shopping Hubs - Handled: {len(hubs)} | Inserted: {hubs_inserted} | Skipped: {hubs_skipped}")
    print(f"Stores        - Handled: {len(stores)} | Inserted: {stores_inserted} | Skipped: {stores_skipped}")
    print("=======================================================")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
