import sqlite3


def create_tables(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open('../migrations/create_database_structure.sql', 'r') as file:
        cursor.executescript(file.read())
    connection.commit()
    connection.close()


# Create the tables
create_tables("../water_pump_db.sqlite")
