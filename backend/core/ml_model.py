import os
import requests
import tensorflow as tf
import numpy as np
from PIL import Image
from django.conf import settings
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = settings.AI_MODEL_PATH
GDRIVE_FILE_ID = '1wFGyiCBS2JilypI3QvX0uYcWf4TxC2uf'

def download_model():
    print('Downloading model from Google Drive...')
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    url = f'https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}'
    session = requests.Session()
    response = session.get(url, stream=True)
    
    # Handle Google Drive large file warning
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            url = url + '&confirm=' + value
            response = session.get(url, stream=True)
            break
    
    with open(MODEL_PATH, 'wb') as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)
    
    print(f'Model downloaded to {MODEL_PATH}')

model = None

def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            download_model()
        print(f'Loading model from {MODEL_PATH}')
        model = tf.keras.models.load_model(MODEL_PATH)
        print('Model loaded!')
    return model

CLASS_LABELS = {
    0: 'E-Waste', 1: 'General', 2: 'Glass',
    3: 'Hazardous', 4: 'Metal', 5: 'Organic',
    6: 'Paper', 7: 'Plastic', 8: 'Textile'
}

def preprocess_image(image_file):
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img).astype('float32')
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def classify_waste(image_file):
    try:
        m = get_model()
        img_array = preprocess_image(image_file)
        preds = m.predict(img_array, verbose=0)
        preds = preds[0]
        predicted_index = int(np.argmax(preds))
        confidence = float(np.max(preds)) * 100.0
        predicted_class = CLASS_LABELS.get(predicted_index, 'Unknown')
        all_scores = {
            CLASS_LABELS.get(i, f'Class_{i}'): float(preds[i]) * 100.0
            for i in range(len(preds))
        }
        return {
            'success': True,
            'class': predicted_class,
            'index': predicted_index,
            'confidence': round(confidence, 1),
            'all_scores': all_scores,
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}
