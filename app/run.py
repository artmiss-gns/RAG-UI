import streamlit as st
from streamlit_chat import message
import os
import tempfile
import requests
import json

def query_api(context_file_path, query):
    url = "https://growing-bessy-hossein-golmohammadi-03788de4.koyeb.app"
    
    with open(context_file_path, 'rb') as file:
        files = {'context': file}
        data = {'query': query}
    
        with st.spinner():
            response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return json.loads(response.text)["answer"]
    else:
        return f"Error: API request failed with status code {response.status_code}"

st.set_page_config(
    page_title="RAG UI",
    page_icon=":mag:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Configuration")

# PDF file upload
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF file",
    type="pdf",
    accept_multiple_files=False,
    help="Upload a PDF file to extract text and build the knowledge base.",
    key="pdf_uploader",
)

# Choosing K : (Relevant Documents)
# FIXME: 
# ! Add `k` here too as a parameter, currently, only the default value of k=5 is passed
K = st.sidebar.slider("Number of retrieved relevant documents", min_value=1, max_value=10, value=5)

# Main content area
st.title("RAG System")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Getting user input
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if a PDF file has been uploaded
    if uploaded_file is not None:
        print(uploaded_file)
        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Generate assistant response
        response = query_api(tmp_file_path, prompt)
        
        # Remove the temporary file
        os.unlink(tmp_file_path)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        with st.chat_message("assistant"):
            st.markdown("Please upload a PDF file before asking questions.")
        st.session_state.messages.append({"role": "assistant", "content": "Please upload a PDF file before asking questions."})