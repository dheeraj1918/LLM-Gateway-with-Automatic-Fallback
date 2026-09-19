from pymongo import MongoClient
from backend.config import DATABASE_NAME,MONGO_URI
client=MongoClient(MONGO_URI)
db=client[DATABASE_NAME]

users_collection=db["users"]
providers_collection=db["providers"]
models_collection=db["models"]
gateway_keys_collection=db["gateway_api_keys"]
requests_collection=db["llm_requests"]
attempts_collection=db["llm_attempts"]
gateway_keys_collection = db["gateway_api_keys"]

