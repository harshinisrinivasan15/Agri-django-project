import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def train_fertilizer_model():
    data = pd.read_csv(os.path.join(BASE_DIR, 'data/fertilizer.csv'))

    # Encode crop names to numbers
    le_crop = LabelEncoder()
    data['Crop'] = le_crop.fit_transform(data['Crop'])

    # Features (N, P, K, pH, soil_moisture, Crop)
    X = data[['N', 'P', 'K', 'pH', 'soil_moisture', 'Crop']]

    # Target: classify fertilizer type based on soil condition
    # We'll generate fertilizer class automatically
    def classify(row):
        if row['K'] < 30:
            return "Potash"
        elif row['N'] < 40:
            return "Urea"
        elif row['P'] < 30:
            return "DAP"
        else:
            return "Balanced"

    data['Fertilizer'] = data.apply(classify, axis=1)
    y = data['Fertilizer']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, os.path.join(BASE_DIR, 'fertilizer_model.pkl'))
    joblib.dump(le_crop, os.path.join(BASE_DIR, 'fertilizer_label_encoder.pkl'))

    print("✅ Fertilizer model trained successfully!")

def predict_fertilizer(N, P, K, ph, soil_moisture, crop):
    model = joblib.load(os.path.join(BASE_DIR, 'fertilizer_model.pkl'))
    le_crop = joblib.load(os.path.join(BASE_DIR, 'fertilizer_label_encoder.pkl'))

    crop_encoded = le_crop.transform([crop])[0]
    features = [[N, P, K, ph, soil_moisture, crop_encoded]]
    prediction = model.predict(features)[0]
    return prediction

if __name__ == "__main__":
    train_fertilizer_model()
