"""
Example usage of the AI Research Agent
"""

from src import (
    PaperRetriever,
    PaperSummarizer,
    ResearchAnalyzer,
    ReportGenerator,
    VectorStoreManager,
    load_config
)


def example_basic_search():
    """Example: Basic paper search and summarization."""
    print("=" * 60)
    print("Example 1: Basic Paper Search")
    print("=" * 60)
    
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize retriever
    retriever = PaperRetriever(config)
    
    # Fetch papers
    papers = retriever.fetch_papers(
        query="vision transformers",
        max_results=5,
        days_back=365
    )
    
    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}")
        print(f"   Authors: {', '.join(paper['authors'][:3])}")
        print(f"   Published: {paper['published'].strftime('%Y-%m-%d')}")
        print()


def example_full_analysis():
    """Example: Complete research workflow with analysis."""
    print("=" * 60)
    print("Example 2: Full Research Analysis")
    print("=" * 60)
    
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize components
    retriever = PaperRetriever(config)
    summarizer = PaperSummarizer(config)
    analyzer = ResearchAnalyzer()
    report_gen = ReportGenerator(config)
    
    # Retrieve papers
    query = "attention mechanisms in transformers"
    papers = retriever.fetch_papers(query, max_results=10)
    
    # Fast summarization
    papers = summarizer.summarize_papers_fast(papers)
    
    # Deep analysis (optional - requires OpenAI API key)
    # papers = summarizer.analyze_papers_deep(papers)
    
    # Extract insights
    insights = summarizer.extract_key_insights(papers)
    
    # Generate research directions
    directions = summarizer.generate_research_directions(papers, insights)
    
    # Analyze trends
    temporal = analyzer.analyze_temporal_trends(papers)
    categories = analyzer.analyze_categories(papers)
    
    # Generate report
    report = report_gen.generate_markdown_report(
        query=query,
        papers=papers,
        insights=insights,
        research_directions=directions,
        analysis_data={'temporal': temporal, 'categories': categories}
    )
    
    # Save report
    filepath = report_gen.save_report(report, "example_report", "markdown")
    print(f"\nReport saved to: {filepath}")


def example_comparison():
    """Example: Compare two research topics."""
    print("=" * 60)
    print("Example 3: Topic Comparison")
    print("=" * 60)
    
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize components
    retriever = PaperRetriever(config)
    analyzer = ResearchAnalyzer()
    report_gen = ReportGenerator(config)
    
    # Retrieve papers for both topics
    topic1 = "GANs"
    topic2 = "Diffusion Models"
    
    papers1 = retriever.fetch_papers(topic1, max_results=10)
    papers2 = retriever.fetch_papers(topic2, max_results=10)
    
    # Compare
    comparison = analyzer.compare_topics(papers1, papers2, topic1, topic2)
    
    # Generate comparison report
    report = report_gen.generate_comparison_report(comparison)
    
    # Save
    filepath = report_gen.save_report(report, "comparison_report", "markdown")
    print(f"\nComparison report saved to: {filepath}")


def example_vector_storage():
    """Example: Store and query research sessions."""
    print("=" * 60)
    print("Example 4: Vector Storage and RAG")
    print("=" * 60)
    
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize components
    retriever = PaperRetriever(config)
    summarizer = PaperSummarizer(config)
    vector_store = VectorStoreManager(config)
    
    # Retrieve and summarize papers
    query = "reinforcement learning"
    papers = retriever.fetch_papers(query, max_results=5)
    papers = summarizer.summarize_papers_fast(papers)
    
    # Create mock insights and directions
    insights = {'common_methods': [], 'research_gaps': []}
    directions = []
    
    # Store session
    session_name = "rl_survey_2024"
    success = vector_store.store_research_session(
        session_name=session_name,
        papers=papers,
        insights=insights,
        research_directions=directions,
        query=query
    )
    
    if success:
        print(f"\nSession stored: {session_name}")
        
        # Query the session
        results = vector_store.query_session(
            session_name=session_name,
            query="What are the main approaches in RL?",
            k=3
        )
        
        print(f"\nFound {len(results)} relevant results")


def example_export_formats():
    """Example: Export in different formats."""
    print("=" * 60)
    print("Example 5: Export Formats")
    print("=" * 60)
    
    # Load configuration
    config = load_config("config.yaml")
    
    # Initialize components
    retriever = PaperRetriever(config)
    report_gen = ReportGenerator(config)
    
    # Retrieve papers
    papers = retriever.fetch_papers("neural networks", max_results=5)
    
    # Generate BibTeX
    bibtex = report_gen.generate_bibtex(papers)
    bibtex_path = report_gen.save_report(bibtex, "references", "bibtex")
    print(f"BibTeX saved to: {bibtex_path}")
    
    # Generate JSON
    json_export = report_gen.generate_json(papers, {}, [])
    json_path = report_gen.save_report(json_export, "data", "json")
    print(f"JSON saved to: {json_path}")


if __name__ == "__main__":
    # Run examples
    print("\n🔬 AI Research Agent - Example Usage\n")
    
    # Choose which example to run
    examples = {
        '1': ('Basic Search', example_basic_search),
        '2': ('Full Analysis', example_full_analysis),
        '3': ('Topic Comparison', example_comparison),
        '4': ('Vector Storage', example_vector_storage),
        '5': ('Export Formats', example_export_formats)
    }
    
    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    choice = input("\nSelect example (1-5) or 'all': ").strip()
    
    if choice == 'all':
        for name, func in examples.values():
            try:
                func()
                print("\n")
            except Exception as e:
                print(f"Error in {name}: {str(e)}\n")
    elif choice in examples:
        name, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Invalid choice")
