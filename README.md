# **Smart Navigation Insurance Portal** 🚀  

A **Next.js** web application for seamless navigation through an insurance portal using **Natural Language Processing (NLP)**. Users can type queries, and the system automatically redirects them to the relevant page.  

## **Features**  
✅ **AI-powered Navigation** – Users can enter queries like *"I want to buy a policy"*, and the app redirects them.  
✅ **Bootstrap-based UI** – A modern, responsive design for a smooth user experience.  
✅ **Dynamic Routing** – Next.js file-based routing with automatic redirection.  
✅ **Interactive Components** – Includes a navbar, carousel, and categorized insurance plans.  

## **Tech Stack**  
- **Frontend:** Next.js, React, Bootstrap  
- **Backend API:** Flask (Python)  
- **Intent Detection Model:** Hugging Face **Sentence Transformers** (`msmarco-distilbert-base-tas-b`) & (`all-MiniLM-L6-v2`) Model
- **State Management:** React Hooks (`useState`, `useEffect`, `useRef`)  
- **Navigation:** `next/router` for dynamic route changes  

## **How It Works**  
1. The user enters a **natural language query** in the search bar (e.g., *"I want to buy an insurance policy"*).  
2. The frontend sends the query to a **Flask API** for processing.  
3. The API uses **Hugging Face Sentence Transformers** to extract intent and determine the best matching route.  
4. The response (e.g., `{ "intent": "Buy Policy", "route": "/buy-policy", "score": 0.90 }`) is sent back to the frontend.  
5. If a valid route is found, **Next.js automatically redirects** the user using `router.push(res.data.route)`.  

## **Setup & Installation**  

### **Frontend (Next.js)**
1️⃣ Clone the repository  
```bash
git clone --recurse-submodules https://github.com/karan-panda/nlp-based-smart-navigation
cd nlp-based-smart-navigation
```

2️⃣ Install dependencies
```
npm install
```

3️⃣ Start the development server
```
npm run dev
```

4️⃣ Ensure the backend API is running for NLP-based navigation.

### **Backend (Flask API with Sentence Transformers)**

1️⃣ Install dependencies
```
pip install flask flask_cors sentence-transformers
```

2️⃣ Generate a **Hugging Face API Key**
To use **Sentence Transformers** from Hugging Face, you need an API key.
  
  1. Go to [Hugging Face](https://huggingface.co/join) and create an account (if you don’t have one).  
  2. Navigate to [**Access Tokens**](https://huggingface.co/settings/tokens).  
  3. Click **New Token**, set **read** permissions, and generate the key.  
  4. Copy the key and paste it in .env or in the .py file for local use.

3️⃣ Run the Flask server
```
python apiV2.py
```
