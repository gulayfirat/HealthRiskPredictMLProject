import sqlite3
import pandas as pd

db_name = "Health_Risk.db"

# Method to create and return a database connection and cursor
def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

# Method to create necessary tables in the database
def create_tables(conn, cursor):
    if conn is None:
        print("ERROR(create_table method): Database connection failed.")
        return False
    try:
        # Create Features table to store user health data
        cursor.execute('''
                CREATE TABLE Features (
                    id INTEGER PRIMARY KEY,
                    age INTEGER,
                    weight INTEGER,
                    height INTEGER,
                    exercise VARCHAR,
                    sleep REAL,
                    sugar_intake VARCHAR,
                    smoking VARCHAR,
                    alcohol VARCHAR,
                    married VARCHAR,
                    profession VARCHAR,
                    bmi REAL)
                ''')
        # Create Predicts table (definition continues below)
        cursor.execute('''
                CREATE TABLE Predicts (
                    id INTEGER PRIMARY KEY,
                    predict VARCHAR)
                    ''')
        conn.commit()
        print(f"SUCCESS( create_table method ):  Created {db_name} 's table(s).")
        return True

    except Exception as e:
        print(f"ERROR( create_table method ): {e}")
        return False


# Insert a new record into Features table
def insert_df_to_db(conn, df_data: pd.DataFrame, table_name: str):
    if conn is None:
        print("ERROR( insert_df_to_db method ): Database connection failed.")
        return False
    try:
        df_data.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )

        print(f"SUCCESS( insert_df_to_db method ): {df_data} insert to '{table_name}' table")
        return True

    except Exception as e:
        print(f"ERROR( insert_df_to_db method ): {e}")
        return False


#Other CRUD operations but not used in the project
# Fetch all records from Features table
def fetch_all_features(cursor):
    try:
        cursor.execute('SELECT * FROM Features')
        return cursor.fetchall()
    except Exception as e:
        print(f"ERROR( fetch_all_features method): {e}")
        return []

# Update a record in Features table by id
def update_feature(conn, cursor, feature_id, update_data):
    try:
        cursor.execute('''
            UPDATE Features
            SET age=?, weight=?, height=?, exercise=?, sleep=?, sugar_intake=?, smoking=?, alcohol=?, married=?, profession=?, bmi=?
            WHERE id=?
        ''', (*update_data, feature_id))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"ERROR( update_feature method): {e}")
        return 0

# Delete a record from Features table by id
def delete_feature(conn, cursor, feature_id):
    try:
        cursor.execute('DELETE FROM Features WHERE id=?', (feature_id,))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"ERROR( delete_feature method ): {e}")
        return 0