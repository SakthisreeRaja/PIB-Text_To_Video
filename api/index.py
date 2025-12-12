import os
import shutil
import requests
import subprocess
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import certifi
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)

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

client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SCRIPT_FILE = os.path.join(BASE_DIR, "script.txt")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "output_reel_final.mkv")
LANG_INFO_FILE = os.path.join(BASE_DIR, "language_info.txt")
AUDIO_SCRIPT_FILE = os.path.join(BASE_DIR, "script_audio.txt")

@app.get("/")
def read_root():
    return {"message": "PIB Text-to-Video API Active"}

@app.get("/api/releases")
def get_all_releases():
    try:
        projection = {
            "_id": 0, "full_text": 0,
            "text_hi": 0, "text_ur": 0, "text_pa": 0, "text_gu": 0, 
            "text_mr": 0, "text_te": 0, "text_kn": 0, "text_ml": 0,
            "text_ta": 0, "text_or": 0, "text_bn": 0, "text_as": 0, 
            "text_mni": 0,
            "release_date_dt": 0  
        }
        releases = list(collection.find({}, projection).sort("release_date_dt", -1))
        return releases
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/releases/{item_id}")
def get_release_detail(item_id: int):
    item = collection.find_one({"id": item_id}, {"_id": 0})
    if item:
        return item
    return {"error": "Item not found"}

@app.get("/api/watch/{item_id}")
def watch_video(item_id: int, lang: str = "en"):
    item = collection.find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Article not found")

  
    video_links = item.get("video_links", {})
    
    if lang in video_links and video_links[lang]:
        video_url = video_links[lang]
        
        
        try:
            verify_response = requests.head(video_url, timeout=5)
            if verify_response.status_code == 200:
                print(f"✅ CACHE HIT: Video for {item_id} [{lang}] verified.")
                return {"video_url": video_url, "status": "cached"}
            else:
                print(f"⚠️ CACHE INVALID: Video deleted from Cloudinary. Regenerating...")
        except:
            print(f"⚠️ CACHE INVALID: URL not accessible. Regenerating...")

    print(f"⚠️ CACHE MISS: Generating video for {item_id} [{lang}]...")
    
    text_key = f"text_{lang}" if lang != "en" else "full_text"
    content_text = item.get(text_key, "")
    if not content_text and lang != "en":
         content_text = item.get("full_text", "")

    if not content_text:
         raise HTTPException(status_code=400, detail="No text content found")

   
    if os.path.exists(LANG_INFO_FILE): os.remove(LANG_INFO_FILE)
    if os.path.exists(AUDIO_SCRIPT_FILE): os.remove(AUDIO_SCRIPT_FILE)

    with open(SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(content_text)
    
    with open(LANG_INFO_FILE, "w", encoding="utf-8") as f:
        f.write(lang)
    
    
    if lang == "mni":
        english_text = item.get("full_text", "")
        if english_text:
            with open(AUDIO_SCRIPT_FILE, "w", encoding="utf-8") as f:
                f.write(english_text)

    if os.path.exists(ASSETS_DIR):
        shutil.rmtree(ASSETS_DIR)
    os.makedirs(ASSETS_DIR)

    image_urls = item.get("image_path", "").split(",")
    downloaded_count = 0
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for idx, url in enumerate(image_urls):
        url = url.strip()
        if not url: continue
        try:
            res = requests.get(url, headers=headers, stream=True)
            if res.status_code == 200:
                ext = url.split('.')[-1].split('?')[0]
                if len(ext) > 4: ext = "jpg"
                local_path = os.path.join(ASSETS_DIR, f"img_{idx}.{ext}")
                with open(local_path, "wb") as f:
                    shutil.copyfileobj(res.raw, f)
                downloaded_count += 1
        except:
            pass

    if downloaded_count == 0:
         raise HTTPException(status_code=400, detail="No images found for video generation.")

    try:
        
        script_path = os.path.join(BASE_DIR, "main_code.py")
        if not os.path.exists(script_path):
            script_path = os.path.join(BASE_DIR, "scripts", "main_code.py")

       
        process = subprocess.run([sys.executable, script_path], capture_output=True, text=True, cwd=BASE_DIR)
        
        if process.returncode != 0:
            print(process.stderr)
            raise HTTPException(status_code=500, detail="Video generation failed")

        if not os.path.exists(OUTPUT_VIDEO):
             raise HTTPException(status_code=500, detail="Output file missing")

        print("⬆️ Uploading to Cloudinary...")
        upload_res = cloudinary.uploader.upload(OUTPUT_VIDEO, folder="pib_videos", resource_type="video")
        cloud_url = upload_res["secure_url"]

        key_to_update = f"video_links.{lang}"
        collection.update_one({"id": item_id}, {"$set": {key_to_update: cloud_url}})
        
        print(f"✅ GENERATION COMPLETE: Saved to {key_to_update}")
        
        return {"video_url": cloud_url, "status": "generated_fresh"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))