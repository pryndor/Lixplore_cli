#!/usr/bin/env python3
"""
Reference Manager Integration

Integrates with:
- Zotero (direct API)
- Mendeley (via RIS export)
- EndNote (via RIS export)

Provides one-click adding of articles to reference libraries.
"""

import os
import requests
import json
from typing import List, Dict, Optional


# Configuration file for API keys
CONFIG_FILE = os.path.expanduser("~/.lixplore/refman_config.json")


def load_config() -> Dict:
    """Load reference manager configuration."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}


def save_config(config: Dict):
    """Save reference manager configuration."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def configure_zotero(api_key: str, user_id: str, library_type: str = "user"):
    """
    Configure Zotero API access.

    Args:
        api_key: Zotero API key (get from https://www.zotero.org/settings/keys)
        user_id: Zotero user ID or group ID
        library_type: "user" or "group"
    """
    config = load_config()
    config['zotero'] = {
        'api_key': api_key,
        'user_id': user_id,
        'library_type': library_type
    }
    save_config(config)
    print(f"✓ Zotero configured for {library_type} library (ID: {user_id})")


def article_to_zotero_item(article: Dict) -> Dict:
    """
    Convert article dictionary to Zotero API format.

    Args:
        article: Article dictionary

    Returns:
        Zotero item dictionary
    """
    # Zotero item format
    item = {
        "itemType": "journalArticle",
        "title": article.get('title', ''),
        "abstractNote": article.get('abstract', ''),
        "publicationTitle": article.get('journal', ''),
        "DOI": article.get('doi', ''),
        "url": article.get('url', ''),
        "date": str(article.get('year', '')),
        "creators": []
    }

    # Add authors
    authors = article.get('authors')
    if authors:
        if isinstance(authors, list):
            for author in authors:
                item['creators'].append({
                    "creatorType": "author",
                    "name": str(author)
                })
        elif isinstance(authors, str):
            # Split by common delimiters
            for delimiter in [',', ';', ' and ']:
                if delimiter in authors:
                    author_list = authors.split(delimiter)
                    for author in author_list:
                        if author.strip():
                            item['creators'].append({
                                "creatorType": "author",
                                "name": author.strip()
                            })
                    break
            else:
                # Single author
                item['creators'].append({
                    "creatorType": "author",
                    "name": authors.strip()
                })

    # Add tags from source
    if article.get('source'):
        item['tags'] = [{"tag": f"source:{article['source']}"}]

    return item


def add_to_zotero(articles: List[Dict], collection_key: Optional[str] = None) -> Dict[str, any]:
    """
    Add articles to Zotero library.

    Args:
        articles: List of article dictionaries
        collection_key: Optional Zotero collection key to add items to

    Returns:
        Dictionary with success/failure counts
    """
    config = load_config()
    zotero_config = config.get('zotero')

    if not zotero_config:
        return {
            'success': 0,
            'failed': len(articles),
            'error': 'Zotero not configured. Run: lixplore --configure-zotero <api_key> <user_id>'
        }

    api_key = zotero_config.get('api_key')
    user_id = zotero_config.get('user_id')
    library_type = zotero_config.get('library_type', 'user')

    if not api_key or not user_id:
        return {
            'success': 0,
            'failed': len(articles),
            'error': 'Zotero configuration incomplete'
        }

    # Zotero API endpoint
    base_url = f"https://api.zotero.org/{library_type}s/{user_id}/items"

    headers = {
        'Zotero-API-Key': api_key,
        'Content-Type': 'application/json',
        'Zotero-API-Version': '3'
    }

    success_count = 0
    failed_count = 0
    failed_titles = []

    print(f"\n📚 Adding {len(articles)} article(s) to Zotero...")

    for i, article in enumerate(articles, 1):
        try:
            # Convert to Zotero format
            zotero_item = article_to_zotero_item(article)

            # Add to collection if specified
            if collection_key:
                zotero_item['collections'] = [collection_key]

            # Send to Zotero API
            response = requests.post(
                base_url,
                headers=headers,
                json=[zotero_item],
                timeout=30
            )

            if response.status_code in [200, 201]:
                print(f"[{i}/{len(articles)}] ✓ {article.get('title', 'Unknown')[:60]}...")
                success_count += 1
            else:
                print(f"[{i}/{len(articles)}] ✗ {article.get('title', 'Unknown')[:60]}... (HTTP {response.status_code})")
                failed_count += 1
                failed_titles.append(article.get('title', 'Unknown'))

        except Exception as e:
            print(f"[{i}/{len(articles)}] ✗ {article.get('title', 'Unknown')[:60]}... (Error: {str(e)})")
            failed_count += 1
            failed_titles.append(article.get('title', 'Unknown'))

    print(f"\n✓ Zotero import complete: {success_count} successful, {failed_count} failed")

    return {
        'success': success_count,
        'failed': failed_count,
        'failed_titles': failed_titles
    }


def export_for_mendeley(articles: List[Dict], output_file: Optional[str] = None) -> str:
    """
    Export articles in RIS format for Mendeley import.

    Mendeley doesn't have a public API for direct import, so we export to RIS
    which can be imported into Mendeley Desktop.

    Args:
        articles: List of article dictionaries
        output_file: Optional output filename

    Returns:
        Path to exported file
    """
    from lixplore.utils.export import export_to_ris

    if not output_file:
        output_file = os.path.expanduser("~/lixplore_mendeley_import.ris")

    # Export to RIS format
    export_path = export_to_ris(articles, output_file)

    print(f"\n✓ Exported {len(articles)} article(s) for Mendeley")
    print(f"📁 File: {export_path}")
    print(f"\nℹ️  Import to Mendeley:")
    print(f"   1. Open Mendeley Desktop")
    print(f"   2. File → Import → RIS")
    print(f"   3. Select: {export_path}")

    return export_path


def show_zotero_collections() -> List[Dict]:
    """
    List Zotero collections (for selecting where to add items).

    Returns:
        List of collection dictionaries
    """
    config = load_config()
    zotero_config = config.get('zotero')

    if not zotero_config:
        print("Zotero not configured. Run: lixplore --configure-zotero <api_key> <user_id>")
        return []

    api_key = zotero_config.get('api_key')
    user_id = zotero_config.get('user_id')
    library_type = zotero_config.get('library_type', 'user')

    # Zotero collections endpoint
    url = f"https://api.zotero.org/{library_type}s/{user_id}/collections"

    headers = {
        'Zotero-API-Key': api_key,
        'Zotero-API-Version': '3'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        collections = response.json()

        if collections:
            print("\nZotero Collections:")
            print("=" * 60)
            for col in collections:
                data = col.get('data', {})
                name = data.get('name', 'Unknown')
                key = data.get('key', '')
                num_items = data.get('meta', {}).get('numItems', 0)
                print(f"  • {name} ({num_items} items)")
                print(f"    Key: {key}")
        else:
            print("\nNo collections found in your Zotero library.")

        return collections

    except Exception as e:
        print(f"Error fetching Zotero collections: {e}")
        return []


if __name__ == "__main__":
    # Test reference manager integration
    test_articles = [
        {
            'title': 'Test Article',
            'authors': ['Smith J', 'Doe A'],
            'journal': 'Nature',
            'year': 2024,
            'doi': '10.1234/test',
            'abstract': 'Test abstract',
            'source': 'PubMed'
        }
    ]

    # Test Mendeley export
    export_for_mendeley(test_articles)
