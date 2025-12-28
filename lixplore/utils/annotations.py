#!/usr/bin/env python3
"""
Annotation system for Lixplore articles.

Allows users to:
- Rate articles (1-5 stars)
- Add comments and notes
- Tag articles
- Mark read status
- Set priority levels
- Search and filter annotations
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

ANNOTATIONS_FILE = os.path.expanduser("~/.lixplore_annotations.json")


class AnnotationManager:
    """Manage article annotations and metadata."""

    def __init__(self):
        self.annotations = self._load_annotations()

    def _load_annotations(self) -> Dict:
        """Load existing annotations from file."""
        if os.path.exists(ANNOTATIONS_FILE):
            try:
                with open(ANNOTATIONS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_annotations(self):
        """Save annotations to file."""
        try:
            with open(ANNOTATIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.annotations, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save annotations: {e}")

    def _get_article_id(self, article: Dict) -> str:
        """Get unique identifier for article (DOI or title hash)."""
        doi = article.get('doi')
        if doi:
            return f"doi:{doi}"

        title = article.get('title', '')
        if title:
            return f"title:{hash(title)}"

        return f"unknown:{hash(str(article))}"

    def annotate(self, article: Dict, comment: str = None, rating: int = None,
                 tags: List[str] = None, read_status: str = None,
                 priority: str = None) -> str:
        """
        Add or update annotation for an article.

        Args:
            article: Article dictionary
            comment: Text comment/note
            rating: Rating (1-5)
            tags: List of tags
            read_status: 'unread', 'reading', 'read'
            priority: 'low', 'medium', 'high'

        Returns:
            Article ID
        """
        article_id = self._get_article_id(article)

        # Initialize annotation if doesn't exist
        if article_id not in self.annotations:
            self.annotations[article_id] = {
                'article_info': {
                    'title': article.get('title', 'No title'),
                    'authors': article.get('authors', []),
                    'year': article.get('year'),
                    'doi': article.get('doi'),
                    'source': article.get('source'),
                },
                'comments': [],
                'tags': [],
                'rating': None,
                'read_status': 'unread',
                'priority': 'medium',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

        # Update annotation
        annotation = self.annotations[article_id]

        if comment:
            annotation['comments'].append({
                'timestamp': datetime.now().isoformat(),
                'text': comment
            })

        if rating is not None:
            if 1 <= rating <= 5:
                annotation['rating'] = rating
            else:
                print(f"Warning: Rating must be 1-5, got {rating}")

        if tags:
            existing_tags = set(annotation['tags'])
            existing_tags.update(tags)
            annotation['tags'] = sorted(list(existing_tags))

        if read_status:
            if read_status in ['unread', 'reading', 'read']:
                annotation['read_status'] = read_status
            else:
                print(f"Warning: Invalid read_status '{read_status}'")

        if priority:
            if priority in ['low', 'medium', 'high']:
                annotation['priority'] = priority
            else:
                print(f"Warning: Invalid priority '{priority}'")

        annotation['updated_at'] = datetime.now().isoformat()

        self._save_annotations()
        return article_id

    def get_annotation(self, article_id: str) -> Optional[Dict]:
        """Get annotation for an article."""
        return self.annotations.get(article_id)

    def get_annotation_for_article(self, article: Dict) -> Optional[Dict]:
        """Get annotation using article object."""
        article_id = self._get_article_id(article)
        return self.get_annotation(article_id)

    def remove_annotation(self, article_id: str) -> bool:
        """Remove annotation for an article."""
        if article_id in self.annotations:
            del self.annotations[article_id]
            self._save_annotations()
            return True
        return False

    def list_all(self, filter_params: Dict = None) -> List[Dict]:
        """
        List all annotated articles with optional filtering.

        Args:
            filter_params: {
                'min_rating': int,
                'max_rating': int,
                'tags': List[str],
                'read_status': str,
                'priority': str,
                'has_comments': bool
            }

        Returns:
            List of annotations
        """
        results = []

        for article_id, annotation in self.annotations.items():
            # Apply filters
            if filter_params:
                if 'min_rating' in filter_params:
                    if not annotation.get('rating') or annotation['rating'] < filter_params['min_rating']:
                        continue

                if 'max_rating' in filter_params:
                    if not annotation.get('rating') or annotation['rating'] > filter_params['max_rating']:
                        continue

                if 'tags' in filter_params:
                    required_tags = filter_params['tags']
                    if not any(tag in annotation.get('tags', []) for tag in required_tags):
                        continue

                if 'read_status' in filter_params:
                    if annotation.get('read_status') != filter_params['read_status']:
                        continue

                if 'priority' in filter_params:
                    if annotation.get('priority') != filter_params['priority']:
                        continue

                if 'has_comments' in filter_params:
                    has_comments = len(annotation.get('comments', [])) > 0
                    if has_comments != filter_params['has_comments']:
                        continue

            results.append({
                'article_id': article_id,
                'annotation': annotation
            })

        return results

    def search_annotations(self, query: str) -> List[Dict]:
        """
        Search annotations by keyword in comments, tags, or title.

        Args:
            query: Search query string

        Returns:
            List of matching annotations
        """
        results = []
        query_lower = query.lower()

        for article_id, annotation in self.annotations.items():
            # Search in title
            title = annotation.get('article_info', {}).get('title', '')
            if query_lower in title.lower():
                results.append({
                    'article_id': article_id,
                    'annotation': annotation,
                    'match_type': 'title',
                    'match_text': title
                })
                continue

            # Search in comments
            for comment in annotation.get('comments', []):
                if query_lower in comment['text'].lower():
                    results.append({
                        'article_id': article_id,
                        'annotation': annotation,
                        'match_type': 'comment',
                        'match_text': comment['text']
                    })
                    break

            # Search in tags
            if any(query_lower in tag.lower() for tag in annotation.get('tags', [])):
                results.append({
                    'article_id': article_id,
                    'annotation': annotation,
                    'match_type': 'tag',
                    'match_text': ', '.join(annotation['tags'])
                })

        return results

    def export_annotations(self, format: str = 'markdown', output_file: str = None) -> str:
        """
        Export all annotations to a file.

        Args:
            format: 'markdown', 'json', 'csv'
            output_file: Output file path (optional)

        Returns:
            Export file path
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"lixplore_annotations_{timestamp}.{format if format != 'markdown' else 'md'}"

        if format == 'markdown':
            return self._export_markdown(output_file)
        elif format == 'json':
            return self._export_json(output_file)
        elif format == 'csv':
            return self._export_csv(output_file)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_markdown(self, output_file: str) -> str:
        """Export annotations as Markdown."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Lixplore Annotations\n\n")
            f.write(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"**Total Annotated Articles:** {len(self.annotations)}\n\n")
            f.write("---\n\n")

            for i, (article_id, annotation) in enumerate(self.annotations.items(), 1):
                info = annotation.get('article_info', {})

                f.write(f"## {i}. {info.get('title', 'No title')}\n\n")

                # Metadata
                authors = info.get('authors', [])
                if authors:
                    f.write(f"**Authors:** {', '.join(authors[:3])}")
                    if len(authors) > 3:
                        f.write(f" *et al.*")
                    f.write("\n\n")

                if info.get('year'):
                    f.write(f"**Year:** {info['year']}\n\n")

                if info.get('doi'):
                    f.write(f"**DOI:** {info['doi']}\n\n")

                # Rating
                if annotation.get('rating'):
                    stars = '' * annotation['rating']
                    f.write(f"**Rating:** {stars} ({annotation['rating']}/5)\n\n")

                # Tags
                if annotation.get('tags'):
                    tags_str = ' '.join([f"`{tag}`" for tag in annotation['tags']])
                    f.write(f"**Tags:** {tags_str}\n\n")

                # Status
                f.write(f"**Status:** {annotation.get('read_status', 'unread').title()}")
                f.write(f" | **Priority:** {annotation.get('priority', 'medium').title()}\n\n")

                # Comments
                if annotation.get('comments'):
                    f.write("**Notes:**\n\n")
                    for comment in annotation['comments']:
                        timestamp = comment['timestamp'].split('T')[0]
                        f.write(f"- *{timestamp}:* {comment['text']}\n")
                    f.write("\n")

                f.write("---\n\n")

        return output_file

    def _export_json(self, output_file: str) -> str:
        """Export annotations as JSON."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.annotations, f, indent=2, ensure_ascii=False)
        return output_file

    def _export_csv(self, output_file: str) -> str:
        """Export annotations as CSV."""
        import csv

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Article ID', 'Title', 'Authors', 'Year', 'DOI',
                'Rating', 'Tags', 'Read Status', 'Priority',
                'Comments Count', 'Latest Comment', 'Created', 'Updated'
            ])

            # Data
            for article_id, annotation in self.annotations.items():
                info = annotation.get('article_info', {})
                comments = annotation.get('comments', [])

                writer.writerow([
                    article_id,
                    info.get('title', ''),
                    '; '.join(info.get('authors', [])),
                    info.get('year', ''),
                    info.get('doi', ''),
                    annotation.get('rating', ''),
                    '; '.join(annotation.get('tags', [])),
                    annotation.get('read_status', ''),
                    annotation.get('priority', ''),
                    len(comments),
                    comments[-1]['text'] if comments else '',
                    annotation.get('created_at', ''),
                    annotation.get('updated_at', '')
                ])

        return output_file

    def get_statistics(self) -> Dict:
        """Get statistics about annotations."""
        total = len(self.annotations)

        if total == 0:
            return {
                'total': 0,
                'by_rating': {},
                'by_status': {},
                'by_priority': {},
                'with_comments': 0,
                'total_comments': 0,
                'total_tags': 0
            }

        by_rating = {}
        by_status = {}
        by_priority = {}
        with_comments = 0
        total_comments = 0
        all_tags = set()

        for annotation in self.annotations.values():
            # Rating stats
            rating = annotation.get('rating')
            if rating:
                by_rating[rating] = by_rating.get(rating, 0) + 1

            # Status stats
            status = annotation.get('read_status', 'unread')
            by_status[status] = by_status.get(status, 0) + 1

            # Priority stats
            priority = annotation.get('priority', 'medium')
            by_priority[priority] = by_priority.get(priority, 0) + 1

            # Comment stats
            comments = annotation.get('comments', [])
            if comments:
                with_comments += 1
                total_comments += len(comments)

            # Tag stats
            all_tags.update(annotation.get('tags', []))

        return {
            'total': total,
            'by_rating': by_rating,
            'by_status': by_status,
            'by_priority': by_priority,
            'with_comments': with_comments,
            'total_comments': total_comments,
            'total_tags': len(all_tags),
            'unique_tags': sorted(list(all_tags))
        }


