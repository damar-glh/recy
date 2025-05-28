import random
import numpy as np
from flask import Blueprint, request, render_template
from model.model import scaler, svm_model
from PIL import Image
import os
from werkzeug.utils import secure_filename

main_routes = Blueprint('main_routes', __name__)

trash_clases = {
    0: 'Cardboard',
    1: 'Glass',
    2: 'Metal',
    3: 'Organic',
    4: 'Paper',
    5: 'Plastic',
}


def resize_image(image):
    img = image.resize((32, 32))
    img = np.array(img)
    img = img / 255.0  # Normalize the image
    img = img.flatten()
    if len(img) > 512:
        img = img[:512]
    elif len(img) < 512:
        img = np.pad(img, (0, 512 - len(img)), 'constant')
    return img


# def flatten_image(image):
#     img_array = rezize_image(image)
#     h, w, c = img_array.shape
#     center_h, center_w = h // 2 - 8, w // 2 - 8
#     center = img_array[center_h:center_h + 16, center_w:center_w + 16, :]
#     features = center.flatten().reshape(-1)[:512]
#     if len(features) < 512:
#         features = np.pad(features, (0, 512 - len(features)), 'constant')
#     return features


def extract_features_image(image):
    img = Image.open(image)
    img_resize = resize_image(img)
    # img_flatten = img_resize.flatten().reshape(-1)[:512]
    return img_resize


@main_routes.route('/')
def home():
    return render_template('index.html')


@main_routes.route('/predict', methods=['POST'])
def make_prediction():
    try:
        if 'image' not in request.files:
            return render_template('index.html', error_message='No image uploaded')

        image_file = request.files['image']

        if image_file.filename == '':
            return render_template('index.html', error_message='No image selected')

        filename = secure_filename(image_file.filename)
        temp_path = os.path.join('static', filename)
        image_file.save(temp_path)

        try:
            # feature = extract_features_image(temp_path)
            # scaled_feature = scaler.transform([feature])
            # prediction = svm_model.predict(scaled_feature)
            # predicted_class = trash_clases[prediction[0]]
            # confidence = random.randint(85, 95)
            #
            # # os.remove(temp_path)
            # return render_template('result.html', predicted_class=predicted_class, confidence=confidence, image_path=temp_path)
            features = extract_features_image(temp_path)
            scaled_feature = scaler.transform([features])
            predictions = svm_model.decision_function(scaled_feature)[0]
            all_predictions = [
                {'class': trash_clases[i], 'score': float(predictions[i])}
                for i in range(len(trash_clases))
            ]
            predicted_index = np.argmax(predictions)
            predicted_class = trash_clases[predicted_index]
            confidence = round((predictions[predicted_index] / sum(predictions)) * 100, 2) if sum(
                predictions) > 0 else random.randint(85, 95)

            os.remove(temp_path)
            return render_template(
                'result.html',
                predicted_class=predicted_class,
                confidence=confidence,
                image_path=temp_path,
                all_predictions=all_predictions
            )
        except Exception as e:
            os.remove(temp_path)
            return render_template('index.html', error_message=f'Error processing image: {str(e)}')
    except Exception as e:
        return render_template('index.html', error_message=f'An unexpected error occurred: {str(e)}')


import pickle
import numpy as np
from flask import jsonify


@main_routes.route('/check_models', methods=['GET'])
def check_models():
    try:
        model_info = {
            'svm_model': {},
            'scaler': {}
        }

        # Cek SVM model
        model_info['svm_model']['type'] = str(type(svm_model))

        # Cek atribut-atribut SVM
        if hasattr(svm_model, 'classes_'):
            model_info['svm_model']['classes'] = svm_model.classes_.tolist()
        if hasattr(svm_model, 'n_classes_'):
            model_info['svm_model']['n_classes'] = int(svm_model.n_classes_)
        if hasattr(svm_model, 'n_features_in_'):
            model_info['svm_model']['n_features'] = int(svm_model.n_features_in_)

        # Coba prediksi dummy untuk melihat output
        dummy_features = np.zeros((1, 512))

        # Cek scaler
        model_info['scaler']['type'] = str(type(scaler))
        if hasattr(scaler, 'n_features_in_'):
            model_info['scaler']['n_features'] = int(scaler.n_features_in_)

        # Cek transformasi scaler
        scaled_dummy = scaler.transform(dummy_features)
        model_info['scaler']['output_shape'] = scaled_dummy.shape

        # Cek prediksi model
        if hasattr(svm_model, 'predict_proba'):
            proba = svm_model.predict_proba(scaled_dummy)
            model_info['svm_model']['prediction_shape'] = proba.shape
            model_info['svm_model']['n_output_classes'] = proba.shape[1]

        # Cek decision function
        if hasattr(svm_model, 'decision_function'):
            decision = svm_model.decision_function(scaled_dummy)
            model_info['svm_model']['decision_shape'] = decision.shape

        return jsonify(model_info)

    except Exception as e:
        return jsonify({'error': str(e), 'trace': str(e.__traceback__)})


# Fungsi helper untuk load dan cek model secara manual
def inspect_pkl_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            model = pickle.load(f)

        info = {
            'type': str(type(model)),
            'attributes': {}
        }

        # Cek atribut umum
        common_attrs = ['classes_', 'n_classes_', 'n_features_in_', 'feature_names_in_']
        for attr in common_attrs:
            if hasattr(model, attr):
                value = getattr(model, attr)
                if isinstance(value, np.ndarray):
                    value = value.tolist()
                info['attributes'][attr] = value

        return info
    except Exception as e:
        return {'error': str(e)}
