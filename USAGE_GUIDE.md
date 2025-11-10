# 📖 Complete Usage Guide

Comprehensive guide to using the AI Research Agent.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Command Reference](#command-reference)
6. [API Integration](#api-integration)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- OpenAI API key (optional, for deep analysis)

### Steps

```bash
# 1. Clone or download the repository
cd ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Test installation
python test_agent.py
```

---

## Configuration

### config.yaml Structure

```yaml
research_agent:
  # API Configuration
  apis:
    arxiv:
      page_size: 100          # Papers per request
      delay_seconds: 3.0      # Rate limiting
      num_retries: 3          # Retry failed requests
    
    groq:
      api_key: "your_key"     # Pre-configured
      model: "llama-3.3-70b-versatile"
    
    openai:
      api_key: "${OPENAI_API_KEY}"  # From .env
      model: "gpt-4o"
  
  # Model Settings
  models:
    summarizer:               # Fast summarization (Groq)
      temperature: 0.3        # Lower = more focused
      max_tokens: 500
    
    analyzer:                 # Deep analysis (OpenAI)
      temperature: 0.5
      max_tokens: 2000
  
  # Default Search Parameters
  defaults:
    max_papers: 15
    days_back: 730            # 2 years
    categories:
      - cs.AI                 # Artificial Intelligence
      - cs.LG                 # Machine Learning
      - cs.CL                 # NLP
      - cs.CV                 # Computer Vision
  
  # Storage Configuration
  storage:
    vector_db: "faiss"
    embedding_model: "text-embedding-3-small"
    persist_path: "./vector_stores"
  
  # Output Settings
  output:
    format: "markdown"
    include_charts: true
    save_path: "./reports"
```

### arXiv Category Codes

Common categories:
- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CL` - Computation and Language (NLP)
- `cs.CV` - Computer Vision
- `cs.NE` - Neural and Evolutionary Computing
- `cs.RO` - Robotics
- `stat.ML` - Statistics (Machine Learning)
- `quant-ph` - Quantum Physics

[Full list](https://arxiv.org/category_taxonomy)

---

## Basic Usage

### 1. Simple Search

```bash
python research_agent.py "vision transformers"
```

**What happens:**
1. Fetches 15 recent papers from arXiv
2. Generates fast summaries (Groq)
3. Performs deep analysis (GPT-4o)
4. Identifies research gaps
5. Generates research directions
6. Saves markdown report to `./reports/`

### 2. Custom Parameters

```bash
# More papers, shorter time range
python research_agent.py "quantum computing" --max-papers 30 --days-back 180

# Fast mode (no deep analysis)
python research_agent.py "neural networks" --no-deep-analysis
```

### 3. Interactive Mode

```bash
python research_agent.py --interactive
```

**Interactive Commands:**
- `vision transformers` - Regular search
- `/compare GANs vs Diffusion Models` - Compare topics
- `/store my_session` - Store current session
- `/load my_session` - Load saved session
- `/query What datasets were used?` - Query session
- `/list` - List all sessions
- `/exit` - Exit

### 4. Topic Comparison

```bash
python research_agent.py --compare "supervised learning" "self-supervised learning"
```

Generates side-by-side comparison of:
- Paper counts
- Temporal trends
- Methodologies
- Category distributions

---

## Advanced Features

### Vector Storage & RAG

Store research sessions for later semantic search:

```python
from src import load_config, PaperRetriever, VectorStoreManager

config = load_config()
retriever = PaperRetriever(config)
vector_store = VectorStoreManager(config)

# Fetch and store
papers = retriever.fetch_papers("transformers", max_results=15)
vector_store.store_research_session(
    session_name="transformer_survey_2024",
    papers=papers,
    insights={},
    research_directions=[],
    query="transformers"
)

# Query later
results = vector_store.query_session(
    session_name="transformer_survey_2024",
    query="What attention mechanisms are used?",
    k=5
)
```

### Custom Analysis Pipeline

```python
from src import (
    PaperRetriever,
    PaperSummarizer,
    ResearchAnalyzer,
    ReportGenerator,
    load_config
)

config = load_config()

# 1. Retrieve
retriever = PaperRetriever(config)
papers = retriever.fetch_papers("neural architecture search", max_results=20)

# 2. Summarize
summarizer = PaperSummarizer(config)
papers = summarizer.summarize_papers_fast(papers)
papers = summarizer.analyze_papers_deep(papers)

# 3. Analyze
analyzer = ResearchAnalyzer()
temporal = analyzer.analyze_temporal_trends(papers)
categories = analyzer.analyze_categories(papers)
common_terms = analyzer.extract_common_terms(papers)

# 4. Generate insights
insights = summarizer.extract_key_insights(papers)
directions = summarizer.generate_research_directions(papers, insights)

# 5. Create report
report_gen = ReportGenerator(config)
report = report_gen.generate_markdown_report(
    query="neural architecture search",
    papers=papers,
    insights=insights,
    research_directions=directions,
    analysis_data={'temporal': temporal, 'categories': categories}
)

# 6. Export
report_gen.save_report(report, "nas_survey", "markdown")
```

### Export Formats

```python
# BibTeX
bibtex = report_gen.generate_bibtex(papers)
report_gen.save_report(bibtex, "references", "bibtex")

# JSON
json_data = report_gen.generate_json(papers, insights, directions)
report_gen.save_report(json_data, "data", "json")

# Markdown (default)
report_gen.save_report(report, "report", "markdown")
```

---

## Command Reference

### CLI Arguments

```
python research_agent.py [OPTIONS] [QUERY]

Positional Arguments:
  QUERY                 Research query or topic

Optional Arguments:
  --max-papers N        Maximum papers to retrieve (default: 15)
  --days-back N         Days to look back (default: 730)
  --no-deep-analysis    Skip GPT-4o analysis (faster)
  --interactive, -i     Interactive mode
  --compare T1 T2       Compare two topics
  --config PATH         Config file path (default: config.yaml)
  --help, -h            Show help message
```

### Interactive Commands

| Command | Description | Example |
|---------|-------------|---------|
| `query` | Regular search | `vision transformers` |
| `/compare` | Compare topics | `/compare GANs vs Diffusion` |
| `/expand` | Expand subtopic | `/expand attention mechanisms` |
| `/trend` | Temporal analysis | `/trend NLP over 2020-2024` |
| `/store` | Save session | `/store my_session` |
| `/load` | Load session | `/load my_session` |
| `/query` | Query session | `/query What datasets?` |
| `/update` | Update session | `/update` |
| `/export` | Export format | `/export bibtex` |
| `/list` | List sessions | `/list` |
| `/exit` | Exit | `/exit` |

---

## API Integration

### Groq API

**Pre-configured** in `config.yaml`:
```yaml
groq:
  api_key: "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"
  model: "llama-3.3-70b-versatile"
```

Used for:
- Fast paper summarization
- Quick insights extraction

**Rate Limits:**
- Free tier: 30 requests/minute
- Handles automatically with delays

### OpenAI API

**Required for deep analysis**. Set in `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Used for:
- Deep paper analysis
- Cross-paper insights
- Research direction generation
- Semantic embeddings (vector storage)

**Rate Limits:**
- Depends on your tier
- Agent includes automatic rate limiting

**Cost Estimates:**
- Fast summary only (Groq): Free
- With deep analysis (GPT-4o): ~$0.01-0.05 per paper
- Vector embeddings: ~$0.0001 per paper

### arXiv API

**No API key required**. Public access.

**Rate Limits:**
- 3 seconds between requests (configured)
- Max 100 papers per request

**Query Syntax:**
```
ti:title_word          Search in title
abs:abstract_word      Search in abstract
au:author_name         Search by author
cat:category           Filter by category

Operators: AND, OR, ANDNOT
Example: ti:transformer AND cat:cs.LG
```

---

## Troubleshooting

### No Papers Found

**Symptoms:** "No papers found" message

**Solutions:**
1. Broaden search terms
2. Increase `--days-back`
3. Check category filters in `config.yaml`
4. Try alternative keywords

```bash
# Instead of:
python research_agent.py "very specific niche topic"

# Try:
python research_agent.py "broader topic" --days-back 1095
```

### API Errors

#### Groq API Error

**Symptoms:** "Groq API error" in output

**Solutions:**
1. Verify API key in `config.yaml`
2. Check rate limits (wait 1 minute)
3. Try again - may be temporary

#### OpenAI API Error

**Symptoms:** "OpenAI API error" or "deep analysis failed"

**Solutions:**
1. Check `.env` file has correct key
2. Verify API key is active
3. Check billing/credits
4. Use `--no-deep-analysis` flag as fallback

```bash
# Fallback to fast mode
python research_agent.py "your query" --no-deep-analysis
```

### Slow Performance

**Symptoms:** Takes very long to complete

**Causes & Solutions:**

1. **Deep analysis is slow**
   - GPT-4o is slower but more insightful
   - Use `--no-deep-analysis` for speed
   
2. **Too many papers**
   - Reduce `--max-papers`
   - Default is 15, try 5-10 for testing

3. **Rate limiting**
   - arXiv: 3 second delays (required)
   - Groq: 0.5 second delays
   - OpenAI: 1 second delays

```bash
# Fast mode
python research_agent.py "query" --max-papers 5 --no-deep-analysis
```

### Import Errors

**Symptoms:** `ModuleNotFoundError`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install arxiv groq openai langchain langchain-openai langchain-community faiss-cpu pyyaml rich pandas matplotlib
```

### Vector Store Errors

**Symptoms:** "Cannot store session" or "OpenAI embeddings not initialized"

**Cause:** Missing OpenAI API key

**Solution:**
1. Add `OPENAI_API_KEY` to `.env`
2. Vector storage requires OpenAI embeddings
3. Alternative: Use reports without vector storage

### Permission Errors

**Symptoms:** "Permission denied" when saving reports

**Solution:**
```bash
# Check directory permissions
mkdir -p reports vector_stores
chmod 755 reports vector_stores

# Or specify different path in config.yaml
```

---

## Best Practices

### 1. Start Small

```bash
# Test with small query first
python research_agent.py "transformers" --max-papers 5
```

### 2. Use Fast Mode for Exploration

```bash
# Quick overview
python research_agent.py "topic" --no-deep-analysis
```

### 3. Deep Analysis for Final Reports

```bash
# Comprehensive analysis
python research_agent.py "topic" --max-papers 20
```

### 4. Store Important Sessions

```python
# In interactive mode
> vision transformers
> /store vit_survey_2024
```

### 5. Regular Updates

```bash
# Check for new papers monthly
python research_agent.py "your topic" --days-back 30
```

---

## Examples

See `examples/example_usage.py` for:
- Basic search
- Full analysis pipeline
- Topic comparison
- Vector storage
- Export formats

Run examples:
```bash
python examples/example_usage.py
```

---

## Support

### Check System Status

```bash
python test_agent.py
```

### Common Issues

1. **No OpenAI key** → Use `--no-deep-analysis`
2. **Rate limited** → Wait 1 minute, try again
3. **No papers** → Broaden query, increase `--days-back`
4. **Slow** → Reduce `--max-papers`, use `--no-deep-analysis`

### Getting Help

1. Run `python test_agent.py` for diagnostics
2. Check configuration in `config.yaml`
3. Verify API keys in `.env`
4. Review error messages in console

---

## Tips & Tricks

### 1. Effective Queries

**Good:**
- "vision transformers"
- "quantum machine learning"
- "neural architecture search"

**Too Broad:**
- "AI"
- "machine learning"

**Too Specific:**
- "ViT-B/16 with patch size 14"

### 2. Category Filtering

Edit `config.yaml` to focus on specific areas:
```yaml
categories:
  - cs.CV  # Computer vision only
```

### 3. Time Ranges

- **Recent work:** `--days-back 90`
- **Comprehensive:** `--days-back 1095` (3 years)
- **Historical:** `--days-back 3650` (10 years)

### 4. Batch Processing

```bash
# Process multiple topics
for topic in "GANs" "VAEs" "Diffusion"; do
    python research_agent.py "$topic" --max-papers 10
done
```

### 5. Custom Workflows

Create your own scripts using the API:
```python
from src import load_config, PaperRetriever

config = load_config()
retriever = PaperRetriever(config)

topics = ["topic1", "topic2", "topic3"]
for topic in topics:
    papers = retriever.fetch_papers(topic, max_results=10)
    # Process papers...
```

---

Happy researching! 🔬
