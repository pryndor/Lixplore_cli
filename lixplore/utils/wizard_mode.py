#!/usr/bin/env python3
"""
Wizard Mode for Lixplore

Provides guided workflows for common tasks.
Helps new users navigate the tool without memorizing flags.
"""

import sys
from typing import Optional


def get_input(prompt: str, default: str = None) -> str:
    """Get user input with optional default."""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()


def get_choice(prompt: str, options: list, default: int = 1) -> int:
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        marker = "→" if i == default else " "
        print(f"  {marker} {i}. {option}")

    while True:
        choice = get_input("\nYour choice", str(default))
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")


def confirm(prompt: str, default: bool = True) -> bool:
    """Get yes/no confirmation from user."""
    default_str = "Y/n" if default else "y/N"
    response = get_input(f"{prompt} [{default_str}]", "").lower()

    if not response:
        return default

    return response in ['y', 'yes']


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "┌" + "─" * 60 + "┐")
    print(f"│  {text:<57} │")
    print("└" + "─" * 60 + "┘\n")


def search_workflow(shell=None):
    """Guided workflow for searching articles."""
    print_header("SEARCH FOR ARTICLES")

    # Get search query
    query = get_input("What do you want to search for?")
    if not query:
        print("Search cancelled - no query provided")
        return

    # Choose database
    databases = [
        "PubMed (biomedical & life sciences)",
        "arXiv (physics, math, CS, etc.)",
        "Crossref (scholarly works with DOIs)",
        "EuropePMC (European biomedical)",
        "All databases (slower but comprehensive)"
    ]

    db_choice = get_choice("Which database?", databases, default=1)
    db_flags = {
        1: "-P",
        2: "-x",
        3: "-C",
        4: "-E",
        5: "-A"
    }
    db_flag = db_flags[db_choice]

    # Number of results
    max_results = get_input("How many results do you want?", "10")

    # Additional options
    show_abstracts = confirm("Show abstracts?", default=False)
    dedup = False
    if db_choice == 5:  # All databases
        dedup = confirm("Remove duplicates?", default=True)

    # Build command
    command = f'search "{query}" {db_flag} -m {max_results}'
    if show_abstracts:
        command += " -a"
    if dedup:
        command += " -D"

    print(f"\n🚀 Running: {command}\n")

    # Execute if in shell mode
    if shell:
        shell.onecmd(command)
    else:
        print("Execute this command:")
        print(f"  lixplore {command.replace('search', '-q')}")


def annotate_workflow(shell=None):
    """Guided workflow for annotating articles."""
    print_header("ANNOTATE AN ARTICLE")

    if shell and not shell.last_results:
        print("No search results available.")
        print("Run a search first using the search wizard or 'search' command")
        return

    # Get article number
    article_num = get_input("Which article number do you want to annotate?")
    if not article_num.isdigit():
        print("Invalid article number")
        return

    # Rating
    add_rating = confirm("Do you want to rate this article?", default=True)
    rating = None
    if add_rating:
        while True:
            rating = get_input("Rating (1-5 stars)", "4")
            try:
                rating_num = int(rating)
                if 1 <= rating_num <= 5:
                    rating = rating_num
                    break
                print("Rating must be between 1 and 5")
            except ValueError:
                print("Please enter a number")

    # Tags
    add_tags = confirm("Do you want to add tags?", default=True)
    tags = None
    if add_tags:
        print("\nExamples: important, cite-in-paper, methodology, review-later")
        tags = get_input("Tags (comma-separated)")

    # Comment
    add_comment = confirm("Do you want to add a comment/note?", default=True)
    comment = None
    if add_comment:
        comment = get_input("Your comment")

    # Priority
    priorities = ["Low", "Medium", "High"]
    priority_choice = get_choice("Priority level?", priorities, default=2)
    priority = priorities[priority_choice - 1].lower()

    # Read status
    statuses = ["Unread", "Currently reading", "Finished reading"]
    status_choice = get_choice("Read status?", statuses, default=1)
    status_map = {1: "unread", 2: "reading", 3: "read"}
    read_status = status_map[status_choice]

    # Build command
    command = f"annotate {article_num}"
    if rating:
        command += f" --rating {rating}"
    if tags:
        command += f' --tags "{tags}"'
    if comment:
        command += f' --comment "{comment}"'
    command += f" --priority {priority}"
    command += f" --status {read_status}"

    print(f"\n🚀 Annotating article #{article_num}...\n")

    # Execute if in shell mode
    if shell:
        shell.onecmd(command)
    else:
        print("Execute this command:")
        print(f"  (Search first, then annotate)")


