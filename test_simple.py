"""Simple test script without emojis for Windows compatibility."""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.utils import load_config
from src.retrieval import PaperRetriever
from src.summarization import PaperSummarizer

print("="*60)
print("AI Research Agent - Simple Test (Groq Only)")
print("="*60)

# Load config
print("\n[1/4] Loading configuration...")
config = load_config()
print("OK - Configuration loaded")

# Initialize retriever
print("\n[2/4] Initializing paper retriever...")
retriever = PaperRetriever(config)
print("OK - Retriever ready")

# Fetch papers
print("\n[3/4] Fetching 3 papers on 'vision transformers'...")
papers = retriever.fetch_papers(
    query="vision transformers",
    max_results=3,
    days_back=365
)
print(f"OK - Retrieved {len(papers)} papers")

# Display papers
print("\n" + "="*60)
print("RETRIEVED PAPERS:")
print("="*60)
for i, paper in enumerate(papers, 1):
    print(f"\n{i}. {paper['title']}")
    print(f"   Authors: {', '.join(paper['authors'][:3])}")
    print(f"   Published: {paper['published'].strftime('%Y-%m-%d')}")
    print(f"   arXiv: {paper['id']}")

# Summarize with Groq
print("\n[4/4] Generating summaries with Groq...")
summarizer = PaperSummarizer(config)
papers = summarizer.summarize_papers_fast(papers)
print("OK - Summaries generated")

# Display summaries
print("\n" + "="*60)
print("PAPER SUMMARIES:")
print("="*60)
for i, paper in enumerate(papers, 1):
    print(f"\n{i}. {paper['title']}")
    print(f"   Summary: {paper.get('fast_summary', 'N/A')}")

print("\n" + "="*60)
print("TEST COMPLETE!")
print("="*60)
print("\nThe Groq API is working correctly!")
print("Papers were retrieved from arXiv and summarized successfully.")
