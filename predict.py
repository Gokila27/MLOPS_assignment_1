import requests

def send_prediction_request(features):
    url = "http://127.0.0.1:5000/predict"  # Flask app URL
    payload = {"features": features}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Prediction:", response.json()["prediction"])
        else:
            print("Error:", response.json())
    except Exception as e:
        print("An error occurred:", e)

# Example usage
send_prediction_request([5.1, 3.5, 1.4, 0.2])