def view_annotations_workflow(shell=None):
    """Guided workflow for viewing annotations."""
    print_header("👀 VIEW ANNOTATIONS")

    options = [
        "List all annotated articles",
        "List high-rated articles (4-5 stars)",
        "List unread articles",
        "List high-priority articles",
        "Search annotations by keyword"
    ]

    choice = get_choice("What do you want to see?", options)

    if choice == 1:
        command = "list annotations"
    elif choice == 2:
        command = 'list annotations -f "min_rating=4"'
    elif choice == 3:
        command = 'list annotations -f "read_status=unread"'
    elif choice == 4:
        command = 'list annotations -f "priority=high"'
    elif choice == 5:
        keyword = get_input("Search keyword")
        command = f'search-annotations "{keyword}"'

    print(f"\n🚀 Running: {command}\n")

    # Execute if in shell mode
    if shell:
        shell.onecmd(command)
    else:
        print("Execute this command:")
        print(f"  lixplore --{command}")


def export_workflow(shell=None):
    """Guided workflow for exporting annotations."""
    print_header("EXPORT ANNOTATIONS")

    formats = [
        "Markdown (readable, nice formatting)",
        "JSON (backup, programmatic access)",
        "CSV (spreadsheet, Excel)"
    ]

    choice = get_choice("Export format?", formats, default=1)
    format_map = {1: "markdown", 2: "json", 3: "csv"}
    export_format = format_map[choice]

    print(f"\nYour annotations will be exported to:")
    print(f"   lixplore_annotations_{export_format}")
    print()

    if not confirm("Proceed with export?", default=True):
        print("Export cancelled")
        return

    command = f"export {export_format}"

    print(f"\n🚀 Exporting...\n")

    # Execute if in shell mode
    if shell:
        shell.onecmd(command)
    else:
        print("Execute this command:")
        print(f"  lixplore --export-annotations {export_format}")


def pdf_workflow(shell=None):
    """Guided workflow for downloading PDFs."""
    print_header("📄 DOWNLOAD PDFs")

    print("PDF download requires search results first\n")

    if shell and not shell.last_results:
        print("No search results available.")
        print("Run a search first")
        return

    # Get article numbers
    article_nums = get_input("Which articles? (e.g., 1 3 5 or 1-10)")

    # SciHub option
    use_scihub = confirm("Use SciHub as fallback?", default=False)

    # Build command
    print(f"\nTo download PDFs, use this command:")
    scihub_flag = " --use-scihub" if use_scihub else ""
    print(f"  lixplore --download-pdf --pdf-numbers {article_nums}{scihub_flag}")
    print("\nNote: This feature requires running from terminal, not shell mode yet")


def main_wizard_menu(shell=None):
    """Main wizard menu."""
    print_header("LIXPLORE WIZARD")

    workflows = [
        "Search for articles",
        "Annotate an article",
        "View my annotations",
        "Export annotations",
        "Download PDFs",
        "Exit wizard"
    ]

    choice = get_choice("What do you want to do?", workflows)

    if choice == 1:
        search_workflow(shell)
    elif choice == 2:
        annotate_workflow(shell)
    elif choice == 3:
        view_annotations_workflow(shell)
    elif choice == 4:
        export_workflow(shell)
    elif choice == 5:
        pdf_workflow(shell)
    elif choice == 6:
        print("\nExiting wizard mode\n")
        return False

    # Ask if user wants to do something else
    print()
    if confirm("Do you want to do something else?", default=True):
        return True
    else:
        print("\nExiting wizard mode\n")
        return False


def launch_wizard(shell=None):
    """Launch the wizard interface."""
    try:
        while True:
            continue_wizard = main_wizard_menu(shell)
            if not continue_wizard:
                break
    except KeyboardInterrupt:
        print("\n\nWizard cancelled\n")
    except EOFError:
        print("\n\nExiting wizard\n")


if __name__ == "__main__":
    # Test wizard in standalone mode
    launch_wizard()
