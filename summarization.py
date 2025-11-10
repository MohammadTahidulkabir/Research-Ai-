"""Dual-model summarization using Groq and OpenAI."""

from groq import Groq
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

from typing import Dict, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()


class PaperSummarizer:
    """Handles paper summarization using dual-model approach."""
    
    def __init__(self, config: dict):
        """Initialize summarizer with API clients."""
        self.config = config['research_agent']
        
        # Initialize Groq client (fast summarization)
        groq_config = self.config['apis']['groq']
        self.groq_client = Groq(api_key=groq_config['api_key'])
        self.groq_model = groq_config['model']
        
        # Initialize OpenAI client (deep analysis) - optional
        self.openai_client = None
        self.openai_model = None
        if OPENAI_AVAILABLE:
            try:
                openai_config = self.config['apis']['openai']
                if openai_config.get('api_key'):
                    self.openai_client = OpenAI(api_key=openai_config['api_key'])
                    self.openai_model = openai_config['model']
            except Exception as e:
                console.print(f"[yellow]OpenAI not configured: {str(e)}[/yellow]")
        
        # Model settings
        self.summarizer_config = self.config['models']['summarizer']
        self.analyzer_config = self.config['models']['analyzer']
    
    def summarize_papers_fast(self, papers: List[Dict]) -> List[Dict]:
        """
        Quick summarization using Groq model.
        
        Args:
            papers: List of paper dictionaries
        
        Returns:
            Papers with added 'fast_summary' field
        """
        console.print("\n[cyan]📝 Generating fast summaries (Groq)...[/cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Summarizing papers...", total=len(papers))
            
            for paper in papers:
                try:
                    summary = self._summarize_single_fast(paper)
                    paper['fast_summary'] = summary
                    progress.advance(task)
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to summarize {paper['id']}: {str(e)}[/yellow]")
                    paper['fast_summary'] = "Summary unavailable"
                    progress.advance(task)
        
        console.print("[green]✓ Fast summaries complete[/green]")
        return papers
    
    def _summarize_single_fast(self, paper: Dict) -> str:
        """Generate fast summary for a single paper using Groq."""
        prompt = f"""Summarize this research paper in 2-3 clear, technical sentences.

Title: {paper['title']}
Abstract: {paper['summary']}

Focus on:
1. Main contribution or novelty
2. Methods or techniques used
3. Key results or findings

Be specific and technical. Avoid generic statements."""

        response = self.groq_client.chat.completions.create(
            model=self.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.summarizer_config['temperature'],
            max_tokens=self.summarizer_config['max_tokens']
        )
        
        return response.choices[0].message.content.strip()
    
    def analyze_papers_deep(self, papers: List[Dict], context_papers: List[Dict] = None) -> List[Dict]:
        """
        Deep analysis using OpenAI GPT-4o or Groq Llama.
        
        Args:
            papers: List of papers to analyze
            context_papers: Additional papers for context
        
        Returns:
            Papers with added 'deep_analysis' field
        """
        use_groq = not self.openai_client
        if use_groq:
            console.print("\n[cyan]🧠 Performing deep analysis (Groq Llama)...[/cyan]")
        else:
            console.print("\n[cyan]🧠 Performing deep analysis (GPT-4o)...[/cyan]")
        
        # Prepare context
        if context_papers is None:
            context_papers = papers
        
        context_text = self._prepare_context(context_papers)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing papers...", total=len(papers))
            
            for paper in papers:
                try:
                    analysis = self._analyze_single_deep(paper, context_text)
                    paper['deep_analysis'] = analysis
                    progress.advance(task)
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to analyze {paper['id']}: {str(e)}[/yellow]")
                    paper['deep_analysis'] = {
                        'contributions': [],
                        'methods': [],
                        'results': [],
                        'limitations': [],
                        'relations': [],
                        'applications': []
                    }
                    progress.advance(task)
        
        console.print("[green]✓ Deep analysis complete[/green]")
        return papers
    
    def _prepare_context(self, papers: List[Dict]) -> str:
        """Prepare context from related papers."""
        context_lines = []
        for i, paper in enumerate(papers[:5], 1):  # Use top 5 for context
            context_lines.append(f"{i}. {paper['title']} ({paper['published'].year})")
        return "\n".join(context_lines)
    
    def _analyze_single_deep(self, paper: Dict, context: str) -> Dict:
        """Perform deep analysis on a single paper using GPT-4o or Groq."""
        prompt = f"""Analyze this research paper in detail:

Title: {paper['title']}
Authors: {', '.join(paper['authors'][:5])}
Published: {paper['published'].strftime('%Y-%m-%d')}
Abstract: {paper['summary']}

Related recent papers:
{context}

Provide a structured analysis:

1. NOVEL CONTRIBUTIONS (what's genuinely new?)
2. METHODS AND TECHNIQUES (specific algorithms, architectures, approaches)
3. KEY RESULTS (metrics, performance, findings)
4. LIMITATIONS (explicitly stated or implied)
5. RELATIONS (how it builds on or differs from related work)
6. POTENTIAL APPLICATIONS (practical use cases)

Be specific, technical, and objective. Format as JSON with keys: contributions, methods, results, limitations, relations, applications (each as array of strings)."""

        if self.openai_client:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.analyzer_config['temperature'],
                max_tokens=self.analyzer_config['max_tokens'],
                response_format={"type": "json_object"}
            )
        else:
            # Use Groq instead
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.analyzer_config['temperature'],
                max_tokens=self.analyzer_config['max_tokens']
            )
        
        import json
        try:
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except:
            # Fallback if JSON parsing fails
            return {
                'contributions': [response.choices[0].message.content],
                'methods': [],
                'results': [],
                'limitations': [],
                'relations': [],
                'applications': []
            }
    
    def extract_key_insights(self, papers: List[Dict]) -> Dict:
        """Extract key insights across all papers using GPT-4o or Groq."""
        use_groq = not self.openai_client
        if use_groq:
            console.print("\n[cyan]💡 Extracting cross-paper insights (Groq)...[/cyan]")
        else:
            console.print("\n[cyan]💡 Extracting cross-paper insights (GPT-4o)...[/cyan]")
        
        # Prepare paper summaries
        summaries = []
        for i, paper in enumerate(papers, 1):
            summary = f"{i}. {paper['title']}\n"
            summary += f"   Summary: {paper.get('fast_summary', 'N/A')}\n"
            if 'deep_analysis' in paper:
                summary += f"   Methods: {', '.join(paper['deep_analysis'].get('methods', [])[:3])}\n"
            summaries.append(summary)
        
        summaries_text = "\n".join(summaries)
        
        prompt = f"""Analyze these {len(papers)} research papers and identify patterns:

{summaries_text}

Provide a comprehensive analysis:

1. COMMON METHODS: Which techniques/frameworks appear across multiple papers?
2. DATASETS USED: What datasets are commonly used? Any gaps?
3. EVALUATION METRICS: What metrics are used? Are they consistent?
4. RECURRING LIMITATIONS: What limitations appear across papers?
5. RESEARCH GAPS: What areas are underexplored?
6. EMERGING THEMES: What new directions are emerging?

Format as JSON with keys: common_methods, datasets_used, metrics, limitations, research_gaps, emerging_themes (each as array of objects with 'item' and 'details' fields)."""

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=2000,
                    response_format={"type": "json_object"}
                )
            else:
                response = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=2000
                )
            
            import json
            insights = json.loads(response.choices[0].message.content)
            console.print("[green]✓ Insights extracted[/green]")
            return insights
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to extract insights: {str(e)}[/yellow]")
            return {
                'common_methods': [],
                'datasets_used': [],
                'metrics': [],
                'limitations': [],
                'research_gaps': [],
                'emerging_themes': []
            }
    
    def generate_research_directions(self, papers: List[Dict], insights: Dict) -> List[Dict]:
        """Generate actionable research directions using GPT-4o or Groq."""
        use_groq = not self.openai_client
        if use_groq:
            console.print("\n[cyan]🚀 Generating research directions (Groq)...[/cyan]")
        else:
            console.print("\n[cyan]🚀 Generating research directions (GPT-4o)...[/cyan]")
        
        # Prepare context
        context = f"""Based on analysis of {len(papers)} recent papers:

Research Gaps Identified:
{self._format_items(insights.get('research_gaps', []))}

Emerging Themes:
{self._format_items(insights.get('emerging_themes', []))}

Common Limitations:
{self._format_items(insights.get('limitations', []))}"""

        prompt = f"""{context}

Generate 3-5 concrete research project ideas that address these gaps and limitations.

For each project, provide:
1. TITLE: Catchy, descriptive title
2. MOTIVATION: Why this matters (2-3 sentences)
3. APPROACH: How to tackle it (specific methods)
4. EXPECTED CONTRIBUTION: What's novel
5. REQUIRED RESOURCES: Compute, data, expertise needed
6. TIMELINE: Rough estimate (weeks/months)
7. DIFFICULTY: Low/Medium/High

Format as JSON array of project objects."""

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000,
                    response_format={"type": "json_object"}
                )
            else:
                response = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
            
            import json
            result = json.loads(response.choices[0].message.content)
            projects = result.get('projects', [])
            console.print(f"[green]✓ Generated {len(projects)} research directions[/green]")
            return projects
        
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to generate directions: {str(e)}[/yellow]")
            return []
    
    def _format_items(self, items: List) -> str:
        """Format items for prompt context."""
        if not items:
            return "None identified"
        
        formatted = []
        for item in items[:5]:  # Limit to top 5
            if isinstance(item, dict):
                formatted.append(f"- {item.get('item', 'N/A')}: {item.get('details', '')}")
            else:
                formatted.append(f"- {item}")
        
        return "\n".join(formatted)
