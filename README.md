#  AI Research Agent v2.0

> **Autonomous academic research assistant powered by Groq + OpenAI**

An intelligent system that retrieves, analyzes, and synthesizes scientific literature from arXiv, generating comprehensive research reports with gap analysis and actionable project ideas.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

##  Key Features

###  Core Capabilities

| Feature | Description |
|---------|-------------|
|  **Automated Retrieval** | Fetch papers from arXiv with advanced query syntax |
|  **Dual-Model Analysis** | Fast summaries (Groq) + deep insights (GPT-4o) |
|  **Gap Detection** | Identify research gaps and emerging trends |
|  **Project Generation** | Get 3-5 concrete research project ideas |
|  **Vector Storage** | Save sessions with semantic search (RAG) |
|  **Rich Reports** | Publication-ready markdown with citations |
|  **Interactive Mode** | Advanced commands: compare, expand, query |
|  **Multiple Exports** | Markdown, BibTeX, JSON, LaTeX, PDF |

---

##  Quick Start

###  Installation (2 minutes)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh && ./install.sh
```

**Manual:**
```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

###  Test Setup

```bash
python test_agent.py
```

Expected: ✓ All tests pass (OpenAI optional)

###  First Query (30 seconds)

```bash
python research_agent.py "vision transformers" --max-papers 5 --no-deep-analysis
```

**Output:** Comprehensive report in `./reports/`

---

##  Usage Examples

### Basic Search
```bash
# Simple query
python research_agent.py "quantum machine learning"

# Custom parameters
python research_agent.py "neural architecture search" --max-papers 20 --days-back 365

# Fast mode (Groq only)
python research_agent.py "transformers" --no-deep-analysis
```

### Interactive Mode
```bash
python research_agent.py --interactive
```

**Available Commands:**
```
> vision transformers              # Regular search
> /compare GANs vs Diffusion       # Compare topics
> /store my_session                # Save session
> /load my_session                 # Load session
> /query What datasets are used?   # Semantic search
> /list                            # List sessions
> /exit                            # Exit
```

### Topic Comparison
```bash
python research_agent.py --compare "supervised learning" "self-supervised learning"
```

### Programmatic Usage
```python
from src import load_config, PaperRetriever, PaperSummarizer

config = load_config()
retriever = PaperRetriever(config)
summarizer = PaperSummarizer(config)

papers = retriever.fetch_papers("transformers", max_results=10)
papers = summarizer.summarize_papers_fast(papers)
```

---

##  What You Get

### Comprehensive Research Reports

Each report includes:

1. ** Paper Summaries**
   - Key contributions
   - Methods used
   - Results and metrics

2. ** Cross-Paper Analysis**
   - Common approaches
   - Popular datasets
   - Evaluation metrics

3. ** Limitations & Gaps**
   - Recurring limitations
   - Underexplored areas
   - Missing combinations

4. ** Research Directions**
   - 3-5 concrete project ideas
   - Motivation and approach
   - Resource requirements
   - Timeline estimates

5. ** Trend Analysis**
   - Publication timeline
   - Category distribution
   - Author networks

6. ** Complete References**
   - BibTeX-ready citations
   - arXiv links
   - Reproducibility notes

---

## 🛠️ Configuration

### API Keys

**Groq (Pre-configured):**
```yaml
# config.yaml
groq:
  api_key: "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"
```

**OpenAI (User-provided):**
```bash
# .env
OPENAI_API_KEY=sk-your-key-here
```

### Customize Settings

Edit `config.yaml`:
```yaml
defaults:
  max_papers: 15        # Papers per query
  days_back: 730        # Look back 2 years
  categories:           # arXiv categories
    - cs.AI
    - cs.LG
    - cs.CL
    - cs.CV
```

---

##  Project Structure

```
ai-agent/
├── 📄 config.yaml           # Configuration
├── 📄 requirements.txt      # Dependencies
├── 🐍 research_agent.py     # Main CLI
├── 🧪 test_agent.py         # System tests
├── 📦 src/
│   ├── retrieval.py         # arXiv API
│   ├── summarization.py     # Groq + OpenAI
│   ├── analysis.py          # Trend detection
│   ├── report_generator.py  # Report formatting
│   ├── vector_store.py      # RAG system
│   └── utils.py             # Utilities
├── 📂 reports/              # Generated reports
├── 📂 vector_stores/        # Saved sessions
├── 📂 examples/             # Example scripts
└── 📚 docs/
    ├── README.md            # This file
    ├── QUICKSTART.md        # Quick reference
    ├── USAGE_GUIDE.md       # Detailed guide
    ├── GETTING_STARTED.md   # Step-by-step
    └── PROJECT_SUMMARY.md   # Technical details
```

---

##  Cost & Performance

### Speed
- **Fast mode**: ~30 seconds for 10 papers
- **Full analysis**: ~2-5 minutes for 10 papers
- **Vector storage**: +10-20 seconds

### Cost (with OpenAI)
- **Groq only**: Free
- **Deep analysis**: ~$0.01-0.05 per paper
- **Typical 15-paper report**: ~$0.15-0.75

---

## 🎓 Documentation

| Document | Description |
|----------|-------------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Step-by-step setup checklist |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start guide |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | Comprehensive usage manual |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical architecture |

---

## 🔧 Troubleshooting

### Common Issues

**No papers found:**
```bash
# Try broader terms
python research_agent.py "machine learning" --days-back 1095
```

**API errors:**
```bash
# Use fast mode
python research_agent.py "topic" --no-deep-analysis
```

**Slow performance:**
```bash
# Reduce papers
python research_agent.py "topic" --max-papers 5
```

**Run diagnostics:**
```bash
python test_agent.py
```

---

##  Use Cases

- ** Literature Reviews** - Comprehensive topic overviews
- ** Research Planning** - Find gaps and generate ideas
- ** Stay Updated** - Track emerging trends monthly
- ** Comparative Analysis** - Evaluate different approaches
- ** Teaching** - Create reading lists and presentations

---

##  Contributing

Contributions welcome! See issues for planned features:
- [ ] PubMed integration
- [ ] Semantic Scholar support
- [ ] PDF parsing
- [ ] Citation network analysis
- [ ] Web interface

---

##  License

MIT License - See [LICENSE](LICENSE) file

---

##  Credits

- **arXiv API** - Cornell University
- **Groq** - Fast LLM inference
- **OpenAI** - GPT-4o and embeddings
- **LangChain** - RAG framework
- **FAISS** - Vector similarity search

---

##  Support

- 📖 Read the [documentation](USAGE_GUIDE.md)
- 🧪 Run `python test_agent.py`
- 💬 Check error messages in console
- 🔍 Review [troubleshooting guide](USAGE_GUIDE.md#troubleshooting)

---

##  Quick Command Reference

```bash
# Basic
python research_agent.py "your topic"

# Fast mode
python research_agent.py "topic" --no-deep-analysis

# More papers
python research_agent.py "topic" --max-papers 20

# Recent only
python research_agent.py "topic" --days-back 90

# Compare
python research_agent.py --compare "topic1" "topic2"

# Interactive
python research_agent.py --interactive

# Help
python research_agent.py --help
```

---

**Ready to start?** → See [GETTING_STARTED.md](GETTING_STARTED.md)

**Happy Researching! 🔬**
