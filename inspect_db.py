
import sqlite3
import os

db_path = "/home/absolut7/Documents/alquranapk/Al.Quran.ver.1.20.1.build.115_decompiled/assets/databases/quran_ar.db"

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)
        
        # Check columns of 'verses' or similar table if it exists
        for table in tables:
            table_name = table[0]
            print(f"\nColumns in {table_name}:")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(col)
                
            # Sample data
            print(f"Sample data from {table_name}:")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            print(cursor.fetchone())

        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")
