from django.apps import AppConfig
from tensorflow.keras.models import load_model
from django.conf import settings
import os

class AgricartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agricart'
    model = None   # 👈 add this

    def ready(self):
        model_path = os.path.join(
            settings.BASE_DIR,
            'ml',
            'rice_disease_model.h5'
        )
        AgricartConfig.model = load_model(model_path)


