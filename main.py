import streamlit as st
import sys
import os
from modules.writing_style_analyzer import AcademicWritingStyleAnalyzer
from modules.draft_generator import generate_academic_draft
from modules.language_support import MultiLanguageSupport
from modules.publication_search import PublicationSearcher
import re
from research_explore import show_research_explore  # Remove the upload_file import
import docx
import pdfkit  # Ensure you have pdfkit and wkhtmltopdf installed
from modules.draft_generator import generate_academic_draft, handle_download
from accessibility import Accessibility
import PyPDF2

# Initialize the Accessibility class
accessibility = Accessibility()

# Page configuration
st.set_page_config(
    page_title="Academic Paper Generator & Validator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
div.block-container {padding-top: 1rem;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Initialize session state for current page if not exists
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Initialize components
if 'writing_analyzer' not in st.session_state:
    st.session_state.writing_analyzer = AcademicWritingStyleAnalyzer()
if 'publication_searcher' not in st.session_state:
    st.session_state.publication_searcher = PublicationSearcher()


@st.cache_resource
def load_model():
    # Load your heavy model here
    # Replace with actual model loading code
    model = None  # Replace with actual model loading code
    return model  
    

def render_home():
    """
    Render a fully responsive home page for Academic Paper Generator & Validator with 3D effects and animations.
    """
    # Enhanced Responsive CSS with 3D and Animation Effects
    st.markdown("""
    <style>
    /* Global Responsive Styles */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px !important;
        }
    }

    /* Hero Section Responsive */
    .hero-section {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        color: #000000;
        padding: 2rem 1rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 1rem;
        animation: fadeIn 1.5s ease-in-out;
    }
    .hero-section h1 {
        font-size: clamp(1.5rem, 5vw, 3rem);
        margin-bottom: 1rem;
    }
    .hero-section p {
        font-size: clamp(0.9rem, 3vw, 1.2rem);
    }

    /* Keyframes for animations */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Feature Section */
    .feature-section {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    }
    .feature-card {
        flex: 1;
        min-width: 250px;
        max-width: 350px;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in-out;
    }
    .feature-card:hover {
        transform: scale(1.05);
        animation: pulse 1s infinite;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #58a6ff;
    }

    /* Responsive CTA Button */
    .cta-button {
        display: inline-block;
        background-color: #2ea44f;
        color: white !important;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 1rem;
        transition: background-color 0.3s ease;
    }
    .cta-button:hover {
        background-color: #2c974b;
    }

    /* Footer Section */
    .footer-disclaimer {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        text-align: center;
    }
    .footer-disclaimer strong {
        color: #d9534f;
    }
    .footer-disclaimer p {
        margin: 0;
        color: #343a40;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>Academic Paper Generator & Validator</h1>
        <p>Revolutionizing Academic Writing with AI</p>
        <p>Discover, Analyze, and Innovate in Academic Research</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Sections
    st.markdown("<h3>Key Features:</h3>", unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("""
    <style>
        .tech-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .tech-item {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: left;
            animation: fadeIn 1s ease-in-out;
        }
        .tech-item h4 {
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .tech-item p {
            margin: 0;
            color: #7f8c8d;
        }
    </style>
    <div class="tech-section">
        <div class="tech-item">
            <h4>📝 Academic Draft Generator</h4>
            <p>Create well-structured academic drafts tailored to your research topic using advanced AI tools.</p>
        </div>
        <div class="tech-item">
            <h4>✍️ Writing Style Analysis</h4>
            <p>Evaluate readability, grammar, style, and detect passive voice for polished academic writing.</p>
        </div>
        <div class="tech-item">
            <h4>🌐 Multi-language Support</h4>
            <p>Easily translate and write academic content in multiple languages with built-in language support.</p>
        </div>
        <div class="tech-item">
            <h4>🔍 Publication Search</h4>
            <p>Search for academic publications based on keywords, authors, or topics, and access a wide range of databases and journals.</p>
        </div>
        <div class="tech-item">
            <h4>🧠 Research/Explore</h4>
            <p>Explore research topics, analyze trends, find related research, and access various academic resources.</p>
        </div>
        <div class="tech-item">
            <h4>🎧 Accessibility Features</h4>
            <p>Leverage text-to-speech functionality and other tools for an inclusive academic writing experience.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer-like section
    st.markdown("""
    <div class="footer-disclaimer">
        <p><strong>Disclaimer:</strong> This is an AI-assisted academic writing tool. Always consult with academic mentors or experts for final reviews before publication.</p>
    </div>
    """, unsafe_allow_html=True)

    # Including three.js for 3D effects
    st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Create scene, camera, and renderer
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Create a 3D object (cube)
        const geometry = new THREE.BoxGeometry();
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        camera.position.z = 5;

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();
    });
    </script>
    """, unsafe_allow_html=True)

    # Including anime.js for animations
    st.markdown("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        anime({
            targets: '.feature-card',
            translateY: [-10, 10],
            direction: 'alternate',
            loop: true,
            easing: 'easeInOutSine',
            duration: 2000
        });
    });
    </script>
    """, unsafe_allow_html=True)




def render_draft_generator():
    st.title("Academic Draft Generator")
    
    # Step 1: User input for the research topic
    research_topic = st.text_input("Enter your research topic:")

    # Step 2: Button to generate the draft
    if st.button("Generate Draft"):
        if research_topic:
            # Display a spinner while generating the draft
            with st.spinner("Generating draft..."):
                model = load_model()  # Load model on demand
                generated_draft = generate_academic_draft(research_topic, model)
                if generated_draft:
                    st.session_state.generated_draft = generated_draft
        else:
            st.error("Please enter a research topic.")
    
    # Display the generated draft (only once)
    if 'generated_draft' in st.session_state:
        st.write(st.session_state.generated_draft)
        
        # Step 3: Choose download format
        download_format = st.selectbox("Choose download format:", ["TXT", "DOCX"])

        # Handle download functionality
        handle_download(st.session_state.generated_draft, download_format)

    # Additional UI elements (if necessary)
    st.write("Use the form to input a research topic and generate an academic draft.")



def render_writing_style():
    st.title("Writing Style Analysis")
    
    # Initialize analyzer only once using st.session_state
    if 'writing_analyzer' not in st.session_state:
        with st.spinner("Initializing writing style analyzer..."):
            st.session_state.writing_analyzer = AcademicWritingStyleAnalyzer()
    
    text = st.text_area("Enter your academic text for analysis:", height=200)
    
    if st.button("Analyze Writing Style"):
        if text:
            with st.spinner("Analyzing your text... This may take a moment."):

                try:
                    # Analyze readability
                    readability_scores = st.session_state.writing_analyzer.analyze_readability(text)

                    # Display readability metrics
                    st.subheader("📊 Readability Metrics")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Flesch Reading Ease", f"{readability_scores['flesch_reading_ease']:.1f}")
                        st.metric("Gunning Fog Index", f"{readability_scores['gunning_fog']:.1f}")
                        st.metric("SMOG Index", f"{readability_scores['smog_index']:.1f}")

                    with col2:
                        st.metric("Flesch-Kincaid Grade", f"{readability_scores['flesch_kincaid_grade']:.1f}")
                        st.metric("Coleman-Liau Index", f"{readability_scores['coleman_liau_index']:.1f}")
                        st.metric("Automated Readability", f"{readability_scores['automated_readability_index']:.1f}")

                    # Check grammar and style
                    st.subheader("🔍 Grammar and Style Analysis")
                    with st.spinner("Analyzing text..."):
                        issues = st.session_state.writing_analyzer.check_grammar(text)
                        
                        if issues:
                            st.markdown("### ✍️ Grammar Issues")
                            for issue in issues:
                                incorrect_word = issue['incorrect']
                                suggestions = issue['suggestions']
                                
                                # Create a clearer format for each issue
                                st.markdown(f"**Wrong word:** ❌ `{incorrect_word}`")
                                if suggestions:
                                    st.markdown("**Should be replaced with:**")
                                    for suggestion in suggestions:
                                        st.markdown(f"✅ `{suggestion}`")
                                st.markdown("---")  # Add a separator between issues
                        else:
                            st.success("✨ Excellent! No significant grammar issues found.")
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
        else:
            st.warning("Please enter some text to analyze.")


def render_language_support():
    st.title("Language Support")
    translator = MultiLanguageSupport()
    
    languages = [
        "French",
        "German",
        "Italian",
        "Portuguese",
        "Dutch",
        "Polish",
        "Russian",
        "Japanese",
        "Korean",
        "Chinese (Simplified)"
    ]
    
    # Text input
    text = st.text_area("Enter text:", height=150, help="Enter text for language detection and translation")
    
    # Detect Language button
    if st.button("Detect Language"):
        if text:
            detected_code, detected_name = translator.detect_language(text)
            st.success(f"Detected Language: {detected_name}")
        else:
            st.warning("Please enter text to detect its language.")
    
    # Translation section
    st.subheader("Translation")
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox("Source Language", translator.get_supported_languages())
    with col2:
        target_lang = st.selectbox("Target Language", translator.get_supported_languages())
    
    if st.button("Translate"):
        if text:
            with st.spinner("Translating... Please wait."):
                translation = translator.translate_text(text, target_lang)
                st.text_area("Translated Text:", translation, height=600)
        else:
            st.warning("Please enter text to translate.")


def render_publication_search():
    st.title("📚 Academic Publication Search")
    
    # Get available domains
    domains = st.session_state.publication_searcher.get_domain_suggestions()
    
    # Search interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Enter your research topic or keywords:", 
                                   placeholder="e.g., AI in healthcare, machine learning for medical diagnosis")
    
    with col2:
        selected_domain = st.selectbox("🎯 Select Domain:", domains)
    
    # Search button and result limit
    col3, col4, col5 = st.columns([1, 1, 2])
    
    with col3:
        limit = st.number_input("📊 Number of results:", min_value=5, max_value=50, value=10)
    
    with col4:
        search_button = st.button("🔍 Search Publications", use_container_width=True)
    
    # Perform search when button is clicked
    if search_button and search_query:
        with st.spinner("🔄 Searching academic publications..."):
            results = st.session_state.publication_searcher.search_publications(
                search_query, selected_domain, limit
            )
            
            if results:
                st.markdown(f"### Found {len(results)} Publications")
                
                for i, pub in enumerate(results, 1):
                    # Calculate relevance indicator
                    score = pub.get('score', 0)
                    relevance = "🟢 High" if score > 4 else "🟡 Medium" if score > 2 else "🔴 Low"
                    
                    with st.expander(f"{i}. {pub['title']}", expanded=i==1):
                        # Two columns: main content and metadata
                        col_main, col_meta = st.columns([3, 1])
                        
                        with col_main:
                            # Authors
                            st.markdown(f"**Authors:** {', '.join(pub['authors'])}")
                            
                            # Abstract
                            st.markdown("**Abstract:**")
                            st.markdown(pub['summary'])
                            
                            # Link to paper
                            st.markdown(f"[📄 View Full Paper]({pub['link']})")
                        
                        with col_meta:
                            st.markdown(f"""
                            **Relevance:** {relevance}
                            
                            **Domain:** {pub['domain']}
                            
                            **Published:** {pub['published'][:10]}
                            
                            **Source:** {pub['source']}
                            """)
            else:
                st.warning("No publications found. Try modifying your search terms or selecting a different domain.")
                st.markdown("""
                **Search Tips:**
                - Use more specific keywords
                - Try different combinations of terms
                - Check if the domain matches your topic
                - Include relevant technical terms
                """)
    
    # Show tips when no search is performed
    if not search_button:
        st.markdown("""
        ### 💡 Search Tips
        - Use specific keywords related to your research interest
        - Select the most relevant domain for better results
        - Try different combinations of keywords
        - Use technical terms common in your field
        
        **Example Searches:**
        - "AI in healthcare diagnosis"
        - "machine learning medical imaging"
        - "deep learning patient monitoring"
        """)

