# Academic Paper Generator and Validator

A streamlined application for academic writing assistance with powerful tools for generating drafts, analyzing writing styles, and language support.

## Key Features
### 📝 Academic Draft Generator
Create well-structured academic drafts tailored to your research topic using advanced AI tools.

### ✍️ Writing Style Analysis
Evaluate readability, grammar, style, and detect passive voice for polished academic writing.

### 🌐 Multi-language Support
Easily translate and write academic content in multiple languages with built-in language support.

### 🔍 Publication Search
Search for academic publications based on keywords, authors, or topics, and access a wide range of databases and journals.

### 🧠 Research/Explore
Explore research topics, analyze trends, find related research, and access various academic resources.

### 🎧 Accessibility Features
Leverage text-to-speech functionality and other tools for an inclusive academic writing experience.

## Tech Stack
- **Programming Language**: Python
- **Web Framework**: Streamlit
- **APIs Used**: Groq API for summarization
- **Language Models**: llama-3.3-70b-versatile
- **Other Libraries**:
  - nltk: Natural Language Processing
  - textstat: Text readability metrics
  - language-tool-python: Grammar checking
  - deep-translator: Language translation
  - langdetect: Language detection
  - gTTS: Google Text-to-Speech

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

Run the application:
```bash
streamlit run main.py
```

## Project Overview
This project aims to assist researchers and students in generating high-quality academic papers efficiently. By leveraging AI technology, it provides tools for drafting, analyzing, and improving academic writing.

## Usage Instructions
1. Run the application using the command:
   ```bash
   python main.py
   ```
2. Follow the on-screen instructions to generate drafts and analyze your writing.

## Project Structure
```
Academic Paper Generator and Validator/
├── main.py              # Main application file
├── modules/             # Core functionality modules
│   ├── __init__.py
│   ├── draft_generator.py
│   ├── language_support.py
│   └── writing_style_analyzer.py
├── requirements.txt     # Project dependencies
└── .env                # Environment variables (not in repo)
```

## Dependencies
- streamlit: Web application framework
- groq: AI language model API
- nltk: Natural Language Processing
- textstat: Text readability metrics
- language-tool-python: Grammar checking
- deep-translator: Language translation
- langdetect: Language detection
- gTTS: Google Text-to-Speech

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request detailing your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
