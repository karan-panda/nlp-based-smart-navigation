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
    "Add Policy": {
        "synonyms": ["Add a policy", "Create new policy", "Register policy"],
        "route": "/add-policy"
    },

    "Buy Policy": {
        "synonyms": ["Purchase insurance", "Get policy", "Buy insurance"],
        "route": "/buy-policy"
    },

    "Claim": {
        "synonyms": ["File a claim", "Claim insurance", "Raise a claim"],
        "route": "/claim"
    },

    "Blogs": {
        "synonyms": ["Read articles", "Insurance blogs", "Latest news"],
        "route": "/blogs"
    },

    "Profile": {
        "synonyms": ["My account", "User profile", "Settings"],
        "route": "/profile"
    }

}

keywords = []
keyword_to_functionality = {}

for intent, details in functionality.items():
    phrases = [intent] + details["synonyms"]
    keywords.extend(phrases)
    for phrase in phrases:
        keyword_to_functionality[phrase] = details["route"]

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
    matched_phrase = keywords[max_score_index]
    matched_functionality = keyword_to_functionality[matched_phrase]
    
    return jsonify({
        "intent": matched_phrase,
        "route": matched_functionality,
        "score": max_score
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)