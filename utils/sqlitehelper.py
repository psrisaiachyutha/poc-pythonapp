import sqlite3
from sqlite3 import Error


def create_database(db_file_name: str):
    """ create a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file_name)

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(db_file_name, table_name, create_table_query):
    connection = None
    try:
        connection = sqlite3.connect(db_file_name)
        cursor = connection.cursor()

        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # creating the table
        cursor.execute(create_table_query)

        connection.close()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

