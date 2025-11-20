#Try running this code in collab doing local may crash due to network issues
#also collab have run even network stopped as they are running in google servers and they synced again when network is back so prefer collab for this code

#local running code 
import sqlite3
import os
from deep_translator import GoogleTranslator

BASE = os.path.dirname(__file__)
SOURCE_DB = os.path.join(BASE, "pib_data.db")
TARGET_DB = os.path.join(BASE, "pib_translations.db")

LANG_MAP = {
    "hi": "hi",
    "ur": "ur",
    "pa": "pa",
    "gu": "gu",
    "mr": "mr",
    "te": "te",
    "kn": "kn",
    "ml": "ml",
    "ta": "ta",
    "or": "or",
    "bn": "bn",
    "as": "as",
    "mni": "mni-Mtei"
}

MAX_LEN = 4500

def chunk_text(text, max_len=MAX_LEN):
    if len(text) <= max_len:
        return [text]

    chunks = []
    current = ""

    paragraphs = text.split("\n\n")

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_len:
            chunks.append(current.strip())
            current = para + "\n\n"
        else:
            current += para + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks

def safe_translate(text, lang):
    if not text:
        return ""

    chunks = chunk_text(text)

    out = []
    for c in chunks:
        try:
            translated = GoogleTranslator(source="auto", target=lang).translate(c)
            out.append(translated)
        except Exception as e:
            print(f"⚠️ Error translating to {lang}: {e}")
            out.append("")

    return "\n\n".join(out)


def create_translation_db():
    print("Loading Source DB:", SOURCE_DB)

    src = sqlite3.connect(SOURCE_DB)
    c_src = src.cursor()

    dst = sqlite3.connect(TARGET_DB)
    c_dst = dst.cursor()

    columns = ["id INTEGER PRIMARY KEY"]
    for code in LANG_MAP.keys():
        columns.append(f"title_{code} TEXT")
        columns.append(f"text_{code} TEXT")

    c_dst.execute(f"CREATE TABLE IF NOT EXISTS translations ({', '.join(columns)});")
    dst.commit()

    c_src.execute("SELECT id, title, full_text FROM press_releases ORDER BY id ASC")
    rows = c_src.fetchall()

    print(f"🔵 Total rows: {len(rows)}")

    for idx, (rid, title, full_text) in enumerate(rows, start=1):
        print(f"[{idx}] Translating row ID {rid}")

        translated = {}

        for code, lang in LANG_MAP.items():
            translated[f"title_{code}"] = safe_translate(title, lang)
            translated[f"text_{code}"] = safe_translate(full_text, lang)

        col_names = ["id"] + list(translated.keys())
        placeholders = ",".join("?" for _ in col_names)

        c_dst.execute(
            f"INSERT OR REPLACE INTO translations ({','.join(col_names)}) VALUES ({placeholders})",
            [rid] + list(translated.values())
        )

        dst.commit()

    src.close()
    dst.close()

    print("\n✅ DONE! Translations saved in:", TARGET_DB)


if __name__ == "__main__":
    create_translation_db()



#colab code below


# import sqlite3
# import os
# from deep_translator import GoogleTranslator

# ROOT = os.path.dirname(__file__) if "__file__" in globals() else "/content/drive/MyDrive/pib_project"

# SOURCE_DB = os.path.join(ROOT, "pib_data.db")
# TARGET_DB = os.path.join(ROOT, "pib_translations.db")

# LANG_MAP = {
#     "hi": "hi",
#     "ur": "ur",
#     "pa": "pa",
#     "gu": "gu",
#     "mr": "mr",
#     "te": "te",
#     "kn": "kn",
#     "ml": "ml",
#     "ta": "ta",
#     "or": "or",
#     "bn": "bn",
#     "as": "as",
#     "mni": "mni-Mtei"   
# }

# MAX_LEN = 4500 


# def chunk_text(text, max_len=MAX_LEN):
#     if len(text) <= max_len:
#         return [text]

#     chunks = []
#     block = ""

#     paragraphs = text.split("\n\n")

#     for para in paragraphs:
#         if len(block) + len(para) + 2 > max_len:
#             chunks.append(block.strip())
#             block = para + "\n\n"
#         else:
#             block += para + "\n\n"

#     if block.strip():
#         chunks.append(block.strip())

#     return chunks

# def safe_translate(text, lang):
#     if not text:
#         return ""

#     chunks = chunk_text(text)

#     out = []
#     for c in chunks:
#         try:
#             part = GoogleTranslator(source="auto", target=lang).translate(c)
#             out.append(part)
#         except Exception as e:
#             print(f"⚠️  Translation failed for lang {lang}: {e}")
#             out.append("")

#     return "\n\n".join(out)

# def create_translation_db():

#     print("Opening source DB:", SOURCE_DB)

#     src = sqlite3.connect(SOURCE_DB)
#     cur_src = src.cursor()

#     dst = sqlite3.connect(TARGET_DB)
#     cur_dst = dst.cursor()

#     cols = ["id INTEGER PRIMARY KEY"]
#     for code in LANG_MAP.keys():
#         cols.append(f"title_{code} TEXT")
#         cols.append(f"text_{code} TEXT")

#     cur_dst.execute(f"CREATE TABLE IF NOT EXISTS translations ({', '.join(cols)});")
#     dst.commit()

#     cur_src.execute("SELECT id, title, full_text FROM press_releases ORDER BY id ASC")
#     rows = cur_src.fetchall()

#     print(f"🔵 TOTAL ROWS FOUND: {len(rows)}")
#     print("🚀 Starting full translation (no skipping)...")

#     for idx, (rid, title, full_text) in enumerate(rows, start=1):
#         print(f"[{idx}] Translating ID {rid}")

#         translated = {}

#         for code, lang in LANG_MAP.items():
#             translated[f"title_{code}"] = safe_translate(title, lang)

#         for code, lang in LANG_MAP.items():
#             translated[f"text_{code}"] = safe_translate(full_text, lang)

#         c_names = ["id"] + list(translated.keys())
#         qs = ",".join("?" for _ in c_names)

#         cur_dst.execute(
#             f"INSERT OR REPLACE INTO translations ({','.join(c_names)}) VALUES ({qs})",
#             [rid] + list(translated.values())
#         )

#         dst.commit()

#     src.close()
#     dst.close()

#     print("\n✅ Translation completed successfully!")
#     print("📁 Saved at:", TARGET_DB)



# if __name__ == "__main__":
#     create_translation_db()