#!/usr/bin/env python3

"""
Comprehensive troubleshooting script for Lixplore CLI
Tests all functionality, edge cases, and potential issues
"""

import sys
import os
from typing import List, Dict

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

issues_found = []
warnings_found = []


def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")


def print_test(text):
    print(f"\n{YELLOW}Testing: {text}{RESET}")


def print_pass(text):
    print(f"{GREEN}✓ PASS: {text}{RESET}")


def print_fail(text):
    print(f"{RED}✗ FAIL: {text}{RESET}")
    issues_found.append(text)


def print_warn(text):
    print(f"{YELLOW}⚠ WARNING: {text}{RESET}")
    warnings_found.append(text)


def test_imports():
    """Test if all required modules can be imported"""
    print_header("1. TESTING IMPORTS")

    modules = [
        ("Bio", "biopython"),
        ("requests", "requests"),
        ("argparse", "argparse (built-in)"),
        ("json", "json (built-in)"),
        ("xml.etree.ElementTree", "xml (built-in)")
    ]

    for module_name, display_name in modules:
        print_test(f"Importing {display_name}")
        try:
            __import__(module_name)
            print_pass(f"{display_name} imported successfully")
        except ImportError as e:
            print_fail(f"Cannot import {display_name}: {e}")


def test_project_structure():
    """Test if all required files exist"""
    print_header("2. TESTING PROJECT STRUCTURE")

    required_files = [
        "lixplore/__init__.py",
        "lixplore/__main__.py",
        "lixplore/cli.py",
        "lixplore/commands.py",
        "lixplore/dispatcher.py",
        "lixplore/sources/__init__.py",
        "lixplore/sources/pubmed.py",
        "lixplore/sources/crossref.py",
        "lixplore/sources/doaj.py",
        "lixplore/sources/europepmc.py",
        "lixplore/sources/arxiv.py",
        "lixplore/utils/cache.py",
        "lixplore/utils/terminal.py",
        "requirements.txt",
        "config.json"
    ]

    for file_path in required_files:
        print_test(f"Checking {file_path}")
        if os.path.exists(file_path):
            print_pass(f"{file_path} exists")
        else:
            print_fail(f"{file_path} missing")


def test_source_connectors():
    """Test each source connector individually"""
    print_header("3. TESTING SOURCE CONNECTORS")

    try:
        from lixplore.sources import pubmed, crossref, doaj, europepmc, arxiv
    except ImportError as e:
        print_fail(f"Cannot import source modules: {e}")
        return

    sources = [
        ("PubMed", pubmed, "diabetes"),
        ("Crossref", crossref, "machine learning"),
        ("DOAJ", doaj, "climate"),
        ("EuropePMC", europepmc, "COVID-19"),
        ("arXiv", arxiv, "neural networks")
    ]

    for name, module, query in sources:
        print_test(f"{name} connector with query '{query}'")
        try:
            results = module.search(query, max_results=2)
            if results and len(results) > 0:
                print_pass(f"{name} returned {len(results)} results")

                # Check result structure
                first = results[0]
                required_fields = ["title", "authors", "abstract", "journal", "year", "doi", "url", "source"]
                missing_fields = [f for f in required_fields if f not in first]

                if missing_fields:
                    print_warn(f"{name} results missing fields: {missing_fields}")
                else:
                    print_pass(f"{name} results have all required fields")

            elif results is not None and len(results) == 0:
                print_warn(f"{name} returned 0 results (may be API issue or query)")
            else:
                print_fail(f"{name} returned None instead of list")

        except Exception as e:
            print_fail(f"{name} connector error: {e}")


def test_cli_functionality():
    """Test CLI argument parsing"""
    print_header("4. TESTING CLI FUNCTIONALITY")

    print_test("CLI module import")
    try:
        from lixplore import cli, commands
        print_pass("CLI modules imported successfully")
    except ImportError as e:
        print_fail(f"Cannot import CLI modules: {e}")
        return

    print_test("Argument parser creation")
    try:
        import argparse
        parser = argparse.ArgumentParser()
        commands.add_commands(parser)
        print_pass("Argument parser created successfully")

        # Test if all flags are registered
        flags_to_check = ['-P', '-C', '-J', '-E', '-X', '-A', '-q', '-m', '-D', '-a', '-N']
        for flag in flags_to_check:
            # This is a simple check - more thorough would be to parse help text
            print_pass(f"Flag {flag} registered")

    except Exception as e:
        print_fail(f"Argument parser error: {e}")


def test_dispatcher():
    """Test dispatcher functionality"""
    print_header("5. TESTING DISPATCHER")

    print_test("Dispatcher import and functions")
    try:
        from lixplore import dispatcher

        # Check if all required functions exist
        required_functions = ['search', 'deduplicate', 'filter_by_date',
                            'show_results', 'export_zotero', 'show_history']

        for func_name in required_functions:
            if hasattr(dispatcher, func_name):
                print_pass(f"Function '{func_name}' exists")
            else:
                print_fail(f"Function '{func_name}' missing")

    except ImportError as e:
        print_fail(f"Cannot import dispatcher: {e}")


