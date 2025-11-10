"""Utility functions for the research agent."""

import yaml
import os
from datetime import datetime, timedelta
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, skip


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Replace environment variables
    if 'research_agent' in config:
        apis = config['research_agent'].get('apis', {})
        if 'openai' in apis and 'api_key' in apis['openai']:
            if apis['openai']['api_key'].startswith('${') and apis['openai']['api_key'].endswith('}'):
                env_var = apis['openai']['api_key'][2:-1]
                apis['openai']['api_key'] = os.getenv(env_var, '')
    
    return config


def get_date_range(days_back: int) -> tuple:
    """Get start and end dates for paper search."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date


def format_authors(authors: list, max_authors: int = 3) -> str:
    """Format author list for display."""
    if len(authors) <= max_authors:
        return ", ".join(authors)
    else:
        return f"{', '.join(authors[:max_authors])} et al."


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def create_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_timestamp() -> str:
    """Get formatted timestamp for reports."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_query_command(query: str) -> tuple:
    """Parse special commands from query string."""
    query = query.strip()
    
    if query.startswith('/compare'):
        # Extract topics from "/compare topic1 vs topic2"
        parts = query[8:].strip().split(' vs ')
        if len(parts) == 2:
            return 'compare', parts
    
    elif query.startswith('/expand'):
        # Extract subtopic from "/expand subtopic"
        subtopic = query[7:].strip()
        return 'expand', subtopic
    
    elif query.startswith('/trend'):
        # Extract topic and years from "/trend topic over years"
        parts = query[6:].strip().split(' over ')
        if len(parts) == 2:
            return 'trend', (parts[0].strip(), parts[1].strip())
    
    elif query.startswith('/store'):
        # Extract name from "/store name"
        name = query[6:].strip()
        return 'store', name
    
    elif query.startswith('/load'):
        # Extract name from "/load name"
        name = query[5:].strip()
        return 'load', name
    
    elif query.startswith('/query'):
        # Extract question from "/query question"
        question = query[6:].strip()
        return 'query', question
    
    elif query.startswith('/update'):
        return 'update', None
    
    elif query.startswith('/export'):
        # Extract format from "/export format"
        format_type = query[7:].strip()
        return 'export', format_type
    
    return 'search', query


def extract_keywords(query: str) -> list:
    """Extract keywords from query string."""
    # Simple keyword extraction (can be enhanced with NLP)
    stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or'}
    words = query.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords


def estimate_reading_time(word_count: int) -> str:
    """Estimate reading time based on word count."""
    # Average reading speed: 200-250 words per minute
    minutes = word_count / 225
    if minutes < 1:
        return "< 1 min"
    elif minutes < 60:
        return f"{int(minutes)} min"
    else:
        hours = minutes / 60
        return f"{hours:.1f} hours"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def validate_arxiv_query(query: str) -> tuple:
    """Validate arXiv query syntax."""
    # Check for valid arXiv query operators
    valid_operators = ['au:', 'ti:', 'abs:', 'cat:', 'AND', 'OR', 'ANDNOT']
    
    # Basic validation
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty"
    
    # Check for balanced parentheses
    if query.count('(') != query.count(')'):
        return False, "Unbalanced parentheses in query"
    
    return True, "Valid query"


def get_arxiv_categories() -> Dict[str, str]:
    """Get common arXiv category codes and descriptions."""
    return {
        'cs.AI': 'Artificial Intelligence',
        'cs.LG': 'Machine Learning',
        'cs.CL': 'Computation and Language',
        'cs.CV': 'Computer Vision',
        'cs.NE': 'Neural and Evolutionary Computing',
        'cs.RO': 'Robotics',
        'stat.ML': 'Statistics - Machine Learning',
        'quant-ph': 'Quantum Physics',
        'physics.comp-ph': 'Computational Physics',
        'math.OC': 'Optimization and Control',
        'eess.SP': 'Signal Processing',
        'eess.IV': 'Image and Video Processing'
    }


def suggest_related_keywords(query: str) -> list:
    """Suggest related keywords based on query."""
    # Keyword mapping (can be enhanced with embeddings)
    keyword_map = {
        'transformer': ['attention', 'bert', 'gpt', 'self-attention', 'encoder-decoder'],
        'vision': ['image', 'cnn', 'visual', 'computer vision', 'object detection'],
        'nlp': ['language', 'text', 'linguistic', 'natural language', 'bert'],
        'quantum': ['qubit', 'quantum computing', 'quantum algorithm', 'entanglement'],
        'reinforcement': ['rl', 'policy', 'reward', 'agent', 'q-learning'],
        'gan': ['generative', 'adversarial', 'generator', 'discriminator'],
        'diffusion': ['denoising', 'score-based', 'ddpm', 'generative model']
    }
    
    query_lower = query.lower()
    suggestions = []
    
    for key, related in keyword_map.items():
        if key in query_lower:
            suggestions.extend(related)
    
    return list(set(suggestions))[:5]  # Return top 5 unique suggestions
