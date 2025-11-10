# 🚀 Getting Started Checklist

Follow these steps to get your AI Research Agent up and running!

## ✅ Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] OpenAI API key (optional, but recommended)
- [ ] Internet connection for arXiv access

## 📦 Installation Steps

### Step 1: Install Dependencies

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Or manually:**
```bash
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully

---

### Step 2: Configure API Keys

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Note:** 
- Groq API key is already configured in `config.yaml`
- OpenAI key is optional but enables deep analysis features

---

### Step 3: Test Installation

Run the system test:
```bash
python test_agent.py
```

**Expected results:**
- ✓ All packages installed
- ✓ Configuration valid
- ✓ Directories ready
- ✓ arXiv retrieval working
- ✓ Groq API working
- ✓ or ⚠ OpenAI API (optional)

**If tests fail:**
- Check error messages
- Verify API keys
- Ensure all dependencies installed
- See [Troubleshooting](#troubleshooting)

---

## 🎯 First Research Query

### Quick Test (5 minutes)

Run your first query:
```bash
python research_agent.py "vision transformers" --max-papers 5 --no-deep-analysis
```

**What happens:**
1. Fetches 5 recent papers from arXiv
2. Generates fast summaries using Groq
3. Creates a markdown report
4. Saves to `./reports/`

**Expected time:** ~30 seconds

---

### Full Analysis (10 minutes)

Try with deep analysis:
```bash
python research_agent.py "vision transformers" --max-papers 5
```

**What happens:**
1. Fetches 5 papers
2. Fast summaries (Groq)
3. Deep analysis (GPT-4o)
4. Cross-paper insights
5. Research directions
6. Comprehensive report

**Expected time:** ~2-3 minutes

**Note:** Requires OpenAI API key

---

## 📚 Learn the Basics

### 1. View Your Report

Check the `./reports/` directory for your generated report.

**Report includes:**
- Paper summaries
- Key contributions
- Research gaps
- Suggested projects
- Complete references

---

### 2. Try Different Queries

```bash
# Machine Learning
python research_agent.py "neural architecture search"

# Natural Language Processing
python research_agent.py "large language models"

# Computer Vision
python research_agent.py "object detection"

# Quantum Computing
python research_agent.py "quantum machine learning"
```

---

### 3. Adjust Parameters

```bash
# More papers
python research_agent.py "transformers" --max-papers 20

# Recent papers only (last 3 months)
python research_agent.py "transformers" --days-back 90

# Fast mode (no deep analysis)
python research_agent.py "transformers" --no-deep-analysis
```

---

### 4. Compare Topics

```bash
python research_agent.py --compare "GANs" "Diffusion Models"
```

**Output:** Side-by-side comparison report

---

### 5. Interactive Mode

```bash
python research_agent.py --interactive
```

**Try these commands:**
```
> vision transformers
> /store vit_survey
> /list
> /load vit_survey
> /query What datasets are used?
> /exit
```

---

## 🎓 Next Steps

### Explore Advanced Features

1. **Vector Storage**
   - Store research sessions
   - Semantic search
   - See: `examples/example_usage.py`

2. **Custom Analysis**
   - Programmatic API
   - Custom workflows
   - See: `USAGE_GUIDE.md`

3. **Export Formats**
   - BibTeX for citations
   - JSON for data
   - See: Report Generator docs

---

### Read Documentation

- **README.md** - Project overview
- **QUICKSTART.md** - Quick reference
- **USAGE_GUIDE.md** - Comprehensive guide
- **PROJECT_SUMMARY.md** - Technical details

---

## 🔧 Configuration

### Customize Settings

Edit `config.yaml` to adjust:

```yaml
defaults:
  max_papers: 15        # Change default paper count
  days_back: 730        # Change default time range
  categories:           # Change arXiv categories
    - cs.AI
    - cs.LG
```

### Model Settings

```yaml
models:
  summarizer:
    temperature: 0.3    # Adjust creativity (0.0-1.0)
    max_tokens: 500     # Adjust summary length
```

---

## 💡 Tips for Success

### 1. Start Small
- Use `--max-papers 5` for testing
- Use `--no-deep-analysis` for speed
- Gradually increase complexity

### 2. Effective Queries
- **Good:** "vision transformers", "quantum ML"
- **Too broad:** "AI", "machine learning"
- **Too specific:** "ViT-B/16 patch size 14"

### 3. Use Fast Mode First
```bash
# Quick exploration
python research_agent.py "topic" --no-deep-analysis

# Then deep dive
python research_agent.py "topic"
```

### 4. Save Important Sessions
```bash
python research_agent.py --interactive
> your query
> /store session_name
```

### 5. Regular Updates
```bash
# Check monthly for new papers
python research_agent.py "your topic" --days-back 30
```

---

## ⚠️ Troubleshooting

### Common Issues

#### "No module named 'rich'"
**Solution:**
```bash
pip install -r requirements.txt
```

#### "No papers found"
**Solutions:**
- Try broader search terms
- Increase `--days-back`
- Check arXiv is accessible

#### "Groq API error"
**Solutions:**
- Verify API key in `config.yaml`
- Wait 1 minute (rate limit)
- Try again

#### "OpenAI API error"
**Solutions:**
- Check `.env` has correct key
- Verify API key is active
- Use `--no-deep-analysis` as fallback

#### Slow performance
**Solutions:**
- Use `--no-deep-analysis`
- Reduce `--max-papers`
- Expected: 2-5 min for full analysis

---

## 📞 Getting Help

### 1. Run Diagnostics
```bash
python test_agent.py
```

### 2. Check Configuration
- Verify `config.yaml` settings
- Check `.env` has OpenAI key
- Ensure directories exist

### 3. Review Error Messages
- Read console output carefully
- Check API error messages
- Verify network connection

### 4. Consult Documentation
- See `USAGE_GUIDE.md` for details
- Check `PROJECT_SUMMARY.md` for technical info
- Review examples in `examples/`

---

## ✨ You're Ready!

Congratulations! You've successfully set up the AI Research Agent.

### Quick Command Reference

```bash
# Basic search
python research_agent.py "your topic"

# Fast mode
python research_agent.py "topic" --no-deep-analysis

# More papers
python research_agent.py "topic" --max-papers 20

# Recent only
python research_agent.py "topic" --days-back 90

# Compare topics
python research_agent.py --compare "topic1" "topic2"

# Interactive
python research_agent.py --interactive

# Help
python research_agent.py --help
```

---

## 🎯 Suggested First Projects

### 1. Literature Review
```bash
python research_agent.py "your research area" --max-papers 30
```

### 2. Stay Updated
```bash
python research_agent.py "your field" --days-back 30
```

### 3. Compare Approaches
```bash
python research_agent.py --compare "method A" "method B"
```

### 4. Find Research Gaps
```bash
python research_agent.py "emerging topic" --max-papers 20
```

---

## 📈 Track Your Progress

- [ ] Installation complete
- [ ] Test passed
- [ ] First query successful
- [ ] Report generated
- [ ] Tried different parameters
- [ ] Used interactive mode
- [ ] Stored a session
- [ ] Compared topics
- [ ] Read documentation
- [ ] Customized configuration

---

**Happy Researching! 🔬**

For more help, see:
- `README.md` - Overview
- `QUICKSTART.md` - Quick reference  
- `USAGE_GUIDE.md` - Detailed guide
- `PROJECT_SUMMARY.md` - Technical details
