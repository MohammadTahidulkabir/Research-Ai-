#!/usr/bin/env python3
"""
AI Research Agent - Main CLI Interface
Autonomous academic research assistant for paper retrieval and analysis.
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from src.utils import load_config, parse_query_command, format_timestamp
from src.retrieval import PaperRetriever
from src.summarization import PaperSummarizer
from src.analysis import ResearchAnalyzer
from src.report_generator import ReportGenerator
from src.vector_store import VectorStoreManager

console = Console()


class ResearchAgent:
    """Main research agent orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the research agent."""
        console.print("[cyan]Initializing AI Research Agent...[/cyan]")
        
        try:
            self.config = load_config(config_path)
            self.retriever = PaperRetriever(self.config)
            self.summarizer = PaperSummarizer(self.config)
            self.analyzer = ResearchAnalyzer()
            self.report_generator = ReportGenerator(self.config)
            self.vector_store = VectorStoreManager(self.config)
            
            console.print("[green]Agent initialized successfully[/green]\n")
        except Exception as e:
            console.print(f"[red]Error initializing agent: {str(e)}[/red]")
            sys.exit(1)
    
    def run_research_query(
        self,
        query: str,
        max_papers: int = None,
        days_back: int = None,
        deep_analysis: bool = True
    ) -> dict:
        """
        Execute a complete research query workflow.
        
        Args:
            query: Research query string
            max_papers: Maximum number of papers to retrieve
            days_back: Number of days to look back
            deep_analysis: Whether to perform deep analysis (GPT-4o)
        
        Returns:
            Dictionary containing all results
        """
        console.print(Panel.fit(
            f"[bold cyan]Research Query:[/bold cyan] {query}",
            border_style="cyan"
        ))
        
        # Phase 1: Retrieve papers
        console.print("\n[bold]Phase 1: Paper Retrieval[/bold]")
        papers = self.retriever.fetch_papers(
            query=query,
            max_results=max_papers,
            days_back=days_back
        )
        
        if not papers:
            console.print("[red]No papers found. Try adjusting your query.[/red]")
            suggestions = self.retriever.suggest_query_improvements(query, 0)
            if suggestions:
                console.print("\n[yellow]Suggestions:[/yellow]")
                for suggestion in suggestions:
                    console.print(f"  - {suggestion}")
            return {}
        
        # Phase 2: Fast summarization
        console.print("\n[bold]Phase 2: Fast Summarization[/bold]")
        papers = self.summarizer.summarize_papers_fast(papers)
        
        # Phase 3: Deep analysis (optional)
        if deep_analysis:
            console.print("\n[bold]Phase 3: Deep Analysis[/bold]")
            papers = self.summarizer.analyze_papers_deep(papers)
        
        # Phase 4: Extract insights
        console.print("\n[bold]Phase 4: Cross-Paper Analysis[/bold]")
        insights = self.summarizer.extract_key_insights(papers)
        
        # Phase 5: Generate research directions
        console.print("\n[bold]Phase 5: Research Directions[/bold]")
        research_directions = self.summarizer.generate_research_directions(papers, insights)
        
        # Phase 6: Additional analysis
        console.print("\n[bold]Phase 6: Trend Analysis[/bold]")
        temporal_analysis = self.analyzer.analyze_temporal_trends(papers)
        category_analysis = self.analyzer.analyze_categories(papers)
        
        analysis_data = {
            'temporal': temporal_analysis,
            'categories': category_analysis
        }
        
        # Generate report
        console.print("\n[bold]Phase 7: Report Generation[/bold]")
        report = self.report_generator.generate_markdown_report(
            query=query,
            papers=papers,
            insights=insights,
            research_directions=research_directions,
            analysis_data=analysis_data
        )
        
        # Save report
        timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
        filename = f"research_report_{timestamp}"
        filepath = self.report_generator.save_report(report, filename, 'markdown')
        
        console.print(f"\n[green]Report saved to: {filepath}[/green]")
        
        return {
            'query': query,
            'papers': papers,
            'insights': insights,
            'research_directions': research_directions,
            'analysis_data': analysis_data,
            'report': report,
            'report_path': filepath
        }
    
    def compare_topics(self, topic1: str, topic2: str, max_papers: int = 10) -> dict:
        """Compare two research topics."""
        console.print(Panel.fit(
            f"[bold cyan]Comparing:[/bold cyan] {topic1} vs {topic2}",
            border_style="cyan"
        ))
        
        # Retrieve papers for both topics
        console.print(f"\n[cyan]Fetching papers for: {topic1}[/cyan]")
        papers1 = self.retriever.fetch_papers(topic1, max_results=max_papers)
        
        console.print(f"\n[cyan]Fetching papers for: {topic2}[/cyan]")
        papers2 = self.retriever.fetch_papers(topic2, max_results=max_papers)
        
        # Analyze comparison
        comparison = self.analyzer.compare_topics(papers1, papers2, topic1, topic2)
        
        # Generate comparison report
        report = self.report_generator.generate_comparison_report(comparison)
        
        # Save report
        timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
        filename = f"comparison_{timestamp}"
        filepath = self.report_generator.save_report(report, filename, 'markdown')
        
        console.print(f"\n[green]Comparison report saved to: {filepath}[/green]")
        
        return {
            'comparison': comparison,
            'report': report,
            'report_path': filepath
        }
    
    def store_session(self, session_name: str, results: dict) -> bool:
        """Store research session to vector database."""
        return self.vector_store.store_research_session(
            session_name=session_name,
            papers=results['papers'],
            insights=results['insights'],
            research_directions=results['research_directions'],
            query=results['query']
        )
    
    def load_session(self, session_name: str) -> dict:
        """Load a stored research session."""
        return self.vector_store.load_research_session(session_name)
    
    def query_session(self, session_name: str, query: str) -> list:
        """Query a stored research session."""
        results = self.vector_store.query_session(session_name, query)
        
        if results:
            console.print(f"\n[bold]Query Results:[/bold]\n")
            for i, result in enumerate(results, 1):
                console.print(f"[cyan]{i}. Relevance: {result['relevance_score']:.3f}[/cyan]")
                console.print(f"Type: {result['metadata'].get('type', 'unknown')}")
                console.print(f"{result['content'][:300]}...\n")
        
        return results
    
    def list_sessions(self):
        """List all stored sessions."""
        sessions = self.vector_store.list_sessions()
        
        if not sessions:
            console.print("[yellow]No stored sessions found[/yellow]")
            return
        
        table = Table(title="Stored Research Sessions")
        table.add_column("Session Name", style="cyan")
        
        for session in sessions:
            table.add_row(session)
        
        console.print(table)
    
    def interactive_mode(self):
        """Run agent in interactive mode."""
        console.print(Panel.fit(
            "[bold cyan]🔬 AI Research Agent - Interactive Mode[/bold cyan]\n"
            "Commands: /compare, /expand, /store, /load, /query, /list, /exit",
            border_style="cyan"
        ))
        
        current_results = None
        
        while True:
            try:
                query = Prompt.ask("\n[bold cyan]Enter query[/bold cyan]")
                
                if not query:
                    continue
                
                # Parse command
                command_type, command_data = parse_query_command(query)
                
                if command_type == 'search':
                    # Regular search
                    current_results = self.run_research_query(command_data)
                
                elif command_type == 'compare':
                    # Compare two topics
                    topic1, topic2 = command_data
                    self.compare_topics(topic1, topic2)
                
                elif command_type == 'store':
                    # Store current session
                    if current_results:
                        session_name = command_data
                        self.store_session(session_name, current_results)
                    else:
                        console.print("[yellow]No active session to store[/yellow]")
                
                elif command_type == 'load':
                    # Load session
                    session_name = command_data
                    session_data = self.load_session(session_name)
                    if session_data:
                        summary = self.vector_store.export_session_summary(session_name)
                        console.print(f"\n{summary}")
                
                elif command_type == 'query':
                    # Query stored session
                    if current_results:
                        # Ask for session name
                        session_name = Prompt.ask("Session name")
                        self.query_session(session_name, command_data)
                    else:
                        console.print("[yellow]Specify session name first[/yellow]")
                
                elif command_type == 'list':
                    # List sessions
                    self.list_sessions()
                
                elif query.lower() in ['/exit', '/quit', 'exit', 'quit']:
                    console.print("[cyan]Goodbye![/cyan]")
                    break
                
                else:
                    console.print("[yellow]Unknown command. Try /help for available commands.[/yellow]")
            
            except KeyboardInterrupt:
                console.print("\n[cyan]Goodbye![/cyan]")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Research Agent - Academic paper retrieval and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python research_agent.py "vision transformers"
  python research_agent.py "quantum machine learning" --max-papers 20
  python research_agent.py --interactive
  python research_agent.py --compare "GANs" "Diffusion Models"
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='Research query or topic'
    )
    
    parser.add_argument(
        '--max-papers',
        type=int,
        default=None,
        help='Maximum number of papers to retrieve (default: 15)'
    )
    
    parser.add_argument(
        '--days-back',
        type=int,
        default=None,
        help='Number of days to look back (default: 730)'
    )
    
    parser.add_argument(
        '--no-deep-analysis',
        action='store_true',
        help='Skip deep analysis with GPT-4o (faster but less detailed)'
    )
    
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--compare',
        nargs=2,
        metavar=('TOPIC1', 'TOPIC2'),
        help='Compare two research topics'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ResearchAgent(config_path=args.config)
    
    # Interactive mode
    if args.interactive:
        agent.interactive_mode()
        return
    
    # Comparison mode
    if args.compare:
        agent.compare_topics(args.compare[0], args.compare[1], max_papers=args.max_papers or 10)
        return
    
    # Regular search mode
    if args.query:
        results = agent.run_research_query(
            query=args.query,
            max_papers=args.max_papers,
            days_back=args.days_back,
            deep_analysis=not args.no_deep_analysis
        )
        
        # Ask if user wants to store session
        if results and Confirm.ask("\nStore this session for later retrieval?"):
            session_name = Prompt.ask("Session name")
            agent.store_session(session_name, results)
        
        return
    
    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
