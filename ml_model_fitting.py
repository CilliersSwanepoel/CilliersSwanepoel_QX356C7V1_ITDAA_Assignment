import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import joblib

# Step 1: Data Preprocessing
database_path = 'heart.db'
with sqlite3.connect(database_path) as conn:
    cleaned_data = pd.read_sql_query("SELECT * FROM heart_data", conn)

X = cleaned_data.drop('target', axis=1)
y = cleaned_data['target']

numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X.select_dtypes(include=['object', 'category']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

X_preprocessed = preprocessor.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

print("Data preprocessing complete.")

# Step 2: Model Training and Evaluation
model = KNeighborsClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=True)
accuracy = report['accuracy']
precision = report['weighted avg']['precision']
recall = report['weighted avg']['recall']
f1_score = report['weighted avg']['f1-score']

print(f"K-Nearest Neighbors Accuracy: {accuracy}")
print(f"K-Nearest Neighbors Precision: {precision}")
print(f"K-Nearest Neighbors Recall: {recall}")
print(f"K-Nearest Neighbors F1 Score: {f1_score}")

# Save the model and preprocessor
joblib.dump(model, 'K-Nearest Neighbors.joblib')
joblib.dump(preprocessor, 'preprocessor.joblib')

print("Model and preprocessor saved successfully.")
