from flask import Flask, render_template
import pickle, sklearn

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Load the pre-trained model
with open('model/svm_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
# Ensure the model is loaded correctly
if not isinstance(model, sklearn.base.BaseEstimator):
    raise ValueError("The loaded model is not a valid scikit-learn estimator.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')