def render_research_explore():
    show_research_explore()

def render_text_to_speech():
    st.header('Text-to-Speech')
    text_input = st.text_area('Enter text to convert to speech:')
    if st.button('Convert to Speech'):
        if text_input:
            with st.spinner('Converting text to speech...'):
                audio_buffer = accessibility.text_to_speech(text_input)
                st.audio(audio_buffer.read(), format='audio/mp3')  # Use `.read()` to get the content
                st.success('Text converted to speech!')
        else:
            st.error('Please enter some text to convert.')

def render_About():
    st.markdown("""
    <style>
    /* Keyframes for Animations */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes slideIn {
        0% { transform: translateY(50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* General Styles */
    .animated-title, .project-intro, .capabilities, .author-section, .cta-section, .image-container {
        animation: fadeIn 2s ease-in-out;
        font-size: 1.1rem;
        color: #34495e;
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .animated-title {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }

    .capabilities ul {
        list-style-type: none;
        padding: 0;
    }

    .capabilities ul li {
        margin: 10px 0;
        padding-left: 1.5em;
        text-indent: -1.5em;
        display: flex;
        align-items: center;
    }

    .capabilities ul li::before {
        content: '🚀';
        margin-right: 0.5em;
        animation: slideIn 1.5s ease-in-out;
    }

    .author-section a {
        color: #2980b9;
        text-decoration: none;
        font-weight: bold;
    }

    .author-section a:hover {
        text-decoration: underline;
    }

    .image-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    .image-container img {
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        animation: slideIn 1.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="animated-title">About the Academic Paper Generator and Validator</div>', unsafe_allow_html=True)

    # Short Project Introduction
    st.markdown("""
    <div class="project-intro">
        The <strong>Academic Paper Generator and Validator</strong> is a comprehensive AI-powered tool designed to assist researchers, students, and professionals in crafting high-quality academic papers.
        By leveraging cutting-edge AI technologies, this platform accelerates the drafting process, enhances writing quality, and ensures the accuracy of references and citations.
        This tool is ideal for anyone looking to streamline the academic writing process while maintaining high standards of quality.
    </div>
    """, unsafe_allow_html=True)

    # Capabilities Section with Bullet Points and Emphasis
    st.markdown('<div class="capabilities"><h3>Capabilities:</h3>', unsafe_allow_html=True)
    st.markdown("""
    <ul>
        <li><strong>Accelerated Draft Generation</strong>: Quickly create well-structured academic drafts tailored to your research topic.</li>
        <li><strong>Writing Style Enhancement</strong>: Improve grammar, readability, and overall style with advanced AI-powered analysis.</li>
        <li><strong>Multi-language Support</strong>: Easily write and translate academic papers in multiple languages for global collaboration.</li>
        <li><strong>Publication Search</strong>: Search for academic publications based on keywords, authors, or topics, and access a wide range of databases and journals.</li>
        <li><strong>Research Exploration Tools</strong>: Explore trends, find related research, and access academic resources to enrich your work.</li>
        <li><strong>Enhanced Accessibility</strong>: Proofread and review your drafts using integrated <strong>Text-to-Speech</strong> functionality, ensuring accessibility for all users.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Author Section with a Bio and Call to Action
    st.markdown('<div class="author-section"><h3>👨‍💻 Author:</h3>', unsafe_allow_html=True)
    st.markdown("""
    This project was developed by <strong>Dadvaiah Pavan</strong>, a passionate developer and AI enthusiast with expertise in <strong>Artificial Intelligence</strong> and <strong>Machine Learning</strong>.
    With a focus on improving academic writing processes, Dadvaiah Pavan created this tool to bridge the gap between cutting-edge AI research and practical academic needs.
    The aim is to empower students, researchers, and academics by providing a comprehensive platform that helps in generating, enhancing, and validating high-quality academic papers with ease.
    Explore more of my work on my <a href="https://github.com/DadvaiahPavan">GitHub</a> or visit my <a href="https://pavandadvaiah.netlify.app/">portfolio</a> for further details.
    </div>
    """, unsafe_allow_html=True)

    # Image related to AI in Academic Writing
    st.markdown('<div class="image-container"><img src="https://i.ibb.co/mSGptyV/67641a8342db5.png" alt="AI-Powered Academic Writing Assistance"></div>', unsafe_allow_html=True)




def render_sidebar():
    with st.sidebar:
        st.title("📄 Academic Paper Generator")
        st.markdown("---")
        
        # Navigation buttons in sidebar
        if st.button("🏠 Home", key="sidebar_home", use_container_width=True):
            st.session_state.current_page = "Home"
        
        if st.button("📝 Draft Generator", key="sidebar_draft_generator", use_container_width=True):
            st.session_state.current_page = "Draft Generator"
        
        if st.button("✍️ Writing Style", key="sidebar_writing_style", use_container_width=True):
            st.session_state.current_page = "Writing Style"
        
        if st.button("🌍 Language Support", key="sidebar_language_support", use_container_width=True):
            st.session_state.current_page = "Language Support"
        
        if st.button("🔍 Publication Search", key="sidebar_publication_search", use_container_width=True):
            st.session_state.current_page = "Publication Search"
        
        if st.button("🔬 Research/Explore", key="sidebar_research_explore", use_container_width=True):
            st.session_state.current_page = "Research/Explore"
        
        if st.button("🗣️ Text-to-Speech", key="sidebar_text_to_speech", use_container_width=True):
            st.session_state.current_page = "Text-to-Speech"
        
        if st.button("ℹ️ About", key="sidebar_about", use_container_width=True):
            st.session_state.current_page = "About"
        
        # Additional sidebar information
        st.markdown("---")
        st.markdown("""
        **Academic Paper Generator and Validator**  
        *Version 1.0.0*

        Powered by advanced AI technologies for efficient academic writing and research support.
       """)


        

def main():
    # Initialize session state for navigation if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Render the sidebar
    render_sidebar()
    
    # Render the appropriate page based on selection
    if st.session_state.current_page == "Home":
        render_home()
    elif st.session_state.current_page == "Draft Generator":
        render_draft_generator()
    elif st.session_state.current_page == "Writing Style":
        render_writing_style()
    elif st.session_state.current_page == "Language Support":
        render_language_support()
    elif st.session_state.current_page == "Publication Search":
        render_publication_search()
    elif st.session_state.current_page == "Research/Explore":
        render_research_explore()
    elif st.session_state.current_page == "Text-to-Speech":
        render_text_to_speech()
    elif st.session_state.current_page == "About":
        render_About()
    
    
if __name__ == "__main__":
    main()
