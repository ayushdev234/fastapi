import sqlite3
import pandas as pd
import os

# Absolute path (adjust filename if needed)
db_path = r'D:\FASTAPI\blog\blog.db'

# Check if file exists
if not os.path.exists(db_path):
    raise FileNotFoundError(f"❌ Database file not found at: {db_path}")

conn = sqlite3.connect(db_path)

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

print("📋 Tables in the database:")
print(tables)

for table_name in tables['name']:
    print(f"\n📄 Data from table: {table_name}")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    print(df)

conn.close()
