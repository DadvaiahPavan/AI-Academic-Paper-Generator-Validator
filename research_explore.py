import os
import logging
import streamlit as st
import torch
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Groq API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to extract text from a DOCX file
def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return ""

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to split document into chunks
def split_document_into_chunks(document_text):
    return [chunk.strip() for chunk in document_text.split('\n') if chunk.strip()]  

# Function to perform semantic search using Groq API with llama-3.3-70b-versatile model
def semantic_search_llama(query, document_chunks, max_results=3):
    api_url = 'https://api.groq.com/openai/v1/chat/completions'  # Corrected endpoint for Groq API
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    results = []
    
    for chunk in document_chunks:
        data = {
            'model': 'llama-3.3-70b-versatile',  # Specify the model
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{query} in context: {chunk}"}
            ],
            'temperature': 0.5,
            'max_tokens': 100,
            'top_p': 1.0,
            'frequency_penalty': 0,
            'presence_penalty': 0
        }
        
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            result_text = response_json['choices'][0]['message']['content'].strip()
            results.append(result_text)
            if len(results) >= max_results:
                break
        else:
            st.error(f"Error in API call: {response.status_code} - {response.text}")
            break
    
    return results

# Function to display the Research/Explore section
def show_research_explore():
    st.title("Research/Explore Section")
    st.write("This is where users can perform detailed semantic searches.")
    
    # Upload a document
    uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Process uploaded file
        if uploaded_file.type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document_text = extract_text_from_docx(uploaded_file)
        else:
            document_text = uploaded_file.read().decode("utf-8")  # For .txt files
        
        document_chunks = split_document_into_chunks(document_text)
        
        # Initialize query variable
        query = st.text_input("Enter your search query:")
        max_results = st.selectbox("Select Max Results", [1, 5, 10])
        
        if st.button("Search"):
            if query:  # Ensure query is not empty
                st.write(f"Debug: Search button clicked with query: {query}")  # Debugging output
                
                # Show a spinner while performing the search
                with st.spinner("Searching for relevant content..."):
                    results = semantic_search_llama(query, document_chunks, max_results)
                
                st.write("### Search Results:")
                
                if results:
                    for idx, result in enumerate(results):
                        st.write(f"**Result {idx+1}**")
                        st.write(result)
                else:
                    st.write("No relevant content found.")
            else:
                st.error("Please enter a search query.")

# Call the render function in your main app logic
if __name__ == "__main__":
    show_research_explore()
