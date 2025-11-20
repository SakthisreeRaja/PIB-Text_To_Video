import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from urllib.parse import quote_plus
import certifi

load_dotenv()

app = FastAPI()

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
        releases = list(collection.find({}, {"_id": 0}))
        releases.sort(key=lambda x: x.get('sqlite_id', 0), reverse=True)
        return releases
    except Exception as e:
        return {"error": str(e)}