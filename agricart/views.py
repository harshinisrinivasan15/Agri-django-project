from pathlib import Path
import os
import json
import numpy as np
import uuid

from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from agricart.form import CustomUserForm
from ml.crop_model import predict_crop  # keep existing usage
from ml.fertilizer_model import predict_fertilizer
import joblib

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from .apps import AgricartConfig
from .utils import preprocess_image
from django.http import JsonResponse
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR/"ml"/"model.pkl"
model = joblib.load(MODEL_PATH)

CLASS_NAMES = [
    "Bacterialblight",
    "Blast",
    "Brownspot",
    "dead_heart",
    "normal",
    "Rice Hispa",
    "Tungro"
]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def home(request):
    return render(request,"agricart/index.html")
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid Username or Password")
                return render("/login")
        return render(request,"agricart/login.html")
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("/")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Registration Success You Can Login Now..!")
            return redirect('login')
        else:
            print(form.errors)
    return render(request,"agricart/register.html",{'form':form})

def cropguide(request):
    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.error(request, "Please Login To Get Crop Prediction.")
            return redirect('login')

        N = int(request.POST.get("nitrogen"))
        P = int(request.POST.get("phosphorous"))
        K = int(request.POST.get("potassium"))
        ph = float(request.POST.get("ph"))
        rainfall = float(request.POST.get("rainfall"))

        result = predict_crop(N, P, K, ph, rainfall)

        return render(request, "agricart/result.html", {"result": result})

    return render(request, "agricart/cropguide.html")


def result(request):
    return render(request,"agricart/result.html")

def disease(request):
    if request.method == "POST" and request.FILES.get("image"):

        if not request.user.is_authenticated:
            messages.error(request, "Please Login To Predict Disease.")
            return redirect('login')

        image_file = request.FILES["image"]

        ext = image_file.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        upload_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

        with open(upload_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        image_url = settings.MEDIA_URL + "uploads/" + filename

        img_array = preprocess_image(upload_path)
        model = AgricartConfig.model

        preds = model.predict(img_array)
        predicted_class = CLASS_NAMES[np.argmax(preds)]
        confidence = round(float(np.max(preds)) * 100, 2)

        return render(request, "agricart/disease_result.html", {
            "disease": predicted_class,
            "confidence": confidence,
            "image_url": image_url
        })

    return render(request, "agricart/disease.html")


def disease_result(request):
    return render(request,"agricart/disease_result.html")

def fertilizer(request):
    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.error(request, "Please Login To Get Fertilizer Recommendation.")
            return redirect('login')

        N = int(request.POST.get('nitrogen'))
        P = int(request.POST.get('phosphorous'))
        K = int(request.POST.get('potassium'))
        crop = request.POST.get('crop')

        ph = 5.5
        soil_moisture = 40

        result = predict_fertilizer(N, P, K, ph, soil_moisture, crop)

        suggestions = {
            "Potash": [
                "The K value of your soil is low.",
                "Mix in muriate of potash or sulphate of potash",
                "Try kelp meal or seaweed",
                "Try Sul-Po-Mag",
                "Bury banana peels below the soil surface",
                "Use Potash fertilizers with high potassium"
            ],
            "Urea": [
                "Your soil has low nitrogen content.",
                "Apply compost or urea fertilizer",
                "Use legume-based cover crops to enrich nitrogen",
                "Add organic matter regularly"
            ],
            "DAP": [
                "Phosphorus is low in your soil.",
                "Add DAP or bone meal",
                "Use rock phosphate for long-term results",
                "Mix composted manure with phosphorus sources"
            ],
            "Balanced": [
                "Your soil nutrients are well balanced!",
                "Maintain organic matter levels",
                "Use compost for steady nutrient release"
            ]
        }

        advice = suggestions.get(result, ["Apply balanced fertilizer as needed."])

        return render(request, "agricart/fertilizer_result.html", {
            "result": result,
            "advice": advice,
            "N": N,
            "P": P,
            "K": K,
            "crop": crop
        })

    return render(request, "agricart/fertilizer.html")

def fertilizer_result(request):
    return render(request,'agricart/fertilizer_result.html')

def chat(request):
    msg = request.POST.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an agriculture expert for Indian farmers."},
            {"role": "user", "content": msg}
        ]
    )

    reply = response.choices[0].message.content
    return JsonResponse({"reply": reply})
