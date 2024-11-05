import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('your_database.db')
CURSOR = connection.cursor()

# Optionally, you might want to add a function to close the connection
def close_connection():
    connection.close()
