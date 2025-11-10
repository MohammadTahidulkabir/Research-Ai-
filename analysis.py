"""Analysis module for trend detection and gap identification."""

from typing import List, Dict
from collections import Counter
from datetime import datetime
import re


class ResearchAnalyzer:
    """Analyzes research papers for trends, patterns, and gaps."""
    
    def __init__(self):
        """Initialize analyzer."""
        pass
    
    def analyze_temporal_trends(self, papers: List[Dict]) -> Dict:
        """Analyze publication trends over time."""
        # Group papers by year and month
        by_year = Counter()
        by_month = Counter()
        
        for paper in papers:
            year = paper['published'].year
            month = paper['published'].strftime('%Y-%m')
            by_year[year] += 1
            by_month[month] += 1
        
        return {
            'by_year': dict(sorted(by_year.items())),
            'by_month': dict(sorted(by_month.items())),
            'total_papers': len(papers),
            'date_range': {
                'start': min(p['published'] for p in papers).strftime('%Y-%m-%d'),
                'end': max(p['published'] for p in papers).strftime('%Y-%m-%d')
            }
        }
    
    def analyze_categories(self, papers: List[Dict]) -> Dict:
        """Analyze distribution of arXiv categories."""
        primary_categories = Counter()
        all_categories = Counter()
        
        for paper in papers:
            primary_categories[paper['primary_category']] += 1
            for cat in paper['categories']:
                all_categories[cat] += 1
        
        return {
            'primary_categories': dict(primary_categories.most_common()),
            'all_categories': dict(all_categories.most_common(10)),
            'category_diversity': len(all_categories)
        }
    
    def analyze_authors(self, papers: List[Dict]) -> Dict:
        """Analyze author patterns and collaborations."""
        author_counts = Counter()
        collaboration_sizes = []
        
        for paper in papers:
            for author in paper['authors']:
                author_counts[author] += 1
            collaboration_sizes.append(len(paper['authors']))
        
        return {
            'top_authors': dict(author_counts.most_common(10)),
            'total_unique_authors': len(author_counts),
            'avg_collaboration_size': sum(collaboration_sizes) / len(collaboration_sizes),
            'max_collaboration_size': max(collaboration_sizes),
            'min_collaboration_size': min(collaboration_sizes)
        }
    
    def extract_common_terms(self, papers: List[Dict], top_n: int = 20) -> List[tuple]:
        """Extract most common terms from titles and abstracts."""
        # Combine all text
        all_text = []
        for paper in papers:
            all_text.append(paper['title'].lower())
            all_text.append(paper['summary'].lower())
        
        text = ' '.join(all_text)
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'we', 'our', 'they', 'their',
            'with', 'from', 'by', 'as', 'which', 'can', 'using', 'used'
        }
        
        # Extract words (alphanumeric, 3+ chars)
        words = re.findall(r'\b[a-z]{3,}\b', text)
        words = [w for w in words if w not in stop_words]
        
        # Count frequencies
        word_counts = Counter(words)
        
        return word_counts.most_common(top_n)
    
    def detect_methodology_patterns(self, papers: List[Dict]) -> Dict:
        """Detect common methodological patterns."""
        # Keywords for different methodologies
        method_keywords = {
            'deep_learning': ['neural', 'deep learning', 'cnn', 'rnn', 'lstm', 'transformer'],
            'machine_learning': ['classification', 'regression', 'clustering', 'supervised', 'unsupervised'],
            'reinforcement_learning': ['reinforcement', 'policy', 'reward', 'agent', 'q-learning'],
            'optimization': ['optimization', 'gradient', 'optimizer', 'sgd', 'adam'],
            'probabilistic': ['bayesian', 'probabilistic', 'stochastic', 'distribution'],
            'generative': ['generative', 'gan', 'vae', 'diffusion', 'autoencoder'],
            'attention': ['attention', 'self-attention', 'cross-attention', 'multi-head']
        }
        
        method_counts = {method: 0 for method in method_keywords}
        
        for paper in papers:
            text = (paper['title'] + ' ' + paper['summary']).lower()
            for method, keywords in method_keywords.items():
                if any(keyword in text for keyword in keywords):
                    method_counts[method] += 1
        
        return {
            'method_distribution': method_counts,
            'most_common': max(method_counts, key=method_counts.get),
            'diversity_score': len([v for v in method_counts.values() if v > 0])
        }
    
    def identify_dataset_mentions(self, papers: List[Dict]) -> List[tuple]:
        """Identify commonly mentioned datasets."""
        # Common dataset names
        dataset_patterns = [
            'imagenet', 'coco', 'mnist', 'cifar', 'glue', 'squad',
            'wikitext', 'openwebtext', 'common crawl', 'bookcorpus',
            'librispeech', 'voxceleb', 'kinetics', 'youtube',
            'ms marco', 'natural questions', 'hotpotqa'
        ]
        
        dataset_counts = Counter()
        
        for paper in papers:
            text = (paper['title'] + ' ' + paper['summary']).lower()
            for dataset in dataset_patterns:
                if dataset in text:
                    dataset_counts[dataset] += 1
        
        return dataset_counts.most_common(10)
    
    def identify_limitations(self, papers: List[Dict]) -> List[str]:
        """Extract limitation patterns from papers with deep analysis."""
        limitations = []
        
        for paper in papers:
            if 'deep_analysis' in paper:
                paper_limitations = paper['deep_analysis'].get('limitations', [])
                limitations.extend(paper_limitations)
        
        # Count similar limitations
        limitation_counts = Counter(limitations)
        
        # Return unique limitations sorted by frequency
        return [lim for lim, count in limitation_counts.most_common(15)]
    
    def identify_research_gaps(self, papers: List[Dict], insights: Dict) -> List[Dict]:
        """Identify research gaps based on paper analysis."""
        gaps = []
        
        # Gap 1: Underexplored combinations
        methods = insights.get('common_methods', [])
        datasets = insights.get('datasets_used', [])
        
        if len(methods) > 1 and len(datasets) > 1:
            gaps.append({
                'type': 'methodological',
                'description': 'Potential for combining different methodological approaches',
                'details': f"Methods like {methods[0].get('item', 'N/A')} could be tested with alternative datasets"
            })
        
        # Gap 2: Temporal gaps
        temporal_analysis = self.analyze_temporal_trends(papers)
        recent_year = max(temporal_analysis['by_year'].keys())
        if temporal_analysis['by_year'].get(recent_year, 0) < 3:
            gaps.append({
                'type': 'temporal',
                'description': 'Limited recent work in this area',
                'details': f"Only {temporal_analysis['by_year'].get(recent_year, 0)} papers in {recent_year}"
            })
        
        # Gap 3: Application gaps
        research_gaps = insights.get('research_gaps', [])
        for gap in research_gaps[:3]:
            if isinstance(gap, dict):
                gaps.append({
                    'type': 'application',
                    'description': gap.get('item', 'Unknown gap'),
                    'details': gap.get('details', '')
                })
        
        return gaps
    
    def compare_topics(self, papers1: List[Dict], papers2: List[Dict], topic1: str, topic2: str) -> Dict:
        """Compare two sets of papers on different topics."""
        comparison = {
            'topic1': topic1,
            'topic2': topic2,
            'paper_counts': {
                topic1: len(papers1),
                topic2: len(papers2)
            },
            'temporal_trends': {
                topic1: self.analyze_temporal_trends(papers1),
                topic2: self.analyze_temporal_trends(papers2)
            },
            'methodologies': {
                topic1: self.detect_methodology_patterns(papers1),
                topic2: self.detect_methodology_patterns(papers2)
            },
            'categories': {
                topic1: self.analyze_categories(papers1),
                topic2: self.analyze_categories(papers2)
            }
        }
        
        return comparison
    
    def analyze_citation_potential(self, papers: List[Dict]) -> List[Dict]:
        """Analyze papers for citation potential (based on recency, venue, etc.)."""
        scored_papers = []
        
        current_year = datetime.now().year
        
        for paper in papers:
            score = 0
            factors = []
            
            # Recency score (newer = higher)
            age_years = current_year - paper['published'].year
            if age_years == 0:
                score += 5
                factors.append("Very recent (2024)")
            elif age_years == 1:
                score += 3
                factors.append("Recent (2023)")
            elif age_years <= 2:
                score += 1
            
            # Journal reference (peer-reviewed)
            if paper.get('journal_ref'):
                score += 3
                factors.append("Peer-reviewed")
            
            # DOI (published)
            if paper.get('doi'):
                score += 2
                factors.append("Has DOI")
            
            # Multiple categories (interdisciplinary)
            if len(paper['categories']) > 2:
                score += 1
                factors.append("Interdisciplinary")
            
            scored_papers.append({
                'paper': paper,
                'citation_score': score,
                'factors': factors
            })
        
        # Sort by score
        scored_papers.sort(key=lambda x: x['citation_score'], reverse=True)
        
        return scored_papers
