import numpy as np
from PIL import Image
from flask import Blueprint, request, render_template
from model.model import cnn_feature_extractor_loaded, scaler_loaded, svm_clf_loaded, idx_to_label_loaded
from keras_preprocessing.image import img_to_array

main_routes = Blueprint('main_routes', __name__)

IMG_WIDTH = 384
IMG_HEIGHT = 512

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/predict', methods=['POST'])
def make_prediction():
    if svm_clf_loaded is None or scaler_loaded is None or cnn_feature_extractor_loaded is None or idx_to_label_loaded is None:
        return render_template('error.html', message="Model or scaler not loaded properly.")
    file = request.files['image']
    if 'image' not in request.files:
        return render_template('error.html', message="No file part in the request.")
    if file.filename == '':
        return render_template('error.html', message="No selected file.")
    if file:
        try:
            img = Image.open(file.stream).convert('RGB')
            img_resized = img.resize((IMG_WIDTH, IMG_HEIGHT))
            img_array = img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0

            features = cnn_feature_extractor_loaded.predict(img_array)
            features_flattened = features.reshape(features.shape[0], -1)
            features_scaled = scaler_loaded.transform(features_flattened)

            prediction_index = svm_clf_loaded.predict(features_scaled)[0]
            predicted_label = idx_to_label_loaded.get(prediction_index, "Unknown")

            try:
                probabilities = svm_clf_loaded.predict_proba(features_scaled)[0]
                max_idx = int(np.argmax(probabilities))
                probability_dict = f"{probabilities[max_idx] * 100:.1f}"
            except AttributeError:
                probability_dict = {"info": "Probability scores not available"}
            return render_template('result.html', prediction=predicted_label, probabilities=probability_dict)
        except Exception as e:
            return render_template('error.html', message=f"Error processing the file: {str(e)}")
    return render_template('error.html', message="Invalid file format or content.")