from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# from models.model_api import Model_Api
# from models.student_model import StudentModel
from routes.users import router as user_router

import os

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    uri = os.environ.get('MONGODB_URL')
    
    # for student in collection.find():
    #     print(student)

    # Send a ping to confirm a successful connection
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router, tags=["students"], prefix="/student")

@app.get("/")
async def root():
    return {"message": "Hello World"}
