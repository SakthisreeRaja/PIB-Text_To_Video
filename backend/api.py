import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BACKEND_DIR, 'pib_data.db')


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def read_root():
    """A simple root endpoint to check if the API is running."""
    return {"message": "PIB Text-to-Video API is running!"}

@app.get("/api/releases")
def get_all_releases():
    """
    This is the main API endpoint. It fetches all press releases
    from the database and returns them as a JSON list.
    """
    print("API: /api/releases endpoint was called.")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM press_releases ORDER BY id DESC")
        releases = cursor.fetchall()
        
        conn.close()
        
        
        return [dict(row) for row in releases]
        
    except Exception as e:
        print(f"Error fetching releases: {e}")
        return {"error": str(e)}

