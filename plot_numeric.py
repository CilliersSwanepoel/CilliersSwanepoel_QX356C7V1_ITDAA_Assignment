import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database and load the cleaned data
database_path = 'heart.db'
conn = sqlite3.connect(database_path)
cleaned_data = pd.read_sql_query("SELECT * FROM heart_data", conn)
conn.close()

# Define the numeric variables
numeric_vars = ['age', 'trestbps', 'chol', 'thalach']

# Plot the distribution of numeric variables based on the target variable
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

for i, var in enumerate(numeric_vars):
    row, col = divmod(i, 2)
    sns.histplot(data=cleaned_data, x=var, hue='target', kde=True, ax=axes[row, col])
    axes[row, col].set_title(f'Distribution of {var} by Target')

plt.tight_layout()
plt.show()
