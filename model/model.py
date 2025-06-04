from joblib import load
from tensorflow.keras.models import load_model

cnn_feature_extractor_loaded = load_model('model/feature_extractor_model.keras')
with open('model/scaler_model.pkl', 'rb') as scaler_file:
    scaler_loaded = load(scaler_file)
with open('model/svm_classifier_model.pkl', 'rb') as model_file:
    svm_clf_loaded = load(model_file)
with open('model/class_indices.pkl', 'rb') as class_indices:
    class_indices_loaded = load(class_indices)
    idx_to_label_loaded = {v: k for k, v in class_indices_loaded.items()}