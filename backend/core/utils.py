import os
import numpy as np
from PIL import Image
from django.conf import settings

# Attempt to import tensorflow, fallback gracefully if not installed yet
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

_model = None

def get_model():
    global _model
    if not TF_AVAILABLE:
        print("TensorFlow is not installed. Skipping real AI inference.")
        return None
        
    if _model is None:
        if os.path.exists(settings.AI_MODEL_PATH):
            _model = tf.keras.models.load_model(settings.AI_MODEL_PATH)
        else:
            print(f"Model file not found at {settings.AI_MODEL_PATH}")
            return None
    return _model

# The 9 specific waste categories (sorted alphabetically to match Keras training indices)
CLASSES = ['E-Waste', 'General', 'Glass', 'Hazardous', 'Metal', 'Organic', 'Paper', 'Plastic', 'Textile']

def predict_waste(image_path):
    """
    Loads the image, preprocesses it to 224x224, and runs MobileNetV2 inference.
    Returns (predicted_class_name, confidence_percentage).
    """
    model = get_model()
    
    # Fallback if model isn't loaded (e.g. during development/testing)
    if model is None:
        return 'General', 0.0
        
    try:
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        
        # Standard MobileNetV2 preprocessing
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Run inference
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index]) * 100.0
        
        return CLASSES[predicted_index], round(confidence, 1)
        
    except Exception as e:
        print(f"Error during AI prediction: {e}")
        return 'General', 0.0
