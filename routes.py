import os
import numpy as np
from PIL import Image
from flask import Blueprint, request, render_template, json
from model.model import cnn_feature_extractor_loaded, scaler_loaded, svm_clf_loaded, idx_to_label_loaded
from keras_preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    with open('static/assets/waste-categories/description.json', 'r', encoding='utf-8') as f:
        description = json.load(f)
    categories = [
        {
            'name': filename.split('.')[0].replace('_', ' ').capitalize(),
            'image': f'static/assets/waste-categories/{filename}',
            'description': description[filename.split('.')[0]]
        }
        for filename in os.listdir('static/assets/waste-categories')
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ]
    return render_template('index.html', categories=categories)

@main_routes.route('/about')
def about():
    return render_template('about.html')

@main_routes.route('/contact')
def contact():
    return render_template('contact.html')

@main_routes.route('/clasification')
def clasification():
    return render_template('clasification.html')

IMG_WIDTH = 384
IMG_HEIGHT = 512
@main_routes.route('/predict', methods=['POST'])
def make_prediction():
    if svm_clf_loaded is None or scaler_loaded is None or cnn_feature_extractor_loaded is None or idx_to_label_loaded is None:
        return render_template('control/maintenance.html')
    file = request.files['image']
    if 'image' not in request.files:
        return render_template('control/error.html', message="Image file section not found in request. Make sure you uploaded the file through the form provided. Try restarting the upload process from the beginning.")
    if file.filename == '':
        return render_template('control/error.html', message="There are no files selected to upload. Please select an image first before proceeding. Make sure the file is selected on your device.")
    if file:
        try:
            uploaded_file = os.path.join('static/uploads', secure_filename(file.filename))
            if not os.path.exists('static/uploads'):
                os.makedirs('static/uploads')
            file.save(uploaded_file)

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
            predicted_label = predicted_label.capitalize()

            try:
                probabilities = svm_clf_loaded.predict_proba(features_scaled)[0]
                max_idx = int(np.argmax(probabilities))
                probability_dict = f"{probabilities[max_idx] * 100:.1f}"
            except AttributeError:
                probability_dict = {"info": "Probability scores not available"}

            we_do  = [
                {
                    "name": filename.split('.')[0].replace('_', ' ').capitalize(),
                    "image": f"/static/assets/we-do/{predicted_label.lower()}/{filename}"
                }
                for filename in os.listdir("static/assets/we-do/"+ predicted_label.lower())
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
            ]

            return render_template('predicts.html', prediction=predicted_label, probabilities=probability_dict, image_path=uploaded_file, we_do=we_do)
        except Exception as e:
            return render_template('control/error.html', message=f"An error occurred while processing file. Please try again or use a different file. If the error persists, report this issue.")
    return render_template('control/error.html', message="Invalid file format or content. Make sure you upload an image in the correct format. Use JPG, PNG, or JPEG for best results.")

@main_routes.route('/<path:unknown_path>')
def handle_unknown_path(unknown_path):
    return render_template('control/error.html', message=f"Page {unknown_path} not found. Please double check the URL you entered. Make sure the address is correct and matches the page available.")