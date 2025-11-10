# 🚀 Quick Start Guide

Get started with the AI Research Agent in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (for deep analysis)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** The Groq API key is already configured in `config.yaml`.

## Basic Usage

### Simple Search

```bash
python research_agent.py "vision transformers"
```

This will:
1. Fetch recent papers from arXiv
2. Generate fast summaries (Groq)
3. Perform deep analysis (GPT-4o)
4. Identify research gaps
5. Generate research directions
6. Save a comprehensive markdown report

### Custom Parameters

```bash
# Get 20 papers from the last year
python research_agent.py "quantum machine learning" --max-papers 20 --days-back 365

# Skip deep analysis (faster, uses only Groq)
python research_agent.py "neural networks" --no-deep-analysis
```

### Interactive Mode

```bash
python research_agent.py --interactive
```

Then use commands:
- Regular search: `vision transformers`
- Compare topics: `/compare GANs vs Diffusion Models`
- Store session: `/store my_session_name`
- Load session: `/load my_session_name`
- Query session: `/query What datasets were used?`
- List sessions: `/list`
- Exit: `/exit`

### Compare Topics

```bash
python research_agent.py --compare "GANs" "Diffusion Models"
```

## Output

All reports are saved to the `./reports/` directory by default.

### Report Contents

- 📚 **Summary of Recent Works** - Individual paper summaries
- 🧠 **Cross-Paper Analysis** - Common methods, datasets, metrics
- 🚨 **Limitations & Gaps** - Identified research gaps
- 🚀 **Research Directions** - Actionable project ideas
- 📊 **Trend Analysis** - Temporal and category trends
- 📚 **Complete References** - BibTeX-ready citations

## Advanced Features

### Store Research Sessions

```python
from src import load_config, PaperRetriever, VectorStoreManager

config = load_config()
retriever = PaperRetriever(config)
vector_store = VectorStoreManager(config)

# Fetch papers
papers = retriever.fetch_papers("transformers", max_results=10)

# Store session
vector_store.store_research_session(
    session_name="transformer_survey",
    papers=papers,
    insights={},
    research_directions=[],
    query="transformers"
)
```

### Query Stored Sessions (RAG)

```python
# Query with semantic search
results = vector_store.query_session(
    session_name="transformer_survey",
    query="What are the main attention mechanisms?",
    k=5
)

for result in results:
    print(result['content'])
```

### Export Formats

```python
from src import ReportGenerator

report_gen = ReportGenerator(config)

# BibTeX
bibtex = report_gen.generate_bibtex(papers)
report_gen.save_report(bibtex, "references", "bibtex")

# JSON
json_data = report_gen.generate_json(papers, insights, directions)
report_gen.save_report(json_data, "data", "json")
```

## Configuration

Edit `config.yaml` to customize:

```yaml
research_agent:
  defaults:
    max_papers: 15        # Default number of papers
    days_back: 730        # Look back 2 years
    categories:           # arXiv categories to search
      - cs.AI
      - cs.LG
      - cs.CL
  
  models:
    summarizer:
      temperature: 0.3    # Lower = more focused
      max_tokens: 500
    
    analyzer:
      temperature: 0.5
      max_tokens: 2000
```

## Common Use Cases

### 1. Literature Review

```bash
python research_agent.py "neural machine translation" --max-papers 30
```

### 2. Stay Updated

```bash
# Papers from last month
python research_agent.py "large language models" --days-back 30
```

### 3. Compare Approaches

```bash
python research_agent.py --compare "supervised learning" "self-supervised learning"
```

### 4. Find Research Gaps

The agent automatically identifies:
- Underexplored method combinations
- Missing datasets or benchmarks
- Temporal gaps (areas with limited recent work)
- Application gaps (theory without implementation)

### 5. Generate Project Ideas

Each report includes 3-5 concrete research project proposals with:
- Motivation
- Approach
- Expected contribution
- Required resources
- Timeline estimate

## Troubleshooting

### No papers found

- Try broader search terms
- Increase `--days-back`
- Check arXiv category codes in `config.yaml`

### API errors

- Verify OpenAI API key in `.env`
- Check API rate limits
- Groq API key is pre-configured

### Slow performance

- Use `--no-deep-analysis` to skip GPT-4o (faster)
- Reduce `--max-papers`
- Deep analysis uses GPT-4o which is slower but more insightful

## Examples

See `examples/example_usage.py` for programmatic usage:

```bash
python examples/example_usage.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [examples/](examples/) for code samples
- Check [config.yaml](config.yaml) for all configuration options
- Review generated reports in `./reports/`

## Support

For issues or questions:
1. Check configuration in `config.yaml`
2. Verify API keys in `.env`
3. Review error messages in console output

Happy researching! 🔬