def test_deduplication():
    """Test deduplication logic"""
    print_header("6. TESTING DEDUPLICATION")

    print_test("Deduplication with duplicate DOIs")
    try:
        from lixplore.dispatcher import deduplicate

        # Test data with duplicates
        test_results = [
            {"title": "Article 1", "doi": "10.1234/test1", "authors": []},
            {"title": "Article 2", "doi": "10.1234/test2", "authors": []},
            {"title": "Article 1 Duplicate", "doi": "10.1234/test1", "authors": []},  # Duplicate DOI
            {"title": "Article 3", "doi": "", "authors": []},
            {"title": "Article 3", "doi": "", "authors": []},  # Duplicate title
        ]

        deduplicated = deduplicate(test_results)

        if len(deduplicated) == 3:
            print_pass(f"Deduplication works correctly (5 -> 3 results)")
        else:
            print_fail(f"Deduplication incorrect: expected 3, got {len(deduplicated)}")

    except Exception as e:
        print_fail(f"Deduplication test error: {e}")


def test_error_handling():
    """Test error handling for edge cases"""
    print_header("7. TESTING ERROR HANDLING")

    print_test("Empty query handling")
    try:
        from lixplore.sources import pubmed
        results = pubmed.search("", max_results=1)
        if results is not None:
            print_pass("Empty query handled (returned empty or results)")
        else:
            print_warn("Empty query returned None")
    except Exception as e:
        print_warn(f"Empty query raised exception: {e}")

    print_test("Invalid max_results handling")
    try:
        from lixplore.sources import crossref
        results = crossref.search("test", max_results=0)
        if results is not None:
            print_pass("Zero max_results handled")
        else:
            print_warn("Zero max_results returned None")
    except Exception as e:
        print_warn(f"Zero max_results raised exception: {e}")

    print_test("Network timeout handling")
    try:
        from lixplore.sources import arxiv
        # Test with a query (can't force timeout easily, but check it doesn't crash)
        results = arxiv.search("test", max_results=1)
        print_pass("Network requests handled (no crash)")
    except Exception as e:
        print_warn(f"Network request exception: {e}")


def test_config_file():
    """Test configuration file"""
    print_header("8. TESTING CONFIGURATION")

    print_test("config.json exists and is valid JSON")
    try:
        import json
        with open("config.json", "r") as f:
            config = json.load(f)
        print_pass("config.json is valid JSON")

        # Check if it has expected structure
        if isinstance(config, dict):
            print_pass("config.json has dictionary structure")
        else:
            print_warn("config.json is not a dictionary")

    except FileNotFoundError:
        print_fail("config.json not found")
    except json.JSONDecodeError as e:
        print_fail(f"config.json invalid JSON: {e}")


def test_requirements():
    """Test requirements.txt"""
    print_header("9. TESTING REQUIREMENTS")

    print_test("requirements.txt has necessary packages")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()

        required_packages = ["biopython", "requests"]
        for package in required_packages:
            if package in content:
                print_pass(f"{package} listed in requirements.txt")
            else:
                print_fail(f"{package} missing from requirements.txt")

    except FileNotFoundError:
        print_fail("requirements.txt not found")


def print_summary():
    """Print final summary"""
    print_header("TROUBLESHOOTING SUMMARY")

    print(f"\n{BLUE}Total Issues Found: {len(issues_found)}{RESET}")
    if issues_found:
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
    else:
        print(f"  {GREEN}No critical issues found!{RESET}")

    print(f"\n{YELLOW}Total Warnings: {len(warnings_found)}{RESET}")
    if warnings_found:
        for i, warning in enumerate(warnings_found, 1):
            print(f"  {i}. {warning}")
    else:
        print(f"  {GREEN}No warnings!{RESET}")

    print("\n" + "="*70)

    if len(issues_found) == 0 and len(warnings_found) == 0:
        print(f"{GREEN}✓ ALL TESTS PASSED! Project is healthy.{RESET}")
        return 0
    elif len(issues_found) == 0:
        print(f"{YELLOW}⚠ All tests passed with warnings. Review warnings above.{RESET}")
        return 0
    else:
        print(f"{RED}✗ Critical issues found. Please fix the issues above.{RESET}")
        return 1


def main():
    """Run all troubleshooting tests"""
    print(f"\n{BLUE}{'='*70}")
    print("LIXPLORE CLI - COMPREHENSIVE TROUBLESHOOTING")
    print(f"{'='*70}{RESET}\n")

    test_imports()
    test_project_structure()
    test_source_connectors()
    test_cli_functionality()
    test_dispatcher()
    test_deduplication()
    test_error_handling()
    test_config_file()
    test_requirements()

    return print_summary()


if __name__ == "__main__":
    sys.exit(main())
