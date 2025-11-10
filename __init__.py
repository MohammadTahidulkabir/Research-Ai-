"""AI Research Agent - Academic paper retrieval and analysis system."""

from .retrieval import PaperRetriever
from .summarization import PaperSummarizer
from .analysis import ResearchAnalyzer
from .report_generator import ReportGenerator
from .vector_store import VectorStoreManager
from .utils import load_config

__version__ = "2.0.0"
__all__ = [
    "PaperRetriever",
    "PaperSummarizer",
    "ResearchAnalyzer",
    "ReportGenerator",
    "VectorStoreManager",
    "load_config"
]