def display_annotation(annotation: Dict, article_id: str = None):
    """Display a single annotation in a formatted way."""
    info = annotation.get('article_info', {})

    print("\n" + "="*80)
    print(f"ANNOTATION: {info.get('title', 'No title')}")
    print("="*80)

    # Article info
    authors = info.get('authors', [])
    if authors:
        print(f"Authors: {', '.join(authors[:3])}", end='')
        if len(authors) > 3:
            print(f" et al. ({len(authors)} total)")
        else:
            print()

    if info.get('year'):
        print(f"Year: {info['year']}")

    if info.get('doi'):
        print(f"DOI: {info['doi']}")

    if info.get('source'):
        print(f"Source: {info['source']}")

    print()

    # Annotation details
    if annotation.get('rating'):
        stars = '' * annotation['rating']
        print(f"Rating: {stars} ({annotation['rating']}/5)")

    if annotation.get('tags'):
        print(f"Tags: {', '.join(annotation['tags'])}")

    print(f"Read Status: {annotation.get('read_status', 'unread').title()}")
    print(f"Priority: {annotation.get('priority', 'medium').title()}")

    # Comments
    comments = annotation.get('comments', [])
    if comments:
        print(f"\nComments ({len(comments)}):")
        for i, comment in enumerate(comments, 1):
            timestamp = comment['timestamp'].split('T')
            date = timestamp[0]
            time = timestamp[1].split('.')[0] if len(timestamp) > 1 else ''
            print(f"  [{i}] {date} {time}")
            print(f"      {comment['text']}")

    # Timestamps
    print(f"\nCreated: {annotation.get('created_at', 'Unknown')}")
    print(f"Updated: {annotation.get('updated_at', 'Unknown')}")

    if article_id:
        print(f"\nArticle ID: {article_id}")

    print("="*80 + "\n")
