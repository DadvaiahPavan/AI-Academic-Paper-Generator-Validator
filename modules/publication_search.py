import requests
from typing import List, Dict
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

class PublicationSearcher:
    """
    Handles searching for academic publications across various domains using different APIs.
    """
    
    def __init__(self):
        """Initialize the publication searcher with API endpoints"""
        # Base URLs for different academic APIs
        self.arxiv_api = "http://export.arxiv.org/api/query"
        self.core_api = "https://core.ac.uk/api/v3"
        
    def search_publications(self, query: str, domain: str, limit: int = 10) -> List[Dict]:
        """
        Search for publications based on query and domain across multiple sources.
        
        Args:
            query (str): Search query
            domain (str): Academic domain (e.g., "Computer Science", "Medicine")
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of publications with their details
        """
        try:
            # Preprocess query and domain for better search
            processed_query = self._preprocess_query(query, domain)
            
            # Search all sources
            arxiv_results = self._search_arxiv(processed_query, domain, limit)
            google_results = self._search_google_scholar(processed_query, limit)
            pubmed_results = self._search_pubmed(processed_query, limit)
            
            # Combine and format results
            all_results = arxiv_results + google_results + pubmed_results
            publications = self._filter_and_rank_results(all_results, query, domain)
            
            return publications[:limit]
            
        except Exception as e:
            print(f"Error searching publications: {e}")
            return []
    
    def _preprocess_query(self, query: str, domain: str) -> str:
        """Preprocess query for better search results"""
        # Convert to lowercase and remove extra spaces
        query = query.lower().strip()
        
        # Add domain-specific keywords if not present
        domain_keywords = {
            "Medicine": ["medical", "healthcare", "clinical", "patient"],
            "Computer Science": ["computing", "algorithm", "software", "system"],
            "Artificial Intelligence": ["ai", "machine learning", "deep learning", "neural"],
            "Machine Learning": ["ml", "deep learning", "neural network", "algorithm"],
            "Data Science": ["data", "analytics", "mining", "statistical"],
            "Robotics": ["robot", "automation", "control", "mechanical"],
            "Natural Language Processing": ["nlp", "language", "text", "linguistic"]
        }
        
        # Add domain-specific keywords if they're relevant but not present
        if domain in domain_keywords:
            keywords = domain_keywords[domain]
            query_terms = query.split()
            for keyword in keywords:
                if any(self._calculate_similarity(keyword, term) > 0.8 for term in query_terms):
                    continue
                if not any(keyword in term for term in query_terms):
                    if domain.lower() not in query.lower():
                        query = f"{query} {domain.lower()}"
                    break
        
        # Handle specific cases
        if "ai" in query.split() or "ml" in query.split():
            query = query.replace("ai", "artificial intelligence")
            query = query.replace("ml", "machine learning")
        
        return query
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity using Levenshtein distance"""
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        distance = self._levenshtein_distance(str1, str2)
        max_length = max(len(str1), len(str2))
        return 1 - (distance / max_length)
    
    def _levenshtein_distance(self, str1: str, str2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(str1) < len(str2):
            return self._levenshtein_distance(str2, str1)
        
        if len(str2) == 0:
            return len(str1)
        
        previous_row = range(len(str2) + 1)
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _filter_and_rank_results(self, results: List[Dict], original_query: str, domain: str) -> List[Dict]:
        """Filter and rank results based on relevance"""
        scored_results = []
        query_terms = set(original_query.lower().split())
        domain_terms = set(domain.lower().split())
        
        for result in results:
            score = 0
            title_lower = result['title'].lower()
            abstract_lower = result.get('summary', '').lower()
            
            # Score based on title match
            for term in query_terms:
                if term in title_lower:
                    score += 5  # Higher weight for title matches
                if term in abstract_lower:
                    score += 2  # Lower weight for abstract matches
            
            # Score based on domain relevance
            for term in domain_terms:
                if term in title_lower:
                    score += 3
                if term in abstract_lower:
                    score += 1
            
            # Score based on recency
            try:
                pub_date = datetime.strptime(result.get('published', '')[:10], '%Y-%m-%d')
                days_old = (datetime.now() - pub_date).days
                recency_score = max(0, 1 - (days_old / 365))  # Higher score for newer papers
                score += recency_score
            except:
                score += 0  # Default score if date parsing fails
            
            # Create publication object with score
            pub = {
                "title": result.get("title", ""),
                "authors": result.get("authors", []),
                "summary": result.get("summary", ""),
                "link": result.get("link", ""),
                "published": result.get("published", ""),
                "source": result.get("source", ""),
                "domain": domain,
                "score": score
            }
            
            # Only include if it's relevant enough
            if score > 0:
                scored_results.append((score, pub))
        
        # Sort by score
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return only the publication objects, without scores
        return [result for score, result in scored_results]

    def _search_arxiv(self, query: str, domain: str, limit: int) -> List[Dict]:
        """Search arXiv for publications with improved query handling"""
        try:
            # Map general domains to arXiv categories
            domain_mapping = {
                "Computer Science": ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.NE"],
                "Physics": ["physics"],
                "Mathematics": ["math"],
                "Biology": ["q-bio"],
                "Economics": ["econ"],
                "Statistics": ["stat"],
                "Electrical Engineering": ["eess"],
                "Medicine": ["q-bio.QM", "stat.ML", "cs.AI"],  # Include relevant AI categories for medical papers
                "Machine Learning": ["cs.LG", "stat.ML"],
                "Artificial Intelligence": ["cs.AI", "cs.LG", "cs.CL", "cs.CV"],
                "Data Science": ["cs.DB", "stat.ML", "cs.LG"],
                "Robotics": ["cs.RO", "cs.AI"],
                "Natural Language Processing": ["cs.CL", "cs.AI"]
            }
            
            # Get arXiv categories
            arxiv_categories = domain_mapping.get(domain, ["all"])
            
            # Build advanced search query
            search_query = f'all:({query})'
            if arxiv_categories != ["all"]:
                category_query = " OR ".join(f"cat:{cat}" for cat in arxiv_categories)
                search_query = f"{search_query} AND ({category_query})"
            
            params = {
                "search_query": search_query,
                "start": 0,
                "max_results": limit,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            
            response = requests.get(self.arxiv_api, params=params)
            
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                
                results = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    result = {
                        "title": entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                        "authors": [author.find('{http://www.w3.org/2005/Atom}name').text 
                                  for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                        "summary": entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                        "link": entry.find('{http://www.w3.org/2005/Atom}id').text.strip(),
                        "published": entry.find('{http://www.w3.org/2005/Atom}published').text.strip(),
                        "source": "arXiv"
                    }
                    results.append(result)
                
                return results
            
            return []
            
        except Exception as e:
            print(f"Error searching arXiv: {e}")
            return []

    def _search_google_scholar(self, query: str, limit: int) -> List[Dict]:
        """Search Google Scholar for publications"""
        url = f"https://scholar.google.com/scholar?q={query}&hl=en&as_sdt=0%2C5"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='gs_r gs_or gs_scl'):
            title = result.find('h3', class_='gs_rt')
            link = title.find('a')['href'] if title else None
            title_text = title.text.strip() if title else "No title"
            authors = result.find('div', class_='gs_a').text.strip() if result.find('div', class_='gs_a') else "No authors"
            published = result.find('span', class_='gs_age').text.strip() if result.find('span', class_='gs_age') else "No date"
            result_dict = {
                "title": title_text,
                "authors": [authors],
                "summary": "",
                "link": link,
                "published": published,
                "source": "Google Scholar"
            }
            results.append(result_dict)
        return results[:limit]

    def _search_pubmed(self, query: str, limit: int) -> List[Dict]:
        """Search PubMed for publications"""
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}&size=200"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='full-text-links'):
            title = result.find('a', class_='article-title')
            link = title['href'] if title else None
            title_text = title.text.strip() if title else "No title"
            authors = result.find('span', class_='authors-list-item').text.strip() if result.find('span', class_='authors-list-item') else "No authors"
            published = result.find('span', class_='citation-part').text.strip() if result.find('span', class_='citation-part') else "No date"
            result_dict = {
                "title": title_text,
                "authors": [authors],
                "summary": "",
                "link": link,
                "published": published,
                "source": "PubMed"
            }
            results.append(result_dict)
        return results[:limit]

    def get_domain_suggestions(self) -> List[str]:
        """Get list of available academic domains"""
        return [
            "Computer Science",
            "Physics",
            "Mathematics",
            "Biology",
            "Economics",
            "Statistics",
            "Electrical Engineering",
            "Medicine",
            "Machine Learning",
            "Artificial Intelligence",
            "Data Science",
            "Robotics",
            "Natural Language Processing"
        ]
