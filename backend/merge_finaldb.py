import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DB = os.path.join(BASE_DIR, 'pib_data.db')
TRANS_DB = os.path.join(BASE_DIR, 'pib_translations.db')
LANG_CODES = [
    "hi", "ur", "pa", "gu", "mr", "te", "kn", 
    "ml", "ta", "or", "bn", "as", "mni"
]

def merge_to_single_table():
    print("🚀 Starting Merge Process...")
    
    if not os.path.exists(MAIN_DB) or not os.path.exists(TRANS_DB):
        print("❌ Error: Database files not found.")
        return

    conn = sqlite3.connect(MAIN_DB)
    cursor = conn.cursor()

    try:
        print("   Attaching Translation DB...")
        cursor.execute(f"ATTACH DATABASE '{TRANS_DB}' AS trans_db")
        print("   Reading schema of 'press_releases'...")
        cursor.execute("PRAGMA table_info(press_releases)")
        main_columns_info = cursor.fetchall()
        main_cols = [col[1] for col in main_columns_info]
        trans_cols = []
        for code in LANG_CODES:
            trans_cols.append(f"title_{code}")
            trans_cols.append(f"text_{code}")
            
        print(f"   Preparing to add {len(trans_cols)} new columns...")
        all_cols_def = []
        for col in main_columns_info:
            name = col[1]
            dtype = col[2]
            pk = "PRIMARY KEY" if col[5] == 1 else ""
            all_cols_def.append(f"{name} {dtype} {pk}")
        for t_col in trans_cols:
            all_cols_def.append(f"{t_col} TEXT")
            
        create_query = f"CREATE TABLE press_releases_merged ({', '.join(all_cols_def)})"
        cursor.execute("DROP TABLE IF EXISTS press_releases_merged")
        cursor.execute(create_query)
        select_main = ", ".join([f"main.{c}" for c in main_cols])
        select_trans = ", ".join([f"t.{c}" for c in trans_cols])
        
        insert_cols = ", ".join(main_cols + trans_cols)
        
        print("   Copying and merging data (this may take a moment)...")
        copy_query = f"""
            INSERT INTO press_releases_merged ({insert_cols})
            SELECT {select_main}, {select_trans}
            FROM press_releases main
            LEFT JOIN trans_db.translations t ON main.id = t.id
        """
        cursor.execute(copy_query)
        print("   Swapping tables...")
        cursor.execute("DROP TABLE press_releases")
        cursor.execute("ALTER TABLE press_releases_merged RENAME TO press_releases")
        
        conn.commit()
        print("✅ Success! 'press_releases' is now a single table with ALL translations.")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    merge_to_single_table()