import numpy as np
from tensorflow.keras.preprocessing import image

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0   # SAME as training
    img_array = np.expand_dims(img_array, axis=0)
    return img_array
