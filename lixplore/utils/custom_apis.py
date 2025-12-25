#!/usr/bin/env python3
"""
Custom API Integration System

Allows users to define their own API sources via configuration files.
Supports Springer, BASE, and any other API with minimal setup.
"""

import json
import os
import requests
from typing import List, Dict, Optional

# Directory for custom API configurations
CUSTOM_API_DIR = os.path.expanduser("~/.lixplore/apis")
CUSTOM_API_CONFIG = os.path.expanduser("~/.lixplore/custom_apis.json")


def ensure_api_directory():
    """Create API configuration directory if it doesn't exist."""
    if not os.path.exists(CUSTOM_API_DIR):
        os.makedirs(CUSTOM_API_DIR, exist_ok=True)


def load_custom_api_config(api_name: str) -> Optional[Dict]:
    """
    Load configuration for a custom API.

    Args:
        api_name: Name of the custom API to load

    Returns:
        API configuration dictionary or None if not found
    """
    ensure_api_directory()

    # Try loading from individual file first
    api_file = os.path.join(CUSTOM_API_DIR, f"{api_name}.json")
    if os.path.exists(api_file):
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading custom API config '{api_name}': {e}")
            return None

    # Try loading from central config file
    if os.path.exists(CUSTOM_API_CONFIG):
        try:
            with open(CUSTOM_API_CONFIG, 'r', encoding='utf-8') as f:
                configs = json.load(f)
                return configs.get(api_name)
        except Exception as e:
            print(f"Error loading custom APIs config: {e}")
            return None

    return None


def list_custom_apis() -> List[str]:
    """
    List all available custom APIs.

    Returns:
        List of custom API names
    """
    ensure_api_directory()
    apis = []

    # Get APIs from individual files
    if os.path.exists(CUSTOM_API_DIR):
        for filename in os.listdir(CUSTOM_API_DIR):
            if filename.endswith('.json'):
                apis.append(filename[:-5])  # Remove .json extension

    # Get APIs from central config
    if os.path.exists(CUSTOM_API_CONFIG):
        try:
            with open(CUSTOM_API_CONFIG, 'r', encoding='utf-8') as f:
                configs = json.load(f)
                apis.extend(list(configs.keys()))
        except:
            pass

    return sorted(set(apis))


def create_example_configs():
    """Create example API configuration files for Springer and BASE."""
    ensure_api_directory()

    # Example: Springer API configuration
    springer_config = {
        "name": "Springer",
        "description": "Springer Nature API for scientific articles",
        "base_url": "http://api.springernature.com/meta/v2/json",
        "requires_auth": True,
        "auth_type": "api_key",
        "auth_param": "api_key",  # Parameter name in URL
        "api_key": "YOUR_SPRINGER_API_KEY_HERE",
        "query_param": "q",
        "limit_param": "p",
        "response_path": "records",  # Path to results array in JSON response
        "field_mapping": {
            "title": "title",
            "authors": "creators[*].creator",  # JSONPath-style
            "abstract": "abstract",
            "doi": "doi",
            "year": "publicationDate",
            "journal": "publicationName",
            "url": "url[0].value"
        }
    }

    # Example: BASE (Bielefeld Academic Search Engine) configuration
    base_config = {
        "name": "BASE",
        "description": "Bielefeld Academic Search Engine",
        "base_url": "https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi",
        "requires_auth": False,
        "query_param": "query",
        "limit_param": "hits",
        "response_format": "xml",  # or "json"
        "response_path": "//result/doc",  # XPath for XML
        "field_mapping": {
            "title": "dctitle",
            "authors": "dcauthor",
            "abstract": "dcdescription",
            "doi": "dcdoi",
            "year": "dcyear",
            "url": "dclink"
        }
    }

    # Save examples to central config file
    examples = {
        "springer": springer_config,
        "base": base_config
    }

    example_file = os.path.join(CUSTOM_API_DIR, "EXAMPLES.json")
    with open(example_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)

    print(f"✓ Example API configurations created at: {example_file}")
    print(f"  - Springer: Requires API key from https://dev.springernature.com/")
    print(f"  - BASE: No authentication required")
    print(f"\nTo use: Copy the config to {CUSTOM_API_CONFIG} or create individual files.")


