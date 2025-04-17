from motor.motor_asyncio import AsyncIOMotorClient

# Replace this URI with your actual MongoDB Atlas URI
client = AsyncIOMotorClient("mongodb+srv://atharva6:atharva4@cluster0.qt7s0jd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["identity_db"]
collection = db["extracted_data"]

async def save_to_mongo(data: dict):
    return await collection.insert_one(data)

async def get_all_records():
    return await collection.find().to_list(length=100)

async def delete_all_records():
    await collection.delete_many({})
