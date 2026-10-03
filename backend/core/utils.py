import os
from django.conf import settings

_model = None

def get_model():
    global _model
    if _model is None:
        try:
            import tensorflow as tf
        except ImportError:
            print("TensorFlow is not installed. Skipping real AI inference.")
            return None

        if os.path.exists(settings.AI_MODEL_PATH):
            _model = tf.keras.models.load_model(settings.AI_MODEL_PATH)
        else:
            print(f"Model file not found at {settings.AI_MODEL_PATH}")
            return None
    return _model

CLASSES = ['E-Waste', 'General', 'Glass', 'Hazardous', 'Metal', 'Organic', 'Paper', 'Plastic', 'Textile']

def predict_waste(image_path):
    """
    Loads the image, preprocesses it to 224x224, and runs MobileNetV2 inference.
    Returns (predicted_class_name, confidence_percentage).
    """
    model = get_model()
    
    if model is None:
        return 'General', 0.0
        
    try:
        import numpy as np
        from PIL import Image
        import tensorflow as tf
        
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index]) * 100.0
        
        return CLASSES[predicted_index], round(confidence, 1)
        
    except Exception as e:
        print(f"Error during AI prediction: {e}")
        return 'General', 0.0
