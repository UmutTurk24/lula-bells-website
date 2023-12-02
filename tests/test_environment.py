# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# # from dotenv import dotenv_values
# from pymongo import MongoClient
# # from routes import router as book_router

# app = FastAPI()
# config = dotenv_values(".env")
# app.include_router(book_router, tags=["books"], prefix="/book")


# @app.on_event("startup")
# async def startup_event():
#     app.mongodb_client = MongoClient(config["ATLAS_URI"])
#     app.database = app.mongodb_client[config["DB_NAME"] + "test"]

# @app.on_event("shutdown")
# async def shutdown_event():
#     app.mongodb_client.close()
#     app.database.drop_collection("books")
