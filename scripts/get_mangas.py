import yaml
from datetime import datetime

from src import lazynotion

db_id = lazynotion.utils.get_db_ids(lazynotion.utils.get_account_name())["log-mangas"]
manga_db = lazynotion.database.Database(db_id=db_id)

def transform_pages(all_pages):
    cleaned_list = []

    for page in all_pages:
        props = page.get("properties", {})
        
        # 1. Helper for Title/Rich Text (Author, Editor, Name)
        def get_text(prop_name):
            prop = props.get(prop_name, {})
            p_type = prop.get("type")
            if not p_type: return ""
            data = prop.get(p_type, [])
            return data[0].get("plain_text", "") if data else ""

        # 2. Hardened Helper for Select/Status (Owned, Priority, Status)
        def get_option(prop_name):
            prop = props.get(prop_name, {})
            p_type = prop.get("type") # e.g., 'select' or 'status'
            if not p_type: return ""
            
            detail = prop.get(p_type)
            # This is the fix: check if 'select' or 'status' is null/None
            if detail is None: 
                return ""
            return detail.get("name", "")

        # 3. Handle the Cover URL
        cover_obj = page.get("cover")
        cover_url = ""
        if cover_obj:
            c_type = cover_obj.get("type")
            cover_url = cover_obj.get(c_type, {}).get("url", "")

        # Build the dictionary mapping your specific keys
        item = {
            "title": get_text("Name"),
            "author": get_text("Author"),
            "status": get_option("Status"),
            "cover_url": cover_url,
            "total_chapters": props.get("No. chapters", {}).get("number", 0),
            "current_chapter": props.get("Current chapter", {}).get("number", 0),
            "publication_year": props.get("Publication year", {}).get("number"),
            "url": props.get("URL", {}).get("url", ""),
        }
        
        cleaned_list.append(item)
    
    return cleaned_list

pages = manga_db.get_pages()
pages = transform_pages(pages)
with open("mangas.yml", "w") as f:
    yaml.safe_dump(pages, f)
