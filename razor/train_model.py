import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Example dataset loading
data = pd.read_csv('process_behavior_dataset.csv')  # Placeholder, load your actual dataset

# Assume features are in columns 0 to N-1, and the label (0: benign, 1: malicious) is in the last column
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Split the dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForest model (as an example)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'model/threat_detection_model.pkl')
