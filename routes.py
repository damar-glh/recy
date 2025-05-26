from flask import Blueprint, request, jsonify, render_template
from joblib import load

# Blueprint
main_routes = Blueprint('main_routes', __name__)

# Load model dan scaler
with open('model/trash_predict_model_scalar.pkl', 'rb') as scaler_file:
    scaler = load(scaler_file)
with open('model/trash_predict_model_svm.pkl', 'rb') as model_file:
    svm_model = load(model_file)

@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/predict', methods=['POST'])
def make_prediction():
    try:
        input_data = request.get_json()
        scaled_data = scaler.transform([input_data])
        prediction = svm_model.predict(scaled_data)
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400