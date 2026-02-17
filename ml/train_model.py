import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("ml/data/Crop_recommendation.csv")

# Keep only N, P, K, ph, rainfall as features
X = data[["N", "P", "K", "ph", "rainfall"]]
y = data["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save model
with open("ml/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model retrained with 5 features and saved as ml/model.pkl")