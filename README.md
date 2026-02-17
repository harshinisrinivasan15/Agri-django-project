#🌾 AGRICART AI 🌿
AI-Powered Smart Agriculture Web Platform (ML + DL + LLM)

A full-stack AI-based web application that helps farmers make smarter decisions using:

🌱 Machine Learning (Crop & Fertilizer Recommendation)

🧠 Deep Learning (Plant Disease Detection)

🤖 Large Language Model – OpenAI (AI-based explanations & suggestions)

##🚀 Features
🌾 Crop Recommendation System

Predicts the best crop based on soil nutrients (N-P-K values), temperature & humidity.

🧪 Fertilizer Recommendation System

Suggests fertilizers based on soil nutrient deficiency or excess.

🍃 Crop Disease Detection

Upload a Crop(Paddy) image

Deep Learning model predicts disease

Provides treatment suggestions

🤖 AI Assistant (LLM Integration)

Uses OpenAI API to:

Explain diseases in simple language

Suggest preventive measures

Provide farming guidance

🛠️ Tech Stack

Backend: Django

Frontend: HTML, CSS

Machine Learning: Scikit-learn

Deep Learning: TensorFlow / Keras

LLM Integration: OpenAI API

Database: SQLite

Version Control: Git & GitHub

🔐 Security

API keys secured using .env

.gitignore configured properly

No secrets exposed in repository

📂 Project Structure
Agri/
│
├── agricart/        # Django app
├── ml/              # Trained ML/DL models
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md

⚙️ How to Run Locally

1️⃣ Clone the repository:

git clone https://github.com/yourusername/your-repo-name.git


2️⃣ Create virtual environment:

python -m venv venv
venv\Scripts\activate


3️⃣ Install dependencies:

pip install -r requirements.txt


4️⃣ Create a .env file in root folder:

OPENAI_API_KEY=your_api_key_here


5️⃣ Run the server:

python manage.py runserver


Open:
http://127.0.0.1:8000/

📊 Data Sources

Custom-built Crop Dataset

Custom-built Fertilizer Dataset

Plant Disease Image Dataset

🎯 Motivation

Agriculture plays a major role in economic development, especially in countries like India.

This project demonstrates how Machine Learning, Deep Learning, and LLMs can be integrated into precision farming systems to assist farmers with intelligent decision-making.

⚠️ Disclaimer

This is a Proof of Concept (POC) project created for educational purposes.
The predictions should not be used for real-world farming decisions without verified agricultural data.

👩‍💻 Author

Harshini Srinivasan
