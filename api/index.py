import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware  # <--- Added Compression
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from urllib.parse import quote_plus
import certifi

load_dotenv()

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

raw_password = os.getenv("MONGO_PASSWORD")
raw_username = "SakthiSreeRaja"
cluster_address = "pibcluster.dipmhuj.mongodb.net"

escaped_username = quote_plus(raw_username)
escaped_password = quote_plus(raw_password) if raw_password else ""

MONGO_URI = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_address}/?appName=PIBcluster"
DB_NAME = "pib_database"
COLLECTION_NAME = "releases"

client = MongoClient(
    MONGO_URI, 
    server_api=ServerApi('1'),
    serverSelectionTimeoutMS=5000,
    tlsCAFile=certifi.where()
)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/")
def read_root():
    return {"message": "PIB Text-to-Video API is running on MongoDB Atlas!"}
@app.get("/api/releases")
def get_all_releases():
    try:
        client.admin.command('ping')
        projection = {
            "_id": 0,
            "full_text": 0,
            "text_hi": 0, "text_ur": 0, "text_pa": 0, "text_gu": 0,
            "text_mr": 0, "text_te": 0, "text_kn": 0, "text_ml": 0,
            "text_ta": 0, "text_or": 0, "text_bn": 0, "text_as": 0,
            "text_mni": 0
        }
        
        releases = list(collection.find({}, projection))
        releases.sort(key=lambda x: x.get('sqlite_id', 0), reverse=True)
        return releases
    except Exception as e:
        return {"error": str(e)}
@app.get("/api/releases/{item_id}")
def get_release_detail(item_id: int):
    try:
        item = collection.find_one({"id": item_id}, {"_id": 0})
        if item:
            return item
        return {"error": "Item not found"}
    except Exception as e:
        return {"error": str(e)}