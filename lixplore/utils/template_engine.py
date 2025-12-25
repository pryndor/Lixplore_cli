#!/usr/bin/env python3

"""
Template engine for Lixplore - apply predefined export templates
"""

import json
import os
from typing import Dict, List


# Template directory paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILTIN_TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "lixplore", "templates")
USER_TEMPLATES_DIR = os.path.expanduser("~/.lixplore/templates")


def ensure_user_templates_dir():
    """Create user templates directory if it doesn't exist."""
    if not os.path.exists(USER_TEMPLATES_DIR):
        os.makedirs(USER_TEMPLATES_DIR)


def load_template(template_name: str) -> Dict:
    """
    Load export template configuration.

    Args:
        template_name: Template name (e.g., 'nature', 'science')

    Returns:
        Template configuration dictionary
    """
    # Try user templates first
    ensure_user_templates_dir()
    user_template_path = os.path.join(USER_TEMPLATES_DIR, f"{template_name}.json")
    if os.path.exists(user_template_path):
        try:
            with open(user_template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Try built-in templates
    builtin_template_path = os.path.join(BUILTIN_TEMPLATES_DIR, f"{template_name}.json")
    if os.path.exists(builtin_template_path):
        try:
            with open(builtin_template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    return None


def apply_template(results: List[Dict], template: Dict) -> List[Dict]:
    """
    Apply template formatting to results.

    Args:
        results: List of article dictionaries
        template: Template configuration

    Returns:
        Formatted results according to template
    """
    if not results or not template:
        return results

    formatted_results = []

    # Extract template settings
    fields = template.get('fields', None)
    field_order = template.get('field_order', None)
    max_authors = template.get('max_authors', None)
    abbreviate_journal = template.get('abbreviate_journal', False)
    include_abstract = template.get('include_abstract', True)

    for article in results:
        formatted = {}

        # Apply field filtering if specified
        if fields:
            for field in fields:
                formatted[field] = article.get(field)
        else:
            formatted = article.copy()

        # Limit authors if specified
        if max_authors and 'authors' in formatted:
            authors = formatted['authors']
            if isinstance(authors, list) and len(authors) > max_authors:
                formatted['authors'] = authors[:max_authors] + ['et al.']

        # Remove abstract if not included
        if not include_abstract and 'abstract' in formatted:
            del formatted['abstract']

        # Abbreviate journal if requested (simple abbreviation)
        if abbreviate_journal and 'journal' in formatted:
            journal = formatted['journal']
            if journal:
                # Simple abbreviation: keep first letter of each word
                words = journal.split()
                abbreviated = '. '.join([w[0].upper() for w in words if w]) + '.'
                formatted['journal'] = abbreviated

        formatted_results.append(formatted)

    # Apply field ordering if specified
    if field_order:
        ordered_results = []
        for article in formatted_results:
            ordered = {}
            for field in field_order:
                if field in article:
                    ordered[field] = article[field]
            # Add any remaining fields not in order
            for field, value in article.items():
                if field not in ordered:
                    ordered[field] = value
            ordered_results.append(ordered)
        return ordered_results

    return formatted_results


def list_templates() -> List[str]:
    """
    List all available templates (built-in and user).

    Returns:
        List of template names
    """
    templates = []

    # List built-in templates
    if os.path.exists(BUILTIN_TEMPLATES_DIR):
        for filename in os.listdir(BUILTIN_TEMPLATES_DIR):
            if filename.endswith('.json'):
                templates.append(filename[:-5])  # Remove .json extension

    # List user templates
    ensure_user_templates_dir()
    if os.path.exists(USER_TEMPLATES_DIR):
        for filename in os.listdir(USER_TEMPLATES_DIR):
            if filename.endswith('.json'):
                name = filename[:-5]
                if name not in templates:
                    templates.append(name + ' (user)')

    return sorted(templates)


def apply_template_to_args(args, template: Dict):
    """
    Apply template configuration to argparse arguments.

    Args:
        args: argparse.Namespace object
        template: Template configuration dictionary
    """
    # Apply export format
    if 'format' in template and not args.export:
        args.export = template['format']

    # Apply citation style
    if 'citation_style' in template and not args.citation:
        args.citation = template['citation_style']

    # Apply field selection
    if 'fields' in template and not args.export_fields:
        args.export_fields = template['fields']

    # Apply sorting
    if 'sort' in template and args.sort == 'relevant':
        args.sort = template['sort']

    # Apply deduplication
    if 'deduplicate' in template and not args.deduplicate:
        args.deduplicate = template['deduplicate']

    # Apply enrichment
    if 'enrich' in template and hasattr(args, 'enrich') and args.enrich is None:
        args.enrich = template['enrich'] if isinstance(template['enrich'], list) else ['all']

    return args
