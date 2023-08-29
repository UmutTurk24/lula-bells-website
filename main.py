from fastapi import FastAPI

from db.model_api import Model_Api

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.environ.get('MONGODB_URL')

app = FastAPI()

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.inventory
model_api = Model_Api(db)
print(model_api.list_students)
# print(db)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.get("/")
async def root():
    return {"message": "Hello World"}
