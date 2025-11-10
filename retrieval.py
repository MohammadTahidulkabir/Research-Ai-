"""Paper retrieval module using arXiv API."""

import arxiv
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class PaperRetriever:
    """Handles paper retrieval from arXiv."""
    
    def __init__(self, config: dict):
        """Initialize retriever with configuration."""
        self.config = config['research_agent']
        self.arxiv_config = self.config['apis']['arxiv']
        
        # Initialize arXiv client
        self.client = arxiv.Client(
            page_size=self.arxiv_config['page_size'],
            delay_seconds=self.arxiv_config['delay_seconds'],
            num_retries=self.arxiv_config['num_retries']
        )
    
    def fetch_papers(
        self,
        query: str,
        max_results: int = None,
        days_back: int = None,
        categories: List[str] = None,
        sort_by: str = 'submittedDate'
    ) -> List[Dict]:
        """
        Fetch papers from arXiv.
        
        Args:
            query: Search query string
            max_results: Maximum number of papers to retrieve
            days_back: Number of days to look back
            categories: List of arXiv categories to filter
            sort_by: Sort criterion ('submittedDate', 'lastUpdatedDate', 'relevance')
        
        Returns:
            List of paper dictionaries
        """
        # Use defaults if not specified
        if max_results is None:
            max_results = self.config['defaults']['max_papers']
        if days_back is None:
            days_back = self.config['defaults']['days_back']
        if categories is None:
            categories = self.config['defaults']['categories']
        
        # Construct search query
        search_query = self._construct_query(query, categories)
        
        # Set sort criterion
        sort_criterion_map = {
            'submittedDate': arxiv.SortCriterion.SubmittedDate,
            'lastUpdatedDate': arxiv.SortCriterion.LastUpdatedDate,
            'relevance': arxiv.SortCriterion.Relevance
        }
        sort_criterion = sort_criterion_map.get(sort_by, arxiv.SortCriterion.SubmittedDate)
        
        # Create search
        search = arxiv.Search(
            query=search_query,
            max_results=max_results * 2,  # Fetch extra to account for date filtering
            sort_by=sort_criterion,
            sort_order=arxiv.SortOrder.Descending
        )
        
        # Calculate date threshold (timezone-aware)
        from datetime import timezone
        date_threshold = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        # Fetch papers with progress indicator
        papers = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Fetching papers from arXiv...", total=None)
            
            try:
                for result in self.client.results(search):
                    # Filter by date
                    if result.published >= date_threshold:
                        paper = self._parse_paper(result)
                        papers.append(paper)
                        
                        # Stop if we have enough papers
                        if len(papers) >= max_results:
                            break
                    
                    progress.update(task, description=f"Fetched {len(papers)} papers...")
            
            except Exception as e:
                console.print(f"[red]Error fetching papers: {str(e)}[/red]")
                return []
        
        console.print(f"[green]✓ Retrieved {len(papers)} papers[/green]")
        return papers
    
    def _construct_query(self, query: str, categories: List[str]) -> str:
        """Construct arXiv query with category filters."""
        # Check if query already has arXiv operators
        if any(op in query for op in ['au:', 'ti:', 'abs:', 'cat:', 'AND', 'OR']):
            return query
        
        # Simple query - search in title and abstract
        base_query = f"(ti:{query} OR abs:{query})"
        
        # Add category filters if specified
        if categories:
            cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
            return f"{base_query} AND ({cat_query})"
        
        return base_query
    
    def _parse_paper(self, result: arxiv.Result) -> Dict:
        """Parse arXiv result into paper dictionary."""
        return {
            'id': result.get_short_id(),
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'published': result.published,
            'updated': result.updated,
            'summary': result.summary.replace('\n', ' '),
            'categories': result.categories,
            'primary_category': result.primary_category,
            'pdf_url': result.pdf_url,
            'entry_url': result.entry_id,
            'comment': result.comment,
            'journal_ref': result.journal_ref,
            'doi': result.doi
        }
    
    def search_by_author(self, author_name: str, max_results: int = 10) -> List[Dict]:
        """Search papers by author name."""
        query = f"au:{author_name}"
        return self.fetch_papers(query, max_results=max_results)
    
    def search_by_category(self, category: str, max_results: int = 10) -> List[Dict]:
        """Search papers by arXiv category."""
        query = f"cat:{category}"
        return self.fetch_papers(query, max_results=max_results, categories=None)
    
    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict]:
        """Retrieve a specific paper by arXiv ID."""
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(self.client.results(search))
            return self._parse_paper(result)
        except Exception as e:
            console.print(f"[red]Error retrieving paper {arxiv_id}: {str(e)}[/red]")
            return None
    
    def validate_query(self, query: str) -> tuple:
        """Validate arXiv query syntax."""
        if not query or len(query.strip()) == 0:
            return False, "Query cannot be empty"
        
        # Check for balanced parentheses
        if query.count('(') != query.count(')'):
            return False, "Unbalanced parentheses in query"
        
        # Check for valid operators
        valid_operators = ['au:', 'ti:', 'abs:', 'cat:', 'AND', 'OR', 'ANDNOT']
        
        return True, "Valid query"
    
    def suggest_query_improvements(self, query: str, num_results: int) -> List[str]:
        """Suggest query improvements if results are insufficient."""
        suggestions = []
        
        if num_results == 0:
            suggestions.append("Try broader search terms")
            suggestions.append("Remove date restrictions")
            suggestions.append("Check category codes")
            suggestions.append(f"Try: 'ti:{query}' or 'abs:{query}'")
        
        elif num_results < 5:
            suggestions.append("Consider expanding time range")
            suggestions.append("Try related keywords")
            suggestions.append("Remove category filters")
        
        return suggestions
