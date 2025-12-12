import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://pib.gov.in/allrel.aspx"
BACKEND_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BACKEND_DIR, 'pib_data.db')
IMAGES_DIR = os.path.join(BACKEND_DIR, 'images')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def setup_database():
    """Creates our database and the 'press_releases' table."""
    print("Setting up database...")
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS press_releases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ministry_name TEXT,
        title TEXT,
        release_date TEXT,
        release_year INTEGER,
        full_text TEXT,
        pib_url TEXT UNIQUE,
        image_path TEXT,
        language TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print("Database ready.")

def fetch_release_links_with_selenium(year, month):
    """
    Uses Selenium to correctly load the page and get the list of links.
    """
    print(f"  Fetching links for {month}/{year} using Selenium...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")
    options.add_argument(f"accept-language={HEADERS['Accept-Language']}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("  Browser opened. Navigating to URL...")
        driver.get(BASE_URL)
        
        day_dropdown_id = 'ContentPlaceHolder1_ddlday'
        
        wait = WebDriverWait(driver, 10)
        print("  Waiting for page elements to load...")
        wait.until(EC.element_to_be_clickable((By.ID, day_dropdown_id)))
        
        print("  Page loaded. Selecting filters...")
        Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddlMinistry')).select_by_value('0')
        Select(driver.find_element(By.ID, day_dropdown_id)).select_by_value('0')
        Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddlMonth')).select_by_value(str(month))
        
        print("  Setting final filter... (This triggers page reload)")
        Select(driver.find_element(By.ID, 'ContentPlaceHolder1_ddlYear')).select_by_value(str(year))
        
        print("  Waiting for page to reload...")
        time.sleep(3) 
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        ministry_sections = soup.find_all('h3')
        links_list = []
        for ministry in ministry_sections:
            ministry_name = ministry.text.strip()
            ul = ministry.find_next_sibling('ul')
            if ul:
                links = ul.find_all('a', href=True)
                for link in links:
                    if "PressReleasePage.aspx" in link['href']:
                        url = f"https://pib.gov.in/{link['href'].lstrip('/')}"
                        links_list.append({'url': url, 'ministry': ministry_name})
                        
        print(f"  Found {len(links_list)} links.")
        return links_list

    except Exception as e:
        print(f"  Error during Selenium fetch for {month}/{year}: {e}")
        return [] 
    finally:
        if driver:
            print("  Closing browser.")
            driver.quit()


def scrape_release_details(session, url, ministry):
    """
    Visits a single press release URL and scrapes its details.
    """
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find('div', class_='innner-page-main-about-us-content-right-part')
        if not content_div:
            content_div = soup.find('div', id='divRelease') 
        if not content_div:
            print(f"    - Could not find content div. Skipping {url}")
            return None

        title_tag = content_div.find('h2', id='Titleh2')
        if not title_tag: title_tag = content_div.find('h2') 
        title = title_tag.text.strip() if title_tag else "No Title Found"
        
        date_tag = content_div.find('div', id='PrDateTime')
        if not date_tag: date_tag = content_div.find('div', class_='ReleaseDateSubHeaddateTime') 
        date_text = date_tag.text.strip().replace("Posted On:", "").strip() if date_tag else "No Date Found"
        
        release_year = None
        for part in date_text.split():
            if part.isdigit() and len(part) == 4:
                release_year = int(part)
                break
        
        paragraphs = content_div.find_all('p')
        full_text = "\n".join([p.text.strip() for p in paragraphs])
        
        lang_links = soup.find('div', class_='ReleaseLang')
        available_languages = "English"
        if lang_links:
            links = lang_links.find_all('a')
            langs = [link.text.strip() for link in links]
            if langs:
                available_languages = "English, " + ", ".join(langs)

        image_tags = [] 
        image_local_paths = [] 
        
        all_images = content_div.find_all('img')
        correct_image_path = "/WriteReadData/userfiles/image/"

        for img in all_images:
            if 'src' in img.attrs and correct_image_path in img['src']:
                image_tags.append(img) 

        if image_tags:
            for image_tag in image_tags:
                try:
                    img_src = image_tag['src']
                    
                    if not img_src.startswith('http'):
                        img_url = f"https://pib.gov.in{img_src}"
                    else:
                        img_url = img_src
                    
                    filename = os.path.basename(img_url.split('?')[0])
                    
                    if not filename:
                        continue

                    image_local_path_for_db = os.path.join('images', filename)
                    image_full_save_path = os.path.join(IMAGES_DIR, filename)
                    
                    if not os.path.exists(image_full_save_path):
                        print(f"    - Downloading image: {filename}")
                        img_response = session.get(img_url, headers=HEADERS, stream=True)
                        img_response.raise_for_status()
                        with open(image_full_save_path, 'wb') as out_file:
                            shutil.copyfileobj(img_response.raw, out_file)
                    
                    image_local_paths.append(image_local_path_for_db)
                    
                except Exception as img_e:
                    print(f"    - Error downloading one image: {img_e}")
        
        final_image_path_string = ",".join(image_local_paths)
        if not final_image_path_string:
            final_image_path_string = None 

        return {
            'ministry_name': ministry, 'title': title, 'release_date': date_text,
            'release_year': release_year, 'full_text': full_text, 'pib_url': url,
            'image_path': final_image_path_string, 
            'language': available_languages
        }
    except Exception as e:
        print(f"    - Error scraping detail page {url}: {e}")
        return None

def main_scraper():
    if os.path.exists(DB_FILE):
        print("Old database found. Deleting to start fresh.")
        os.remove(DB_FILE)
    
    if os.path.exists(IMAGES_DIR):
        print("Deleting old image folder...")
        shutil.rmtree(IMAGES_DIR)
        
    setup_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    with requests.Session() as session:
        
        YEAR = 2025
        for month in range(10, 11): 
            print(f"--- Fetching data for {month}/{YEAR} ---")
            
            links_list = fetch_release_links_with_selenium(YEAR, month)
            
            if not links_list:
                print(f"  No links found for {month}/{YEAR}. Skipping.")
                continue

            print(f"  --- Found {len(links_list)} links. Scraping details... ---")

            for item in links_list:
                url = item['url']
                ministry = item['ministry']
                print(f"    Scraping: {url}")
                
                details = scrape_release_details(session, url, ministry)
                
                if details:
                    try:
                        cursor.execute('''
                        INSERT INTO press_releases (ministry_name, title, release_date, release_year, full_text, pib_url, image_path, language)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (details['ministry_name'], details['title'], details['release_date'], details['release_year'], details['full_text'], details['pib_url'], details['image_path'], details['language']))
                        conn.commit()
                    except sqlite3.IntegrityError:
                        print(f"    - Item already in database. Skipping.")
                    except Exception as e:
                        print(f"    - Error saving to DB: {e}")
                
                time.sleep(0.5) 
                
            time.sleep(1) 

    conn.close()
    print("\n--- Scraping Complete ---")
    print(f"Data saved to {DB_FILE}")

if __name__ == "__main__":
    main_scraper()