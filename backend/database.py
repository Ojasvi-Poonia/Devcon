from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017" #this is a database connection string to connect to mongo db locally
client = AsyncIOMotorClient(MONGO_URI) #creates async connection to mongodb
db = client["devcon"]# creates database named devcon

user_collection = db["users"] #a collection where users data will be stored
async def add_user(user_data):
    result = await user_collection.insert_one(user_data)
    return str(result.inserted_id)
