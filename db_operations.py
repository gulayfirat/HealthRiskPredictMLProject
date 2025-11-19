import sqlite3
import  os
import pandas as pd

db_name = "Health_Risk.db"

#Create Database Method
def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

#Create Table Method
def create_tables(conn, cursor):
    if conn is None:
        print("ERROR(create_table method): Database connection failed.")
        return False
    try:
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
