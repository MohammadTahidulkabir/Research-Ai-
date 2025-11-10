"""Report generation module for creating formatted research reports."""

from typing import List, Dict
from datetime import datetime
import json


class ReportGenerator:
    """Generates formatted research reports in multiple formats."""
    
    def __init__(self, config: dict):
        """Initialize report generator."""
        self.config = config['research_agent']
        self.output_config = self.config['output']
    
    def generate_markdown_report(
        self,
        query: str,
        papers: List[Dict],
        insights: Dict,
        research_directions: List[Dict],
        analysis_data: Dict = None
    ) -> str:
        """Generate comprehensive markdown report."""
        
        report_lines = []
        
        # Header
        report_lines.append(f"# 📘 Research Report: {query}")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Papers Analyzed:** {len(papers)}")
        
        if papers:
            start_date = min(p['published'] for p in papers).strftime('%Y-%m-%d')
            end_date = max(p['published'] for p in papers).strftime('%Y-%m-%d')
            report_lines.append(f"**Date Range:** {start_date} to {end_date}")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Summary of Recent Works
        report_lines.append("## 🔍 Summary of Recent Works")
        report_lines.append("")
        
        for i, paper in enumerate(papers, 1):
            report_lines.extend(self._format_paper_section(paper, i))
        
        # Cross-Paper Analysis
        report_lines.append("## 🧠 Cross-Paper Analysis")
        report_lines.append("")
        
        # Dominant Approaches
        if insights.get('common_methods'):
            report_lines.append("### Dominant Approaches")
            report_lines.append("")
            for i, method in enumerate(insights['common_methods'][:5], 1):
                if isinstance(method, dict):
                    report_lines.append(f"{i}. **{method.get('item', 'N/A')}**")
                    report_lines.append(f"   - {method.get('details', 'No details available')}")
                else:
                    report_lines.append(f"{i}. **{method}**")
                report_lines.append("")
        
        # Common Datasets & Benchmarks
        if insights.get('datasets_used'):
            report_lines.append("### Common Datasets & Benchmarks")
            report_lines.append("")
            for dataset in insights['datasets_used'][:5]:
                if isinstance(dataset, dict):
                    report_lines.append(f"- **{dataset.get('item', 'N/A')}**: {dataset.get('details', '')}")
                else:
                    report_lines.append(f"- {dataset}")
            report_lines.append("")
        
        # Evaluation Metrics
        if insights.get('metrics'):
            report_lines.append("### Evaluation Metrics")
            report_lines.append("")
            for metric in insights['metrics'][:5]:
                if isinstance(metric, dict):
                    report_lines.append(f"- **{metric.get('item', 'N/A')}**: {metric.get('details', '')}")
                else:
                    report_lines.append(f"- {metric}")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # Identified Limitations & Gaps
        report_lines.append("## 🚨 Identified Limitations & Gaps")
        report_lines.append("")
        
        if insights.get('limitations'):
            report_lines.append("### Limitations Across Papers")
            report_lines.append("")
            for i, limitation in enumerate(insights['limitations'][:5], 1):
                if isinstance(limitation, dict):
                    report_lines.append(f"{i}. **{limitation.get('item', 'N/A')}**")
                    report_lines.append(f"   - {limitation.get('details', '')}")
                else:
                    report_lines.append(f"{i}. {limitation}")
                report_lines.append("")
        
        if insights.get('research_gaps'):
            report_lines.append("### Research Gaps Discovered")
            report_lines.append("")
            for i, gap in enumerate(insights['research_gaps'][:5], 1):
                if isinstance(gap, dict):
                    report_lines.append(f"{i}. **{gap.get('item', 'Gap')}**")
                    report_lines.append(f"   - {gap.get('details', 'No details available')}")
                else:
                    report_lines.append(f"{i}. {gap}")
                report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # Suggested Research Directions
        if research_directions:
            report_lines.append("## 🚀 Suggested Research Directions")
            report_lines.append("")
            report_lines.append("### High-Priority Projects")
            report_lines.append("")
            
            for i, project in enumerate(research_directions, 1):
                report_lines.append(f"{i}. **{project.get('title', 'Untitled Project')}**")
                report_lines.append(f"   - **Motivation:** {project.get('motivation', 'N/A')}")
                report_lines.append(f"   - **Approach:** {project.get('approach', 'N/A')}")
                report_lines.append(f"   - **Expected Contribution:** {project.get('expected_contribution', 'N/A')}")
                report_lines.append(f"   - **Required Resources:** {project.get('required_resources', 'N/A')}")
                report_lines.append(f"   - **Timeline:** {project.get('timeline', 'N/A')}")
                report_lines.append(f"   - **Difficulty:** {project.get('difficulty', 'N/A')}")
                report_lines.append("")
        
        # Emerging Themes
        if insights.get('emerging_themes'):
            report_lines.append("### Emerging Themes")
            report_lines.append("")
            for theme in insights['emerging_themes'][:5]:
                if isinstance(theme, dict):
                    report_lines.append(f"- **{theme.get('item', 'N/A')}**: {theme.get('details', '')}")
                else:
                    report_lines.append(f"- {theme}")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # Trend Visualization (if analysis data provided)
        if analysis_data:
            report_lines.append("## 📊 Trend Analysis")
            report_lines.append("")
            
            if 'temporal' in analysis_data:
                temporal = analysis_data['temporal']
                report_lines.append("### Publication Timeline")
                report_lines.append("")
                for year, count in temporal.get('by_year', {}).items():
                    report_lines.append(f"- **{year}**: {count} papers")
                report_lines.append("")
            
            if 'categories' in analysis_data:
                categories = analysis_data['categories']
                report_lines.append("### Category Distribution")
                report_lines.append("")
                for cat, count in list(categories.get('primary_categories', {}).items())[:5]:
                    report_lines.append(f"- **{cat}**: {count} papers")
                report_lines.append("")
        
        # Complete References
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## 📚 Complete References")
        report_lines.append("")
        
        for i, paper in enumerate(papers, 1):
            authors = self._format_authors(paper['authors'])
            year = paper['published'].year
            title = paper['title']
            arxiv_id = paper['id']
            url = paper['entry_url']
            
            report_lines.append(f"[{i}] {authors} ({year}). \"{title}\". *arXiv:{arxiv_id}*")
            report_lines.append(f"    🔗 {url}")
            report_lines.append("")
        
        # Reproducibility Notes
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## 🔧 Reproducibility Notes")
        report_lines.append("")
        report_lines.append(f"**Search Query Used:** `{query}`")
        
        if papers:
            start_date = min(p['published'] for p in papers).strftime('%Y-%m-%d')
            end_date = max(p['published'] for p in papers).strftime('%Y-%m-%d')
            report_lines.append(f"**Date Range:** {start_date} to {end_date}")
        
        report_lines.append(f"**Papers Retrieved:** {len(papers)}")
        report_lines.append("")
        report_lines.append("**To reproduce this search:**")
        report_lines.append("```python")
        report_lines.append("import arxiv")
        report_lines.append("search = arxiv.Search(")
        report_lines.append(f'    query="{query}",')
        report_lines.append(f"    max_results={len(papers)},")
        report_lines.append("    sort_by=arxiv.SortCriterion.SubmittedDate")
        report_lines.append(")")
        report_lines.append("client = arxiv.Client()")
        report_lines.append("results = list(client.results(search))")
        report_lines.append("```")
        report_lines.append("")
        
        # Footer
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("*Report generated by RESEARCH_AGENT v2.0*")
        report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _format_paper_section(self, paper: Dict, index: int) -> List[str]:
        """Format a single paper section."""
        lines = []
        
        lines.append(f"### [{index}] {paper['title']}")
        lines.append("")
        lines.append(f"**Authors:** {self._format_authors(paper['authors'])}")
        lines.append(f"**Published:** {paper['published'].strftime('%Y-%m-%d')} | **arXiv:** [{paper['id']}]({paper['entry_url']})")
        lines.append(f"**Categories:** {', '.join(paper['categories'][:3])}")
        lines.append("")
        
        # Fast summary
        if 'fast_summary' in paper:
            lines.append("**Summary:**")
            lines.append(paper['fast_summary'])
            lines.append("")
        
        # Deep analysis
        if 'deep_analysis' in paper:
            analysis = paper['deep_analysis']
            
            if analysis.get('contributions'):
                lines.append("**Key Contributions:**")
                for contrib in analysis['contributions'][:3]:
                    lines.append(f"- {contrib}")
                lines.append("")
            
            if analysis.get('methods'):
                methods_str = ', '.join(analysis['methods'][:3])
                lines.append(f"**Methods:** {methods_str}")
                lines.append("")
            
            if analysis.get('results'):
                lines.append(f"**Results:** {analysis['results'][0] if analysis['results'] else 'N/A'}")
                lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def _format_authors(self, authors: List[str], max_authors: int = 3) -> str:
        """Format author list."""
        if len(authors) <= max_authors:
            return ", ".join(authors)
        else:
            return f"{', '.join(authors[:max_authors])} et al."
    
    def generate_bibtex(self, papers: List[Dict]) -> str:
        """Generate BibTeX bibliography."""
        bibtex_entries = []
        
        for paper in papers:
            entry_id = paper['id'].replace('.', '_')
            authors_str = " and ".join(paper['authors'])
            year = paper['published'].year
            title = paper['title']
            
            entry = f"""@article{{{entry_id},
  author = {{{authors_str}}},
  title = {{{title}}},
  journal = {{arXiv preprint arXiv:{paper['id']}}},
  year = {{{year}}},
  url = {{{paper['entry_url']}}}
}}"""
            bibtex_entries.append(entry)
        
        return "\n\n".join(bibtex_entries)
    
    def generate_json(self, papers: List[Dict], insights: Dict, research_directions: List[Dict]) -> str:
        """Generate JSON export."""
        data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_papers': len(papers)
            },
            'papers': papers,
            'insights': insights,
            'research_directions': research_directions
        }
        
        # Convert datetime objects to strings
        for paper in data['papers']:
            paper['published'] = paper['published'].isoformat()
            paper['updated'] = paper['updated'].isoformat()
        
        return json.dumps(data, indent=2)
    
    def generate_comparison_report(self, comparison: Dict) -> str:
        """Generate comparison report for two topics."""
        lines = []
        
        topic1 = comparison['topic1']
        topic2 = comparison['topic2']
        
        lines.append(f"# 🆚 Comparative Analysis: {topic1} vs {topic2}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Paper counts
        lines.append("## 📊 Overview")
        lines.append("")
        lines.append("| Metric | " + topic1 + " | " + topic2 + " |")
        lines.append("|--------|" + "-" * len(topic1) + "|" + "-" * len(topic2) + "|")
        lines.append(f"| Papers Found | {comparison['paper_counts'][topic1]} | {comparison['paper_counts'][topic2]} |")
        lines.append("")
        
        # Temporal trends
        lines.append("## 📈 Temporal Trends")
        lines.append("")
        lines.append(f"### {topic1}")
        for year, count in comparison['temporal_trends'][topic1]['by_year'].items():
            lines.append(f"- **{year}**: {count} papers")
        lines.append("")
        
        lines.append(f"### {topic2}")
        for year, count in comparison['temporal_trends'][topic2]['by_year'].items():
            lines.append(f"- **{year}**: {count} papers")
        lines.append("")
        
        # Methodologies
        lines.append("## 🔬 Methodologies")
        lines.append("")
        
        methods1 = comparison['methodologies'][topic1]['method_distribution']
        methods2 = comparison['methodologies'][topic2]['method_distribution']
        
        lines.append("| Method | " + topic1 + " | " + topic2 + " |")
        lines.append("|--------|" + "-" * len(topic1) + "|" + "-" * len(topic2) + "|")
        
        all_methods = set(methods1.keys()) | set(methods2.keys())
        for method in sorted(all_methods):
            count1 = methods1.get(method, 0)
            count2 = methods2.get(method, 0)
            lines.append(f"| {method} | {count1} | {count2} |")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Comparison generated by RESEARCH_AGENT v2.0*")
        lines.append("")
        
        return "\n".join(lines)
    
    def save_report(self, content: str, filename: str, format_type: str = 'markdown') -> str:
        """Save report to file."""
        import os
        
        # Create reports directory if it doesn't exist
        save_path = self.output_config['save_path']
        os.makedirs(save_path, exist_ok=True)
        
        # Add extension based on format
        extensions = {
            'markdown': '.md',
            'bibtex': '.bib',
            'json': '.json',
            'latex': '.tex',
            'html': '.html'
        }
        
        ext = extensions.get(format_type, '.txt')
        if not filename.endswith(ext):
            filename = filename + ext
        
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
