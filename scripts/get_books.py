import yaml
from datetime import datetime

from src import lazynotion

db_id = lazynotion.utils.get_db_ids(lazynotion.utils.get_account_name())["books"]
book_db = lazynotion.database.Database(db_id=db_id)

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
            "genre": [g["name"] for g in props.get("Genre", {}).get("multi_select", [])],
            "editor": get_text("Editor"),
            "priority": get_option("Priority"),
            "start": props.get("Start", {}).get("date", {}).get("start") if props.get("Start", {}).get("date") else None,
            "end": props.get("End", {}).get("date", {}).get("start") if props.get("End", {}).get("date") else None,
            "cover_url": cover_url,
            "progress": props.get("Progress", {}).get("formula", {}).get("number", 0),
            "total_pages": props.get("Total Pages", {}).get("number", 0),
            "publication_year": props.get("Publication year", {}).get("number"),
            "current_page": props.get("Current Page", {}).get("number", 0),
            "url": props.get("Url", {}).get("url", ""),
            "owned": get_option("Owned")
        }
        
        cleaned_list.append(item)
    
    return cleaned_list

pages = book_db.get_pages()
pages = transform_pages(pages)
with open("books.yml", "w") as f:
    yaml.safe_dump(pages, f)
