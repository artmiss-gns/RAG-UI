import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def query_api(query, context_file_path, save_index=False, load_index=False, index_name=None, k=5):
    url = os.getenv("API_URL")
    
    try:
        if context_file_path is None:
            files = None
        else:
            file = open(context_file_path, 'rb')
            files = {'context': file}
                
        form_data = {
            'query': query,
            'save_index': save_index,
            'load_index': load_index,
            'index_name': index_name,
            'k': k
        }
        response = requests.post(
            url, 
            files=files, 
            data=form_data, 
        )
    finally:
        if context_file_path is not None:
            file.close()
            
    print(response.text)
    
    if response.status_code == 200:
        return json.loads(response.text)["answer"]
    else:
        return f"Error: API request failed with status code {response.status_code}\n:{response.text}"
