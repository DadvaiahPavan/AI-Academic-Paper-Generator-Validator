import nltk
import language_tool_python
import textstat
from typing import Dict, List, Tuple, Any
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Download NLTK resources at module level (runs only once when imported)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    logging.warning(f"Failed to download NLTK resources: {e}")

class AcademicWritingStyleAnalyzer:
    """
    Analyzes academic writing style and provides suggestions for improvement.
    """
    
    def __init__(self):
        """Initialize the analyzer with necessary tools and resources."""
        # Initialize language tool
        try:
            self.language_tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            logging.warning(f"Failed to initialize language tool: {e}")
            self.language_tool = None
        
        # Common academic word replacements
        self.academic_synonyms = {
            "show": ["demonstrate", "indicate", "reveal", "establish"],
            "important": ["significant", "crucial", "essential", "fundamental"],
            "big": ["substantial", "considerable", "extensive", "significant"],
            "small": ["minimal", "limited", "marginal", "negligible"],
            "use": ["utilize", "employ", "implement", "apply"],
            "find": ["observe", "determine", "identify", "ascertain"],
            "think": ["hypothesize", "theorize", "postulate", "conjecture"],
            "look at": ["examine", "investigate", "analyze", "evaluate"]
        }

    def _get_academic_synonyms(self, word: str) -> List[str]:
        """
        Get academic synonyms for a given word.
        
        Args:
            word (str): Input word to find synonyms for
            
        Returns:
            List[str]: List of academic synonyms
        """
        # Check direct matches in academic synonyms dictionary
        word = word.lower()
        if word in self.academic_synonyms:
            return self.academic_synonyms[word]
        
        # Get additional synonyms from WordNet
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word and "_" not in lemma.name():
                    synonyms.add(lemma.name())
        
        return list(synonyms)[:5]  # Return top 5 synonyms

    def analyze_readability(self, text: str) -> Dict[str, float]:
        """
        Analyze text readability using various metrics.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict[str, float]: Dictionary containing readability scores
        """
        try:
            return {
                "flesch_reading_ease": textstat.flesch_reading_ease(text),
                "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
                "gunning_fog": textstat.gunning_fog(text),
                "smog_index": textstat.smog_index(text),
                "automated_readability_index": textstat.automated_readability_index(text),
                "coleman_liau_index": textstat.coleman_liau_index(text)
            }
        except Exception as e:
            raise Exception(f"Error analyzing readability: {e}")

    def check_grammar(self, text: str) -> List[Dict[str, Any]]:
        """
        Check the grammar of the provided text and return a list of issues found.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            List[Dict]: List of grammar issues with their suggestions
        """
        if not self.language_tool:
            return []
            
        try:
            matches = self.language_tool.check(text)
            issues = []
            
            for match in matches:
                issue = {
                    'message': match.message,
                    'context': match.context,
                    'offset': match.offset,
                    'length': match.errorLength,
                    'category': match.category,
                    'incorrect': text[match.offset:match.offset + match.errorLength],
                    'suggestions': match.replacements[:3] if match.replacements else []
                }
                issues.append(issue)
                
            return issues
            
        except Exception as e:
            logging.error(f"Error checking grammar: {e}")
            return []

    def detect_passive_voice(self, text: str) -> List[str]:
        """
        Detect sentences using passive voice.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            List[str]: Sentences containing passive voice.
        """
        passive_sentences = []
        sentences = sent_tokenize(text)
        for sentence in sentences:
            # Simple regex pattern for passive voice detection
            if re.search(r'\b(is|are|was|were|be|being|been)\s+\w+ed\b', sentence):
                passive_sentences.append(sentence)
        return passive_sentences

    def analyze_sentence_complexity(self, text: str) -> Dict[str, float]:
        """
        Analyze sentence complexity based on length and structure.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            Dict[str, float]: Average sentence length and complexity score.
        """
        sentences = sent_tokenize(text)
        total_length = sum(len(word_tokenize(sentence)) for sentence in sentences)
        average_length = total_length / len(sentences) if sentences else 0
        complexity_score = textstat.flesch_kincaid_grade(text)
        return {
            'average_length': average_length,
            'complexity_score': complexity_score
        }

    def suggest_conciseness(self, text: str) -> List[str]:
        """
        Suggest improvements for wordiness in the text.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            List[str]: Suggestions for more concise phrasing.
        """
        suggestions = []
        wordy_phrases = {
            "due to the fact that": "because",
            "in the event that": "if",
            "in order to": "to",
            "at this point in time": "now"
        }
        for phrase, replacement in wordy_phrases.items():
            if phrase in text:
                suggestions.append(f'Replace "{phrase}" with "{replacement}"')
        return suggestions

    def load_custom_rules(self, rules_file: str) -> Dict[str, str]:
        """
        Load customizable grammar and style rules from a JSON file.
        
        Args:
            rules_file (str): Path to the JSON file containing rules.
        
        Returns:
            Dict[str, str]: Custom rules loaded from the file.
        """
        import json
        try:
            with open(rules_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            logging.warning(f'Error loading rules: {e}')
            return {}

    def suggest_academic_vocabulary(self, text: str) -> List[Dict[str, Any]]:
        """
        Suggest academic alternatives for common words.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[Dict[str, Any]]: List of word suggestions
        """
        try:
            words = word_tokenize(text)
            suggestions = []
            
            for word in words:
                if word.lower() in self.academic_synonyms:
                    suggestions.append({
                        "word": word,
                        "suggestions": self.academic_synonyms[word.lower()]
                    })
            
            return suggestions
        except Exception as e:
            raise Exception(f"Error suggesting academic vocabulary: {e}")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze the provided text for grammar and style issues.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            Dict[str, Any]: Analysis results including grammar issues and style suggestions.
        """
        try:
            grammar_issues = self.check_grammar(text)
            passive_voice = self.detect_passive_voice(text)
            complexity = self.analyze_sentence_complexity(text)
            conciseness_suggestions = self.suggest_conciseness(text)
            readability = self.analyze_readability(text)
            vocabulary_suggestions = self.suggest_academic_vocabulary(text)
        
            results = {
                'grammar_issues': grammar_issues,
                'passive_voice': passive_voice,
                'complexity': complexity,
                'conciseness_suggestions': conciseness_suggestions,
                'readability': readability,
                'vocabulary_suggestions': vocabulary_suggestions
            }
            return results
        except Exception as e:
            logging.warning(f"An error occurred during analysis: {e}")
            return {'error': str(e)}


# Example usage
analyzer = AcademicWritingStyleAnalyzer()
text = "This is a simple text to analyze. It contains several sentences and aims to demonstrate the functionality of the Academic Writing Style Analyzer."
analysis_results = analyzer.analyze_text(text)
print(analysis_results)
