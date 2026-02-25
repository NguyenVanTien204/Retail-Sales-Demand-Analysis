import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
from psycopg2 import connect, sql

env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

databaseURL = os.getenv("DATABASE_URL")
print("Database URL:", databaseURL)

def create_connection():
    try:
        conn = connect(databaseURL)
        print("Connection to database established.")
        return conn
    except Exception as e:
        print("Error connecting to database:", e)
        return None



def load_data_to_db(dataframe):
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    for index, row in dataframe.iterrows():
        insert_query = sql.SQL("""
            INSERT INTO your_table_name (column1, column2)
            VALUES (%s, %s)
        """)
        cursor.execute(insert_query, (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded to database successfully.")

def downcast_int(df):
    for col in df.select_dtypes(include=['int64']).columns:
        if col != 'units_sold': # giữ units_sold là int nếu cần
            df[col] = pd.to_numeric(df[col], downcast='integer')
    return df
