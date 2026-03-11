import os
import yaml

from src import lazynotion

if __name__=="__main__":

    all_dbs = lazynotion.search.search_all(
        {"filter": {"value": "database", "property": "object"}}
    )
    all_dbs = {db["title"][0]["text"]["content"]: db for db in all_dbs}
    all_dbs = dict(sorted(all_dbs.items(), key=lambda x: x[0]))

    table = [
        ("Title",20),
        # ("Id", 40),
        ("Description",None),
        ("Created",12),
        ("Last edited",12),
        ("Properties",40),
        ("Inline",None),
        ("Public url",None),
        ("In trash",None),
        ("Archived",None),
    ]

    widths = [max(len(t[0])+2,t[1]) if t[1] is not None else len(t[0])+2 for t in table]
    line = '+'.join(['-' * w for w in widths]) + "+\n"


    summary = (
        "+" + line +
            "| " + ' | '.join([t[0].ljust(w-2) for t,w in zip(table, widths)]) + " |\n|" +
            line
    )

    def get_summary(db, widths=widths):
        out = {
            "title": db["title"][0]["text"]["content"],
            # "id": db["id"],
            "description": db["description"][0]["text"]["content"] if len(db["description"])>0 else '',
            "created_time": db["created_time"].split('T')[0],
            "last_edited_time": db["last_edited_time"].split('T')[0],
            "properties": [f"Name:{k} - Type:{v['type']}" for k,v in db["properties"].items()],
            "is_inline": db["is_inline"],
            "public_url": db["public_url"],
            "in_trash": db["in_trash"],
            "archived": db["archived"],
        }
        assert len(out)==len(widths)
        res  = ''
        for (k,v), w in zip(out.items(), widths):
            if k=="properties": v = v[0]
            res += "| " + str(v).ljust(w-1)
        res += "|\n"
        for p in out["properties"][1:]:
            for (k,v), w in zip(out.items(), widths):
                if k!="properties": v = ''
                else: v = p
                res += "| " + str(v).ljust(w-1)
            res += "|\n"
        return out, res

    for db in all_dbs.values():
        out, db_text = get_summary(db)
        summary += db_text + "+" + line

    print(summary)

    notion_account_name = lazynotion.utils.get_account_name()
    db_ids = {notion_account_name: {}}
    for db_name in all_dbs:
        db_ids[notion_account_name][db_name] = all_dbs[db_name]["id"]

    saved_ids = lazynotion.utils.get_db_ids()
    saved_ids.update(db_ids)
    with open("db-ids.yml", "w") as f:
        yaml.safe_dump(saved_ids, f)

