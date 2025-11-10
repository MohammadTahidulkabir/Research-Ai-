"""
Test script for AI Research Agent
Run this to verify your installation and configuration.
"""

import sys
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_imports():
    """Test if all required packages are installed."""
    console.print("\n[cyan]Testing imports...[/cyan]")
    
    required_packages = [
        ('arxiv', 'arxiv'),
        ('groq', 'Groq'),
        ('openai', 'OpenAI'),
        ('langchain', 'langchain'),
        ('langchain_openai', 'OpenAIEmbeddings'),
        ('langchain_community.vectorstores', 'FAISS'),
        ('yaml', 'pyyaml'),
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('rich', 'rich')
    ]
    
    failed = []
    for package, display_name in required_packages:
        try:
            __import__(package)
            console.print(f"  ✓ {display_name}")
        except ImportError:
            console.print(f"  ✗ {display_name} [red](missing)[/red]")
            failed.append(display_name)
    
    if failed:
        console.print(f"\n[red]Missing packages: {', '.join(failed)}[/red]")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
        return False
    
    console.print("[green]All packages installed![/green]")
    return True


def test_config():
    """Test configuration loading."""
    console.print("\n[cyan]Testing configuration...[/cyan]")
    
    try:
        from src.utils import load_config
        config = load_config("config.yaml")
        
        # Check required sections
        assert 'research_agent' in config
        assert 'apis' in config['research_agent']
        assert 'groq' in config['research_agent']['apis']
        
        console.print("  ✓ config.yaml loaded")
        console.print("  ✓ Groq API key configured")
        
        # Check OpenAI key
        openai_key = config['research_agent']['apis']['openai']['api_key']
        if openai_key and openai_key != '':
            console.print("  ✓ OpenAI API key configured")
        else:
            console.print("  ⚠ OpenAI API key not set [yellow](optional for basic features)[/yellow]")
        
        console.print("[green]Configuration valid![/green]")
        return True
    
    except Exception as e:
        console.print(f"[red]Configuration error: {str(e)}[/red]")
        return False


def test_retrieval():
    """Test paper retrieval from arXiv."""
    console.print("\n[cyan]Testing arXiv retrieval...[/cyan]")
    
    try:
        from src.retrieval import PaperRetriever
        from src.utils import load_config
        
        config = load_config("config.yaml")
        retriever = PaperRetriever(config)
        
        # Fetch a small number of papers
        console.print("  Fetching 2 test papers...")
        papers = retriever.fetch_papers(
            query="machine learning",
            max_results=2,
            days_back=30
        )
        
        if papers and len(papers) > 0:
            console.print(f"  ✓ Retrieved {len(papers)} papers")
            console.print(f"  ✓ Sample: {papers[0]['title'][:50]}...")
            console.print("[green]arXiv retrieval working![/green]")
            return True
        else:
            console.print("[yellow]No papers retrieved (might be rate limited)[/yellow]")
            return False
    
    except Exception as e:
        console.print(f"[red]Retrieval error: {str(e)}[/red]")
        return False


def test_groq():
    """Test Groq API connection."""
    console.print("\n[cyan]Testing Groq API...[/cyan]")
    
    try:
        from groq import Groq
        from src.utils import load_config
        
        config = load_config("config.yaml")
        api_key = config['research_agent']['apis']['groq']['api_key']
        
        client = Groq(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'test successful' in 2 words"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        console.print(f"  ✓ Groq API response: {result}")
        console.print("[green]Groq API working![/green]")
        return True
    
    except Exception as e:
        console.print(f"[red]Groq API error: {str(e)}[/red]")
        console.print("[yellow]Check your Groq API key in config.yaml[/yellow]")
        return False


def test_openai():
    """Test OpenAI API connection (optional)."""
    console.print("\n[cyan]Testing OpenAI API (optional)...[/cyan]")
    
    try:
        from openai import OpenAI
        from src.utils import load_config
        import os
        
        config = load_config("config.yaml")
        api_key = config['research_agent']['apis']['openai']['api_key']
        
        if not api_key or api_key == '':
            console.print("  ⚠ OpenAI API key not configured [yellow](skipping)[/yellow]")
            return None
        
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use cheaper model for testing
            messages=[{"role": "user", "content": "Say 'test successful' in 2 words"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        console.print(f"  ✓ OpenAI API response: {result}")
        console.print("[green]OpenAI API working![/green]")
        return True
    
    except Exception as e:
        console.print(f"[yellow]OpenAI API error: {str(e)}[/yellow]")
        console.print("[yellow]Deep analysis features will be limited[/yellow]")
        return False


def test_directories():
    """Test if required directories exist or can be created."""
    console.print("\n[cyan]Testing directories...[/cyan]")
    
    import os
    
    directories = ['reports', 'vector_stores']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            console.print(f"  ✓ {directory}/ ready")
        except Exception as e:
            console.print(f"  ✗ {directory}/ [red]error: {str(e)}[/red]")
            return False
    
    console.print("[green]Directories ready![/green]")
    return True


def run_all_tests():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]🔬 AI Research Agent - System Test[/bold cyan]",
        border_style="cyan"
    ))
    
    results = {
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Directories': test_directories(),
        'arXiv Retrieval': test_retrieval(),
        'Groq API': test_groq(),
        'OpenAI API': test_openai()
    }
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold]Test Summary:[/bold]\n")
    
    for test_name, result in results.items():
        if result is True:
            status = "[green]✓ PASS[/green]"
        elif result is False:
            status = "[red]✗ FAIL[/red]"
        else:
            status = "[yellow]⚠ SKIP[/yellow]"
        
        console.print(f"  {status} {test_name}")
    
    # Overall status
    console.print("\n" + "=" * 60)
    
    failed_tests = [name for name, result in results.items() if result is False]
    
    if not failed_tests:
        console.print(Panel.fit(
            "[bold green]✓ All tests passed![/bold green]\n"
            "You're ready to use the AI Research Agent.\n\n"
            "Try: python research_agent.py \"your research topic\"",
            border_style="green"
        ))
        return True
    else:
        console.print(Panel.fit(
            f"[bold red]✗ {len(failed_tests)} test(s) failed[/bold red]\n\n"
            f"Failed: {', '.join(failed_tests)}\n\n"
            "Please fix the issues above before using the agent.",
            border_style="red"
        ))
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
