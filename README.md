# EduRAG UI: Interactive Learning Interface

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rag-ui.streamlit.app/)

An intuitive educational interface built with Streamlit that connects to the [EduRAG API](https://github.com/artmiss-gns/RAG_API) for AI-powered learning assistance.

## 🎯 Features

- 📚 **Multiple Learning Modes**:
  - Study Assistant: Get detailed explanations and answers
  - Quiz Mode: Test your knowledge
  - Summarize Content: Create concise study materials

- 📋 **Subject-Specific Learning**:
  - Mathematics
  - Science
  - History
  - Computer Science
  - General Topics

- 📑 **Document Support**:
  - Upload study materials (PDF, DOCX, DOC, TXT)
  - Save and load study sets
  - Contextual question answering

## 🔧 Setup & Installation

1. Clone this repository:
```bash
git clone https://github.com/artmiss-gns/RAG_UI
cd RAG_UI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment: Create a .env file:
```env
API_URL=https://your-api-url
```

4. Run the app:
```bash
streamlit run app/run.py
```

## 🚀 Deployment

### Deploying on Streamlit Cloud

1. Fork this repository
2. Connect your fork to Streamlit Cloud
3. In your Streamlit Cloud dashboard:
   - Go to your app settings
   - Navigate to the "Secrets" section
   - Add the following secret:
     ```
     API_URL = "https://your-deployed-api-url"
     ```

### Important Notes

- The API_URL should point to your deployed EduRAG API instance
- Make sure your API is accessible from the internet
- For local development, you can use the .env file
- For Streamlit Cloud deployment, always use the Secrets management system