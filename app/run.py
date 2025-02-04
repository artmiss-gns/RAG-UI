import streamlit as st
from streamlit_chat import message
import os
import tempfile
from dotenv import load_dotenv
from api_call import query_api

load_dotenv()


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
    type=["pdf", "docx", 'doc', 'txt'],
    accept_multiple_files=False,
    help="Upload a file to extract text and build the knowledge base.",
    key="pdf_uploader",
)
if uploaded_file:
    doc_type = uploaded_file.name.rsplit('.', 1)[1]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main content area
st.title("RAG System")


col1, col2 = st.sidebar.columns(2)

save_index = col1.checkbox("Save index", value=False)
load_index = col2.checkbox("Load index", value=False)
if save_index and load_index:
    st.sidebar.error("Cannot save and load index at the same time")
elif save_index:
    index_name = st.sidebar.text_input("Enter a name for the index", value="")
elif load_index:
    if uploaded_file:
        # file should be removed if load_index is chosen
        st.sidebar.error("Please remove the file before loading an index")
    else:
        index_name = st.sidebar.text_input("Enter a name for the index", value="")
else:
    index_name = None

# Choosing K : (Relevant Documents)
# FIXME: K is not implemented in the API yet
K = st.sidebar.slider("Number of retrieved relevant documents", min_value=1, max_value=10, value=5)

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
    
    # Check if a file has been uploaded
    try:
        if uploaded_file is not None:
            print(uploaded_file)
            # Create a temporary file to store the PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{doc_type}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                context_file_path = tmp_file.name
        else:
            context_file_path = None
            
        # Generate assistant response
        with st.spinner("Generating response..."):
            response = query_api(
                query=prompt,
                context_file_path=context_file_path,
                save_index=save_index,
                load_index=load_index,
                index_name=index_name,
                k=K
            )
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
            
    finally:
        if uploaded_file:
            # Remove the temporary file
            os.unlink(context_file_path)