def extract_field(data: Dict, path: str) -> Optional[str]:
    """
    Extract field from nested dictionary using simple path notation.

    Args:
        data: Dictionary to extract from
        path: Field path (e.g., "title" or "metadata.title")

    Returns:
        Extracted value or None
    """
    if not path or not data:
        return None

    parts = path.split('.')
    current = data

    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            idx = int(part)
            current = current[idx] if 0 <= idx < len(current) else None
        else:
            return None

        if current is None:
            return None

    return str(current) if current is not None else None


def call_custom_api(api_name: str, query: str, limit: int = 10) -> List[Dict]:
    """
    Call a custom API and return standardized results.

    Args:
        api_name: Name of the custom API
        query: Search query
        limit: Maximum number of results

    Returns:
        List of article dictionaries in standard format
    """
    config = load_custom_api_config(api_name)
    if not config:
        print(f"Error: Custom API '{api_name}' not found.")
        print(f"Available APIs: {', '.join(list_custom_apis())}")
        print(f"\nRun 'lixplore --create-api-examples' to create example configurations.")
        return []

    # Build request URL
    base_url = config.get('base_url')
    if not base_url:
        print(f"Error: Custom API '{api_name}' missing 'base_url' in configuration.")
        return []

    params = {}
    params[config.get('query_param', 'q')] = query
    params[config.get('limit_param', 'limit')] = limit

    # Add authentication if required
    if config.get('requires_auth'):
        auth_type = config.get('auth_type', 'api_key')
        if auth_type == 'api_key':
            auth_param = config.get('auth_param', 'api_key')
            api_key = config.get('api_key', '')
            if not api_key or api_key == 'YOUR_SPRINGER_API_KEY_HERE':
                print(f"Error: API key not configured for '{api_name}'.")
                print(f"Edit configuration file to add your API key.")
                return []
            params[auth_param] = api_key

    # Make request
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()

        # Parse response
        response_format = config.get('response_format', 'json')
        if response_format == 'json':
            data = response.json()
        else:
            print(f"Error: Unsupported response format '{response_format}' for '{api_name}'.")
            return []

        # Extract results array
        response_path = config.get('response_path', 'results')
        results_raw = extract_field(data, response_path)

        if not isinstance(results_raw, list):
            # Try to get it as a list
            if response_path in data:
                results_raw = data[response_path]
            else:
                results_raw = data

        if not isinstance(results_raw, list):
            print(f"Error: Could not find results array in response from '{api_name}'.")
            return []

        # Convert to standard format
        field_mapping = config.get('field_mapping', {})
        standardized_results = []

        for item in results_raw:
            article = {
                'title': extract_field(item, field_mapping.get('title', 'title')),
                'authors': extract_field(item, field_mapping.get('authors', 'authors')),
                'abstract': extract_field(item, field_mapping.get('abstract', 'abstract')),
                'doi': extract_field(item, field_mapping.get('doi', 'doi')),
                'year': extract_field(item, field_mapping.get('year', 'year')),
                'journal': extract_field(item, field_mapping.get('journal', 'journal')),
                'url': extract_field(item, field_mapping.get('url', 'url')),
                'source': config.get('name', api_name)
            }

            # Handle authors (might be array or string)
            if isinstance(article['authors'], str):
                # Already a string, good
                pass
            elif isinstance(article['authors'], list):
                article['authors'] = ', '.join(str(a) for a in article['authors'] if a)
            else:
                article['authors'] = None

            standardized_results.append(article)

        return standardized_results

    except requests.RequestException as e:
        print(f"Error calling custom API '{api_name}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error with custom API '{api_name}': {e}")
        return []


if __name__ == "__main__":
    # Create example configurations when run directly
    create_example_configs()
