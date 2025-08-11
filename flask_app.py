from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np

app = Flask(__name__)

# Load the model from the .sav file
model_file = "savemodelgridsearchcv.sav"  # adjust file name if necessary
with open(model_file, "rb") as f:
    model = pickle.load(f)

# Define the mapping of class indices to labels
class_labels = {0: "setosa", 1: "versicolor", 2: "virginica"}

# Enhanced HTML template for the UI
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Iris Prediction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #ffffff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 400px;
        }
        h1 {
            color: #333333;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            color: #333333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Iris Prediction</h1>
        <form action="/" method="post">
            <label for="sepal_length">Sepal Length:</label>
            <input type="number" step="any" name="sepal_length" required>
            <label for="sepal_width">Sepal Width:</label>
            <input type="number" step="any" name="sepal_width" required>
            <label for="petal_length">Petal Length:</label>
            <input type="number" step="any" name="petal_length" required>
            <label for="petal_width">Petal Width:</label>
            <input type="number" step="any" name="petal_width" required>
            <button type="submit">Predict</button>
        </form>
        {% if prediction %}
            <div class="result">
                <h2>Prediction: {{ prediction }}</h2>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        try:
            # Get form data
            features = [
                float(request.form["sepal_length"]),
                float(request.form["sepal_width"]),
                float(request.form["petal_length"]),
                float(request.form["petal_width"]),
            ]
            features = np.array(features).reshape(1, -1)
            pred = model.predict(features)
            prediction = class_labels.get(pred[0], "Unknown")
        except Exception as e:
            prediction = f"Error: {str(e)}"
    return render_template_string(html_template, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)