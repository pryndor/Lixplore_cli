#!/usr/bin/env python3

"""
Profile management utilities for Lixplore - save and load export configurations
"""

import json
import os
from typing import Dict, List


# Profile storage location
PROFILES_DIR = os.path.expanduser("~/.lixplore")
PROFILES_FILE = os.path.join(PROFILES_DIR, "profiles.json")


def ensure_profiles_dir():
    """Create ~/.lixplore directory if it doesn't exist."""
    if not os.path.exists(PROFILES_DIR):
        os.makedirs(PROFILES_DIR)
        print(f"✓ Created profiles directory: {PROFILES_DIR}")


def load_profiles() -> Dict:
    """
    Load all saved profiles.

    Returns:
        Dictionary of profiles {profile_name: config_dict}
    """
    ensure_profiles_dir()

    if not os.path.exists(PROFILES_FILE):
        return {}

    try:
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load profiles: {e}")
        return {}


def save_profile(name: str, config: Dict) -> bool:
    """
    Save export profile.

    Args:
        name: Profile name
        config: Configuration dictionary

    Returns:
        True if saved successfully
    """
    ensure_profiles_dir()

    # Load existing profiles
    profiles = load_profiles()

    # Add or update profile
    profiles[name] = config

    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error: Could not save profile: {e}")
        return False


def load_profile(name: str) -> Dict:
    """
    Load export profile by name.

    Args:
        name: Profile name

    Returns:
        Configuration dictionary or None if not found
    """
    profiles = load_profiles()
    return profiles.get(name)


def list_profiles() -> List[str]:
    """
    List all saved profile names.

    Returns:
        List of profile names
    """
    profiles = load_profiles()
    return list(profiles.keys())


def delete_profile(name: str) -> bool:
    """
    Delete saved profile.

    Args:
        name: Profile name

    Returns:
        True if deleted successfully
    """
    profiles = load_profiles()

    if name not in profiles:
        print(f"Error: Profile '{name}' not found")
        return False

    del profiles[name]

    try:
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error: Could not delete profile: {e}")
        return False


def create_profile_from_args(args) -> Dict:
    """
    Create profile configuration from CLI arguments.

    Args:
        args: argparse.Namespace object

    Returns:
        Profile configuration dictionary
    """
    config = {}

    # Export settings
    if hasattr(args, 'export') and args.export:
        config['export_format'] = args.export

    if hasattr(args, 'export_fields') and args.export_fields:
        config['fields'] = args.export_fields

    if hasattr(args, 'citations') and args.citations:
        config['citation_style'] = args.citations

    if hasattr(args, 'zip') and args.zip:
        config['compress'] = True

    # Search/filter settings
    if hasattr(args, 'sort') and args.sort and args.sort != 'relevant':
        config['sort'] = args.sort

    if hasattr(args, 'deduplicate') and args.deduplicate:
        config['deduplicate'] = args.deduplicate

    if hasattr(args, 'dedup_threshold') and args.dedup_threshold != 0.85:
        config['dedup_threshold'] = args.dedup_threshold

    if hasattr(args, 'dedup_keep') and args.dedup_keep and args.dedup_keep != 'most_complete':
        config['dedup_keep'] = args.dedup_keep

    if hasattr(args, 'dedup_merge') and args.dedup_merge:
        config['dedup_merge'] = True

    # Enrichment settings (for future feature)
    if hasattr(args, 'enrich') and args.enrich:
        config['enrich'] = args.enrich if isinstance(args.enrich, list) else ['all']

    return config


def apply_profile_to_args(args, profile: Dict):
    """
    Apply profile configuration to argparse arguments.

    Args:
        args: argparse.Namespace object
        profile: Profile configuration dictionary
    """
    # Export settings
    if 'export_format' in profile and not args.export:
        args.export = profile['export_format']

    if 'fields' in profile and not args.export_fields:
        args.export_fields = profile['fields']

    if 'citation_style' in profile and not args.citations:
        args.citations = profile['citation_style']

    if 'compress' in profile and not args.zip:
        args.zip = profile['compress']

    # Search/filter settings
    if 'sort' in profile and args.sort == 'relevant':
        args.sort = profile['sort']

    if 'deduplicate' in profile and not args.deduplicate:
        args.deduplicate = profile['deduplicate']

    if 'dedup_threshold' in profile and args.dedup_threshold == 0.85:
        args.dedup_threshold = profile['dedup_threshold']

    if 'dedup_keep' in profile and args.dedup_keep == 'most_complete':
        args.dedup_keep = profile['dedup_keep']

    if 'dedup_merge' in profile and not args.dedup_merge:
        args.dedup_merge = profile['dedup_merge']

    # Enrichment settings (for future feature)
    if 'enrich' in profile and hasattr(args, 'enrich') and not args.enrich:
        args.enrich = profile['enrich']

    return args
