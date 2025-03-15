from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

MODEL = [
    "sentence-transformers/msmarco-distilbert-base-tas-b",
    "sentence-transformers/all-MiniLM-L6-v2"
]

API_URL = f"https://api-inference.huggingface.co/models/{MODEL[0]}"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

functionality = {
    "Add Policy": "/add-policy",
    "Buy Policy": "/buy-policy",
    "Claim": "/claim",
    "Blogs": "/blogs",
    "Profile": "/profile"
}

keywords = list(functionality.keys())

def query_nlp(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request Error: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON Decode Error: {str(e)}"}

@app.route("/analyze", methods=["POST"])
def analyze_intent():
    data = request.get_json()
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    response_data = query_nlp({
        "inputs": {
            "source_sentence": user_query,
            "sentences": keywords
        }
    })
    
    if isinstance(response_data, dict) and "error" in response_data:
        return jsonify(response_data), 500
    
    max_score = max(response_data)
    max_score_index = response_data.index(max_score)
    matched_keyword = keywords[max_score_index]
    matched_functionality = functionality[matched_keyword]
    
    return jsonify({
        "intent": matched_keyword,
        "route": matched_functionality,
        "score": max_score
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)