import os, sqlite3

db_path = "db.sqlite3"

print(os.path.exists(db_path))

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

search_text = input("name the baby: ")
cursor.execute(f'select * from baby_tracker_app_baby where name = "{search_text}"')
rows = cursor.fetchall()

for item in rows:
    print(item)

conn.close()
