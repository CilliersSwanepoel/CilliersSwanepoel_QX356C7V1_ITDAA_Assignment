import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

database_path = 'heart.db'
conn = sqlite3.connect(database_path)
cleaned_data = pd.read_sql_query("SELECT * FROM heart_data", conn)
conn.close()

numeric_vars = ['age', 'trestbps', 'chol', 'thalach']

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

for i, var in enumerate(numeric_vars):
    row, col = divmod(i, 2)
    sns.histplot(data=cleaned_data, x=var, hue='target', kde=True, ax=axes[row, col])
    axes[row, col].set_title(f'Distribution of {var} by Target')

plt.tight_layout()
plt.show()
