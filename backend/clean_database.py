import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import certifi

load_dotenv()
MAX_TEXT_LENGTH = 2200      
MIN_TEXT_LENGTH = 100       
MAX_LINK_COUNT = 5
MAX_NUMBER_RATIO = 0.15
SAFETY_THRESHOLD = 100       

print("🧹 Starting Smart Database Cleanup (With Safety Brake)...")

raw_password = os.getenv("MONGO_PASSWORD")
raw_username = "SakthiSreeRaja"
cluster_address = "pibcluster.dipmhuj.mongodb.net"

escaped_username = quote_plus(raw_username)
escaped_password = quote_plus(raw_password) if raw_password else ""

MONGO_URI = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_address}/?appName=PIBcluster"
DB_NAME = "pib_database"
COLLECTION_NAME = "releases"

try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("✅ Connected to MongoDB.")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    exit()

def has_too_many_numbers(text):
    if not text: return False
    digit_count = sum(c.isdigit() for c in text)
    if len(text) == 0: return False
    return (digit_count / len(text)) > MAX_NUMBER_RATIO

def has_too_many_links(text):
    if not text: return False
    link_count = text.count("http") + text.count("www.")
    return link_count > MAX_LINK_COUNT

def clean_db():
    deleted_count = 0
    truncated_count = 0
    current_total = collection.count_documents({})
    print(f"🔍 Scanning {current_total} documents...")
    cursor = collection.find({}, {"_id": 1, "image_path": 1, "full_text": 1, "id": 1})
    for doc in cursor:
        if current_total <= SAFETY_THRESHOLD:
            print(f"\n🛑 SAFETY BRAKE ACTIVATED: Count reached {current_total}. Stopping deletions.")
            break

        doc_id = doc["_id"]
        should_delete = False
        delete_reason = ""
        img_path = doc.get("image_path", "")
        if not img_path or img_path == "None" or img_path == "":
            should_delete = True
            delete_reason = "No Images"

        full_text = doc.get("full_text", "")
        if not should_delete:
            if len(full_text) < MIN_TEXT_LENGTH:
                should_delete = True
                delete_reason = "Text Too Short (<100 chars)"
            elif has_too_many_numbers(full_text):
                should_delete = True
                delete_reason = "Too Many Numbers/Tables"
            elif has_too_many_links(full_text):
                should_delete = True
                delete_reason = "Too Many Links"
        if should_delete:
            collection.delete_one({"_id": doc_id})
            deleted_count += 1
            current_total -= 1  
            if deleted_count % 10 == 0:
                print(f"   🗑️ Deleted 10... (Current Total: {current_total})")
            continue
        full_doc = collection.find_one({"_id": doc_id})
        updates = {}
        needs_update = False

        for key, value in full_doc.items():
            if (key == "full_text" or key.startswith("text_")) and isinstance(value, str):
                if len(value) > MAX_TEXT_LENGTH:
                    truncated = value[:MAX_TEXT_LENGTH]
                    last_period = truncated.rfind(".")
                    if last_period > 0:
                        truncated = truncated[:last_period+1]
                    
                    updates[key] = truncated
                    needs_update = True
        
        if needs_update:
            collection.update_one({"_id": doc_id}, {"$set": updates})
            truncated_count += 1

    print("\n" + "="*40)
    print(f"🗑️  Deleted: {deleted_count}")
    print(f"✂️  Truncated: {truncated_count}")
    print(f"✅ Final Remaining: {current_total}")
    print("="*40)

if __name__ == "__main__":
    clean_db()