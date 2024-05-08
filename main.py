import sqlite3
import pandas as pd

# Load data from CSV file
csv_file_path = 'heart.csv'
data = pd.read_csv(csv_file_path, delimiter=';')

# Create a SQLite database connection
database_path = 'heart.db'  # This will create the database file in the current directory
conn = sqlite3.connect(database_path)

# Write the data to a table named 'heart_data'
data.to_sql('heart_data', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
