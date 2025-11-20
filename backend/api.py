import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BACKEND_DIR, 'pib_data.db')
TRANS_DB_FILE = os.path.join(BACKEND_DIR, 'pib_translations.db')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    
    if os.path.exists(TRANS_DB_FILE):
        try:
            conn.execute(f"ATTACH DATABASE '{TRANS_DB_FILE}' AS trans_db")
        except Exception as e:
            print(f"Warning: Could not attach translation DB: {e}")
            
    return conn

@app.get("/")
def read_root():
    return {"message": "PIB Text-to-Video API is running!"}

@app.get("/api/releases")
def get_all_releases():
    print("API: /api/releases endpoint was called.")
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
       
        query = """
            SELECT main.*, t.* FROM press_releases main 
            LEFT JOIN trans_db.translations t ON main.id = t.id 
            ORDER BY main.id DESC
        """
        
        cursor.execute(query)
        releases = cursor.fetchall()
        
        
        results = [dict(row) for row in releases]
        
        return results
        
    except Exception as e:
        print(f"Error fetching releases: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()