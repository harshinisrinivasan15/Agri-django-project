import pickle
import os

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH,"rb") as f:
    model = pickle.load(f)

def predict_crop(N, P, K,ph, rainfall):
    """Takes soil inputs and returns crop recommendation"""
    features = [[N, P, K, ph, rainfall]]
    prediction = model.predict(features)
    return prediction[0]