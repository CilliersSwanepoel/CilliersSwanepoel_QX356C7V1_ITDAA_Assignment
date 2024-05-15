import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

database_path = 'heart.db'
conn = sqlite3.connect(database_path)
cleaned_data = pd.read_sql_query("SELECT * FROM heart_data", conn)
conn.close()

cleaned_data['target'] = cleaned_data['target'].astype(str)

categorical_vars = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))

for i, var in enumerate(categorical_vars):
    row, col = divmod(i, 2)
    sns.countplot(data=cleaned_data, x=var, hue='target', ax=axes[row, col])
    axes[row, col].set_title(f'Distribution of {var} by Target')

plt.tight_layout()
plt.show()
