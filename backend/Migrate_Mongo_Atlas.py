import sqlite3
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import certifi

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB = os.path.join(BASE_DIR, 'pib_data.db')

raw_username = "SakthiSreeRaja"
raw_password = os.getenv("MONGO_PASSWORD")
cluster_address = "pibcluster.dipmhuj.mongodb.net"

escaped_username = quote_plus(raw_username)
escaped_password = quote_plus(raw_password) if raw_password else ""

MONGO_URI = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_address}/?appName=PIBcluster"

DB_NAME = "pib_database"
COLLECTION_NAME = "releases"

def migrate_direct():
    if not os.path.exists(SQLITE_DB):
        print("Database not found")
        return

    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM press_releases")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} records.")

        if len(rows) == 0:
            return

        client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        client.admin.command('ping')
        print("Connected to Atlas.")

        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        data_to_insert = []
        for row in rows:
            doc = dict(row)
            if 'id' in doc:
                doc['sqlite_id'] = doc['id']
            data_to_insert.append(doc)

        if data_to_insert:
            collection.insert_many(data_to_insert)
            print(f"Uploaded {len(data_to_insert)} documents.")

    except Exception as e:
        print(e)

    finally:
        conn.close()

if __name__ == "__main__":
    migrate_direct()