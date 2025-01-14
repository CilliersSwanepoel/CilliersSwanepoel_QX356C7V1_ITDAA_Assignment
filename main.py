import sqlite3
import pandas as pd

csv_file_path = 'heart.csv'
data = pd.read_csv(csv_file_path, delimiter=';')

database_path = 'heart.db'
conn = sqlite3.connect(database_path)

data.to_sql('heart_data', conn, if_exists='replace', index=False)

cursor = conn.cursor()

audit_query = """
SELECT COUNT(*) FROM heart_data
WHERE 
    age NOT BETWEEN 10 AND 120 OR
    trestbps NOT BETWEEN 70 AND 300 OR
    chol NOT BETWEEN 100 AND 600 OR
    thalach NOT BETWEEN 50 AND 250 OR
    sex NOT IN (0, 1) OR
    cp NOT IN (0, 1, 2, 3) OR
    fbs NOT IN (0, 1) OR
    restecg NOT IN (0, 1, 2) OR
    exang NOT IN (0, 1) OR
    slope NOT IN (0, 1, 2) OR
    ca NOT IN (0, 1, 2, 3, 4) OR
    thal NOT IN (0, 1, 2, 3) OR
    target NOT IN (0, 1)
"""

cursor.execute(audit_query)
anomalies_count = cursor.fetchone()[0]

if anomalies_count > 0:
    print(f"There are {anomalies_count} records that do not meet the specified conditions.")
 
    delete_query = """
    DELETE FROM heart_data
    WHERE 
        age NOT BETWEEN 10 AND 120 OR
        trestbps NOT BETWEEN 70 AND 300 OR
        chol NOT BETWEEN 100 AND 600 OR
        thalach NOT BETWEEN 50 AND 250 OR
        sex NOT IN (0, 1) OR
        cp NOT IN (0, 1, 2, 3) OR
        fbs NOT IN (0, 1) OR
        restecg NOT IN (0, 1, 2) OR
        exang NOT IN (0, 1) OR
        slope NOT IN (0, 1, 2) OR
        ca NOT IN (0, 1, 2, 3, 4) OR
        thal NOT IN (0, 1, 2, 3) OR
        target NOT IN (0, 1)
    """

    cursor.execute(delete_query)
    conn.commit()
    print("Anomalous records have been deleted.")
else:
    print("No records found that violate the specified conditions.")

conn.close()
