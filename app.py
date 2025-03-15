import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

Model = [
    "sentence-transformers/msmarco-distilbert-base-tas-b",
    "sentence-transformers/all-MiniLM-L6-v2",
]

API_URL = "https://api-inference.huggingface.co/models/" + Model[0]
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        print(f"Response content: {response.text}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response content: {response.text}")
        return None

user_ip = input("Enter your query: ")

functionality = {
    "Add Policy": "/add-policy",
    "Buy Policy": "/buy-policy",
    "Claim": "/claim",
    "Blogs": "/blogs",
    "Profile": "/profile"
}

keywords = list(functionality.keys())

data = query({
    "inputs": {
        "source_sentence": user_ip,
        "sentences": keywords 
    }
})

if data is not None:
    max_score = max(data)
    max_score_index = data.index(max_score)
    matched_keyword = keywords[max_score_index]
    matched_functionality = functionality[matched_keyword]

    users_intent = f"{matched_keyword}: {matched_functionality}"
    print(f"Similarity scores: {max_score}")
    print(f"User's intent: {users_intent}")
else:
    print("No data returned from the API")