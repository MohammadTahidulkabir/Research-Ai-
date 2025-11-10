"""Vector storage and RAG capabilities for research sessions."""

from typing import List, Dict, Optional
try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.docstore.document import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    OpenAIEmbeddings = None
    FAISS = None
    Document = dict  # Fallback to dict

import os
import json
import pickle
from rich.console import Console

console = Console()


class VectorStoreManager:
    """Manages vector storage for research sessions."""
    
    def __init__(self, config: dict):
        """Initialize vector store manager."""
        self.config = config['research_agent']
        self.storage_config = self.config['storage']
        self.persist_path = self.storage_config['persist_path']
        
        # Initialize embeddings
        self.embeddings = None
        if LANGCHAIN_AVAILABLE:
            try:
                self.embeddings = OpenAIEmbeddings(
                    model=self.storage_config['embedding_model']
                )
            except Exception as e:
                console.print(f"[yellow]Warning: Could not initialize OpenAI embeddings: {str(e)}[/yellow]")
        else:
            console.print(f"[yellow]Warning: LangChain not available, vector storage disabled[/yellow]")
        
        # Create persist directory
        os.makedirs(self.persist_path, exist_ok=True)
    
    def store_research_session(
        self,
        session_name: str,
        papers: List[Dict],
        insights: Dict,
        research_directions: List[Dict],
        query: str
    ) -> bool:
        """
        Store a complete research session with vector embeddings.
        
        Args:
            session_name: Name for the session
            papers: List of paper dictionaries
            insights: Analysis insights
            research_directions: Generated research directions
            query: Original search query
        
        Returns:
            Success status
        """
        if not self.embeddings:
            console.print("[red]Cannot store session: OpenAI embeddings not initialized[/red]")
            return False
        
        console.print(f"\n[cyan]💾 Storing research session: {session_name}...[/cyan]")
        
        try:
            # Prepare documents for embedding
            documents = self._prepare_documents(papers, insights, research_directions)
            
            # Create vector store
            vectorstore = FAISS.from_documents(documents, self.embeddings)
            
            # Create session directory
            session_path = os.path.join(self.persist_path, session_name)
            os.makedirs(session_path, exist_ok=True)
            
            # Save vector store
            vectorstore.save_local(session_path)
            
            # Save metadata
            metadata = {
                'session_name': session_name,
                'query': query,
                'num_papers': len(papers),
                'created_at': str(papers[0]['published']) if papers else None,
                'papers': papers,
                'insights': insights,
                'research_directions': research_directions
            }
            
            # Convert datetime objects to strings
            for paper in metadata['papers']:
                paper['published'] = paper['published'].isoformat()
                paper['updated'] = paper['updated'].isoformat()
            
            metadata_path = os.path.join(session_path, 'metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, indent=2, fp=f)
            
            console.print(f"[green]✓ Session stored at: {session_path}[/green]")
            console.print(f"[green]  - {len(papers)} papers embedded[/green]")
            console.print(f"[green]  - {len(documents)} document chunks indexed[/green]")
            
            return True
        
        except Exception as e:
            console.print(f"[red]Error storing session: {str(e)}[/red]")
            return False
    
    def _prepare_documents(
        self,
        papers: List[Dict],
        insights: Dict,
        research_directions: List[Dict]
    ) -> List[Document]:
        """Prepare documents for vector embedding."""
        documents = []
        
        # Add papers
        for paper in papers:
            # Main paper content
            content = f"Title: {paper['title']}\n\n"
            content += f"Authors: {', '.join(paper['authors'][:5])}\n\n"
            content += f"Abstract: {paper['summary']}\n\n"
            
            if 'fast_summary' in paper:
                content += f"Summary: {paper['fast_summary']}\n\n"
            
            if 'deep_analysis' in paper:
                analysis = paper['deep_analysis']
                if analysis.get('contributions'):
                    content += f"Contributions: {' '.join(analysis['contributions'])}\n\n"
                if analysis.get('methods'):
                    content += f"Methods: {' '.join(analysis['methods'])}\n\n"
            
            metadata = {
                'type': 'paper',
                'arxiv_id': paper['id'],
                'title': paper['title'],
                'year': paper['published'][:4] if isinstance(paper['published'], str) else paper['published'].year
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        # Add insights
        if insights:
            insights_content = "Research Insights:\n\n"
            
            for key, items in insights.items():
                insights_content += f"{key.replace('_', ' ').title()}:\n"
                for item in items[:5]:
                    if isinstance(item, dict):
                        insights_content += f"- {item.get('item', 'N/A')}: {item.get('details', '')}\n"
                    else:
                        insights_content += f"- {item}\n"
                insights_content += "\n"
            
            documents.append(Document(
                page_content=insights_content,
                metadata={'type': 'insights'}
            ))
        
        # Add research directions
        for i, direction in enumerate(research_directions, 1):
            content = f"Research Direction {i}:\n\n"
            content += f"Title: {direction.get('title', 'N/A')}\n\n"
            content += f"Motivation: {direction.get('motivation', 'N/A')}\n\n"
            content += f"Approach: {direction.get('approach', 'N/A')}\n\n"
            content += f"Expected Contribution: {direction.get('expected_contribution', 'N/A')}\n\n"
            
            documents.append(Document(
                page_content=content,
                metadata={'type': 'research_direction', 'index': i}
            ))
        
        return documents
    
    def load_research_session(self, session_name: str) -> Optional[Dict]:
        """
        Load a previously stored research session.
        
        Args:
            session_name: Name of the session to load
        
        Returns:
            Session data dictionary or None if not found
        """
        session_path = os.path.join(self.persist_path, session_name)
        
        if not os.path.exists(session_path):
            console.print(f"[red]Session not found: {session_name}[/red]")
            return None
        
        console.print(f"\n[cyan]📂 Loading research session: {session_name}...[/cyan]")
        
        try:
            # Load metadata
            metadata_path = os.path.join(session_path, 'metadata.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Load vector store
            if self.embeddings:
                vectorstore = FAISS.load_local(
                    session_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                metadata['vectorstore'] = vectorstore
            
            console.print(f"[green]✓ Session loaded: {metadata['num_papers']} papers[/green]")
            
            return metadata
        
        except Exception as e:
            console.print(f"[red]Error loading session: {str(e)}[/red]")
            return None
    
    def query_session(self, session_name: str, query: str, k: int = 5) -> List[Dict]:
        """
        Query a stored research session using semantic search.
        
        Args:
            session_name: Name of the session
            query: Search query
            k: Number of results to return
        
        Returns:
            List of relevant documents
        """
        session_data = self.load_research_session(session_name)
        
        if not session_data or 'vectorstore' not in session_data:
            return []
        
        console.print(f"\n[cyan]🔍 Querying session for: {query}...[/cyan]")
        
        try:
            vectorstore = session_data['vectorstore']
            results = vectorstore.similarity_search_with_score(query, k=k)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'relevance_score': float(score)
                })
            
            console.print(f"[green]✓ Found {len(formatted_results)} relevant results[/green]")
            
            return formatted_results
        
        except Exception as e:
            console.print(f"[red]Error querying session: {str(e)}[/red]")
            return []
    
    def list_sessions(self) -> List[str]:
        """List all stored research sessions."""
        if not os.path.exists(self.persist_path):
            return []
        
        sessions = []
        for item in os.listdir(self.persist_path):
            item_path = os.path.join(self.persist_path, item)
            if os.path.isdir(item_path):
                metadata_path = os.path.join(item_path, 'metadata.json')
                if os.path.exists(metadata_path):
                    sessions.append(item)
        
        return sessions
    
    def delete_session(self, session_name: str) -> bool:
        """Delete a stored research session."""
        session_path = os.path.join(self.persist_path, session_name)
        
        if not os.path.exists(session_path):
            console.print(f"[red]Session not found: {session_name}[/red]")
            return False
        
        try:
            import shutil
            shutil.rmtree(session_path)
            console.print(f"[green]✓ Session deleted: {session_name}[/green]")
            return True
        
        except Exception as e:
            console.print(f"[red]Error deleting session: {str(e)}[/red]")
            return False
    
    def update_session(self, session_name: str, new_papers: List[Dict]) -> bool:
        """Update an existing session with new papers."""
        session_data = self.load_research_session(session_name)
        
        if not session_data:
            return False
        
        console.print(f"\n[cyan]🔄 Updating session: {session_name}...[/cyan]")
        
        try:
            # Merge papers (avoid duplicates)
            existing_ids = {p['id'] for p in session_data['papers']}
            new_unique_papers = [p for p in new_papers if p['id'] not in existing_ids]
            
            if not new_unique_papers:
                console.print("[yellow]No new papers to add[/yellow]")
                return True
            
            # Update papers list
            all_papers = session_data['papers'] + new_unique_papers
            
            # Re-store with updated data
            return self.store_research_session(
                session_name,
                all_papers,
                session_data['insights'],
                session_data['research_directions'],
                session_data['query']
            )
        
        except Exception as e:
            console.print(f"[red]Error updating session: {str(e)}[/red]")
            return False
    
    def export_session_summary(self, session_name: str) -> str:
        """Export a quick summary of a stored session."""
        session_data = self.load_research_session(session_name)
        
        if not session_data:
            return "Session not found"
        
        summary = f"# Session: {session_name}\n\n"
        summary += f"**Query:** {session_data['query']}\n"
        summary += f"**Papers:** {session_data['num_papers']}\n"
        summary += f"**Created:** {session_data.get('created_at', 'Unknown')}\n\n"
        
        summary += "## Papers:\n"
        for paper in session_data['papers'][:5]:
            summary += f"- {paper['title']} ({paper['published'][:4]})\n"
        
        if len(session_data['papers']) > 5:
            summary += f"- ... and {len(session_data['papers']) - 5} more\n"
        
        return summary
