import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import docx
import pdfkit  # Ensure you have pdfkit and wkhtmltopdf installed

# Load environment variables
load_dotenv()

def generate_academic_draft(research_topic: str, max_tokens: int = 2000) -> str:
    """
    Generate an academic draft using Groq API
    
    Args:
        research_topic (str): The main research topic for the draft
        max_tokens (int, optional): Maximum number of tokens for the generated draft
    
    Returns:
        Optional[str]: Generated academic draft or None if generation fails
    """
    try:
        # Retrieve API key from environment variable
        api_key = os.getenv('GROQ_API_KEY')
        
        # Validate API key
        if not api_key:
            st.error("Groq API key is missing. Please set GROQ_API_KEY in .env file.")
            return None
        
        # Initialize Groq client without proxy settings
        client = Groq(api_key=api_key)
        
        # Construct a comprehensive prompt for academic draft generation
        prompt = f"""
        Generate a structured academic draft on the following research topic: "{research_topic}"
        
        Requirements:
        - Use a formal academic writing style
        - Include an introduction, main body with key arguments, and a conclusion
        - Provide a logical flow of ideas
        - Use academic language and terminology
        - Demonstrate critical thinking and analytical approach
        
        Draft Structure:
        1. Title
        2. Abstract
        3. Introduction
        4. Literature Review
        5. Methodology
        6. Results and Discussion
        7. Conclusion
        8. Potential Future Research Directions
        """
        
        # Generate draft using Groq API
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are an expert academic writing assistant helping to generate a structured research paper draft."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            stream=False
        )
        
        # Extract and return the generated draft
        generated_draft = chat_completion.choices[0].message.content.strip()
        return generated_draft
    
    except Exception as e:
        st.error(f"Error generating academic draft: {e}")
        return None

def handle_download(generated_draft: str, format_choice: str):
    """Handle file download for the selected format"""
    if generated_draft:
        if format_choice == "TXT":
            file_path = "draft.txt"
            with open(file_path, "w") as f:
                f.write(generated_draft)
            with open(file_path, "rb") as f:
                st.download_button("Download as TXT", f, file_name="draft.txt", mime="text/plain")

        elif format_choice == "DOCX":
            file_path = "draft.docx"
            doc = docx.Document()
            doc.add_paragraph(generated_draft)
            doc.save(file_path)
            with open(file_path, "rb") as f:
                st.download_button("Download as DOCX", f, file_name="draft.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        elif format_choice == "PDF":
            file_path = "draft.pdf"
            pdfkit.from_string(generated_draft, file_path)
            with open(file_path, "rb") as f:
                st.download_button("Download as PDF", f, file_name="draft.pdf", mime="application/pdf")

    else:
        st.error("Please generate a draft first by entering a research topic.")
