import os
import sys
import traceback
from django.conf import settings

# Prevent TensorFlow from searching for CUDA / GPU and reduce memory consumption
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

MODEL_PATH = settings.AI_MODEL_PATH
GDRIVE_FILE_ID = '1wFGyiCBS2JilypI3QvX0uYcWf4TxC2uf'

# Check possible locations for the model file
def resolve_model_path():
    candidate_paths = [
        MODEL_PATH,
        os.path.join(str(settings.BASE_DIR), 'ml_model', 'wastewise_model.keras'),
        os.path.join(os.path.dirname(str(settings.BASE_DIR)), 'ml_model', 'wastewise_model.keras'),
        os.path.join(os.path.dirname(str(settings.BASE_DIR)), 'backend', 'ml_model', 'wastewise_model.keras'),
    ]
    for path in candidate_paths:
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return path
    return MODEL_PATH


def download_model(target_path):
    print(f'Downloading model from Google Drive to {target_path}...', flush=True)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    try:
        import gdown
        gdown.download(id=GDRIVE_FILE_ID, output=target_path, quiet=False, fuzzy=True)
        print(f'Model downloaded successfully to {target_path}', flush=True)
    except Exception as e:
        print(f'Failed to download model: {e}', flush=True)
        traceback.print_exc()
        raise RuntimeError(f'Failed to download model from Google Drive: {e}')


model = None


def get_model():
    global model
    if model is None:
        import tensorflow as tf
        
        target_path = resolve_model_path()
        if not os.path.exists(target_path) or os.path.getsize(target_path) < 1000:
            download_model(target_path)
            
        print(f'Loading model from {target_path}...', flush=True)
        # compile=False avoids loading training optimizers/loss, saving RAM and CPU time
        model = tf.keras.models.load_model(target_path, compile=False)
        print('Model loaded successfully!', flush=True)
    return model


CLASS_LABELS = {
    0: 'E-Waste', 1: 'General', 2: 'Glass',
    3: 'Hazardous', 4: 'Metal', 5: 'Organic',
    6: 'Paper', 7: 'Plastic', 8: 'Textile'
}


def preprocess_image(image_file):
    import numpy as np
    from PIL import Image
    import tensorflow as tf
    
    if hasattr(image_file, 'seek'):
        image_file.seek(0)
        
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img).astype('float32')
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def classify_waste(image_file):
    try:
        import numpy as np
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
        print(f'Error in classify_waste: {e}', flush=True)
        traceback.print_exc()
        return {'success': False, 'error': str(e)}
