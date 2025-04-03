import streamlit as st
from streamlit_chat import message
import os
import tempfile
from dotenv import load_dotenv
from api_call import query_api
from query_maker import make_query

load_dotenv()

st.set_page_config(
    page_title="EduRAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_subject" not in st.session_state:
    st.session_state.current_subject = None

# Sidebar Configuration
st.sidebar.title("Learning Settings")

# Subject Selection
subjects = ["General", "Mathematics", "Science", "History", "Computer Science"]
st.session_state.current_subject = st.sidebar.selectbox("Select Subject", subjects)

# Learning Mode
learning_mode = st.sidebar.radio(
    "Select Learning Mode",
    ["Study Assistant", "Quiz Mode", "Summarize Content"]
)

# Document Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Learning Material",
    type=["pdf", "docx", 'doc', 'txt'],
    accept_multiple_files=False,
    help="Upload your study material (textbook, notes, etc.)",
    key="pdf_uploader",
)

if uploaded_file:
    doc_type = uploaded_file.name.rsplit('.', 1)[1]

# Index Management
col1, col2 = st.sidebar.columns(2)
save_index = col1.checkbox("Save Materials", value=False)
load_index = col2.checkbox("Load Materials", value=False)

if save_index and load_index:
    st.sidebar.error("Cannot save and load materials at the same time")
elif save_index:
    index_name = st.sidebar.text_input("Name your study set", value="")
elif load_index:
    if uploaded_file:
        st.sidebar.error("Please remove the file before loading a study set")
    else:
        index_name = st.sidebar.text_input("Enter study set name", value="")
else:
    index_name = None

# Choosing K : (Relevant Documents)
# FIXME: K is not implemented in the API yet
K = st.sidebar.slider("Number of retrieved relevant documents", min_value=1, max_value=10, value=5)

# Main Content Area
st.title(f"EduRAG - Your Personal Learning Assistant 📚")
st.markdown(f"**Current Subject:** {st.session_state.current_subject} | **Mode:** {learning_mode}")

# Mode-specific instructions
if learning_mode == "Study Assistant":
    st.info("Ask any question about your learning material. I'll help you understand the content better!")
elif learning_mode == "Quiz Mode":
    st.info("I'll generate questions based on your learning material to test your knowledge.")
elif learning_mode == "Summarize Content":
    st.info("I'll help you create concise summaries of your learning material.")


# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt_placeholder = {
    "Study Assistant": "Ask your study question here...",
    "Quiz Mode": "Ready for a question?",
    "Summarize Content": "What would you like me to summarize?"
}

if prompt := st.chat_input(prompt_placeholder[learning_mode]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check whether a file has been uploaded
    try:
        if uploaded_file is None and not load_index:
            st.error("Please upload a file or load previous index to use the Study Assistant.")
        else:
            if uploaded_file:   
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{doc_type}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    context_file_path = tmp_file.name
            else:
                context_file_path = None
            # Generate assistant response
            with st.spinner("Generating response..."):
                response = query_api(
                    query=make_query(prompt, learning_mode, st.session_state.current_subject),
                    context_file_path=context_file_path,
                    save_index=save_index,
                    load_index=load_index,
                    index_name=index_name,
                    k=K
                )
                
            with st.chat_message("assistant"):
                st.markdown(f"**{learning_mode}**:")
                st.markdown(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    finally:
        if uploaded_file:
            # Remove the temporary file
            os.unlink(context_file_path)
