import os
import sqlite3 as s3

DATA_BASE = "/home/wlsbase/git_repo_social_post/data/tables/sp_database.db"

def log_hello():
    print("Hello")


def initiate_image():
    try:
        # Use 'with' to ensure the connection is closed automatically
        with s3.connect("test.db") as con: 
            cursor = con.cursor()

            # ... rest of the code ...
            
            # 1. creates table if it does not exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sequences (
                id INTEGER PRIMARY KEY,
                prompt TEXT,
                indep_pairs TEXT,
                dep_pairs TEXT
            )
            """)

            # 2. create new slot for image and gets id
            # NOTE: Use 'cursor' here, not 'cur' (see Problem 2)
            cursor.execute("INSERT INTO sequences DEFAULT VALUES;") 

            image_id = cursor.lastrowid

            # 3. Commit is automatically done by 'with' if no error occurs
            # However, explicitly calling con.commit() here is fine too, 
            # or rely on the default behavior of 'with s3.connect(...) as con:'.
            # For clarity, let's keep the explicit commit you had:
            con.commit() 

            print(image_id)
            return image_id
            
    except s3.Error as e:
        print(f"An SQLite error occurred: {e}")
        return None # Return None if database operation failed
