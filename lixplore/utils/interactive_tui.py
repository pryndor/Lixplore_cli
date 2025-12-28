#!/usr/bin/env python3
"""
Interactive TUI (Text User Interface) Mode

Provides an interactive terminal interface for browsing search results.
Uses rich library if available for enhanced display, falls back to curses.
"""

from __future__ import annotations
import sys
from typing import List, Dict, Optional, TYPE_CHECKING

# Try importing rich library
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.live import Live
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def launch_interactive_mode(results: List[Dict]):
    """
    Launch interactive TUI mode for browsing results.

    Args:
        results: List of article dictionaries
    """
    if not results:
        print("No results to display in interactive mode.")
        return

    if RICH_AVAILABLE:
        launch_rich_tui(results)
    else:
        launch_simple_tui(results)


def launch_rich_tui(results: List[Dict]):
    """
    Launch rich-based interactive TUI.

    Args:
        results: List of article dictionaries
    """
    console = Console()

    console.print("\n[bold cyan]LIXPLORE INTERACTIVE MODE[/bold cyan]")
    console.print("[dim]Navigate results with commands. Type 'help' for available commands.[/dim]\n")

    current_page = 0
    page_size = 10
    total_pages = (len(results) + page_size - 1) // page_size
    selected_articles = set()

    while True:
        # Calculate pagination
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, len(results))
        page_results = results[start_idx:end_idx]

        # Create table
        table = Table(title=f"Search Results (Page {current_page + 1}/{total_pages})", show_header=True)
        table.add_column("#", style="cyan", width=5)
        table.add_column("Selected", style="green", width=8)
        table.add_column("Title", style="white")
        table.add_column("Year", style="yellow", width=6)
        table.add_column("Source", style="magenta", width=12)

        for i, article in enumerate(page_results, start=start_idx + 1):
            check = "Yes" if i in selected_articles else ""
            title = article.get('title', 'No title')[:60] + "..." if len(article.get('title', '')) > 60 else article.get('title', 'No title')
            year = str(article.get('year', 'N/A'))
            source = article.get('source', 'Unknown')

            table.add_row(
                str(i),
                check,
                title,
                year,
                source
            )

        console.print(table)

        # Show selection info
        if selected_articles:
            console.print(f"\n[green]{len(selected_articles)} article(s) selected[/green]")

        # Command prompt
        console.print("\n[bold]Commands:[/bold] (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp")
        command = Prompt.ask("\n>", default="n").lower().strip()

        if command in ['q', 'quit', 'exit']:
            console.print("\n[yellow]Exiting interactive mode...[/yellow]")
            break

        elif command in ['n', 'next']:
            if current_page < total_pages - 1:
                current_page += 1
            else:
                console.print("[yellow]Already on last page[/yellow]")

        elif command in ['p', 'prev', 'previous']:
            if current_page > 0:
                current_page -= 1
            else:
                console.print("[yellow]Already on first page[/yellow]")

        elif command in ['h', 'help']:
            show_help_rich(console)

        elif command in ['v', 'view']:
            article_num = Prompt.ask("Enter article number to view", default="1")
            try:
                num = int(article_num)
                if 1 <= num <= len(results):
                    view_article_rich(console, results[num - 1], num)
                else:
                    console.print(f"[red]Invalid article number. Must be 1-{len(results)}[/red]")
            except ValueError:
                console.print("[red]Invalid number[/red]")

        elif command in ['s', 'select']:
            article_num = Prompt.ask("Enter article number to toggle selection", default="1")
            try:
                num = int(article_num)
                if 1 <= num <= len(results):
                    if num in selected_articles:
                        selected_articles.remove(num)
                        console.print(f"[yellow]Article #{num} deselected[/yellow]")
                    else:
                        selected_articles.add(num)
                        console.print(f"[green]Article #{num} selected[/green]")
                else:
                    console.print(f"[red]Invalid article number. Must be 1-{len(results)}[/red]")
            except ValueError:
                console.print("[red]Invalid number[/red]")

        elif command in ['e', 'export']:
            if selected_articles:
                export_selected_rich(console, results, list(selected_articles))
            else:
                console.print("[yellow]No articles selected. Select articles first with 's' command.[/yellow]")

        elif command.startswith('g'):  # goto page
            try:
                page_num = int(command[1:]) if len(command) > 1 else int(Prompt.ask("Enter page number"))
                if 1 <= page_num <= total_pages:
                    current_page = page_num - 1
                else:
                    console.print(f"[red]Invalid page. Must be 1-{total_pages}[/red]")
            except ValueError:
                console.print("[red]Invalid page number[/red]")

        else:
            console.print(f"[red]Unknown command: {command}. Type 'help' for available commands.[/red]")

        console.print()  # Blank line


def view_article_rich(console: Console, article: Dict, number: int):
    """Display detailed article view with rich formatting."""
    console.clear()

    # Create panel with article details
    details = []
    details.append(f"[bold cyan]Article #{number}[/bold cyan]\n")

    title = article.get('title', 'No title')
    details.append(f"[bold]Title:[/bold] {title}\n")

    authors = article.get('authors')
    if authors:
        if isinstance(authors, list):
            authors_str = ", ".join(authors[:5]) + ("..." if len(authors) > 5 else "")
        else:
            authors_str = str(authors)
        details.append(f"[bold]Authors:[/bold] {authors_str}\n")

    journal = article.get('journal')
    if journal:
        details.append(f"[bold]Journal:[/bold] {journal}")

    year = article.get('year')
    if year:
        details.append(f"  [bold]Year:[/bold] {year}\n")

    doi = article.get('doi')
    if doi:
        details.append(f"[bold]DOI:[/bold] {doi}\n")

    url = article.get('url')
    if url:
        details.append(f"[bold]URL:[/bold] {url}\n")

    source = article.get('source')
    if source:
        details.append(f"[bold]Source:[/bold] {source}\n")

    abstract = article.get('abstract')
    if abstract:
        details.append(f"\n[bold]Abstract:[/bold]\n{abstract[:500]}{'...' if len(abstract) > 500 else ''}")

    panel = Panel("\n".join(details), title="Article Details", border_style="cyan")
    console.print(panel)

    Prompt.ask("\nPress Enter to return")
    console.clear()


def export_selected_rich(console: Console, results: List[Dict], selected_numbers: List[int]):
    """Export selected articles."""
    formats = ["CSV", "JSON", "BibTeX", "RIS", "Excel", "EndNote"]
    console.print("\n[bold]Available export formats:[/bold]")
    for i, fmt in enumerate(formats, 1):
        console.print(f"  {i}. {fmt}")

    choice = Prompt.ask("Select format (1-6)", default="1")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(formats):
            selected_format = formats[idx].lower().replace(" ", "")

            # Get selected articles
            selected_results = [results[num - 1] for num in selected_numbers]

            # Import export function
            from lixplore.utils.export import export_results

            console.print(f"\n[cyan]Exporting {len(selected_results)} article(s) to {formats[idx]}...[/cyan]")
            output_file = export_results(selected_results, selected_format)

            if output_file:
                console.print(f"[green]Exported to: {output_file}[/green]")
            else:
                console.print("[red]Export failed[/red]")
        else:
            console.print("[red]Invalid choice[/red]")
    except ValueError:
        console.print("[red]Invalid input[/red]")


def show_help_rich(console: Console):
    """Show help panel."""
    help_text = """
[bold cyan]Navigation Commands:[/bold cyan]
  n, next      - Go to next page
  p, prev      - Go to previous page
  g<N>         - Go to page N (e.g., g3)

[bold cyan]Article Commands:[/bold cyan]
  v, view      - View detailed article information
  s, select    - Toggle article selection
  e, export    - Export selected articles

[bold cyan]Other Commands:[/bold cyan]
  h, help      - Show this help
  q, quit      - Exit interactive mode

[bold yellow]Tips:[/bold yellow]
  - Select multiple articles before exporting
  - Use arrow keys in prompts to navigate history
  - Press Ctrl+C to cancel any prompt
    """

    panel = Panel(help_text, title="Help", border_style="yellow")
    console.print(panel)
    Prompt.ask("\nPress Enter to continue")


def launch_simple_tui(results: List[Dict]):
    """
    Launch simple text-based TUI (fallback when rich is not available).

    Args:
        results: List of article dictionaries
    """
    print("\n" + "=" * 80)
    print("LIXPLORE INTERACTIVE MODE (Simple)")
    print("=" * 80)
    print("Note: Install 'rich' library for enhanced interface: pip install rich")
    print("=" * 80 + "\n")

    current_page = 0
    page_size = 10
    total_pages = (len(results) + page_size - 1) // page_size
    selected_articles = set()

    while True:
        # Calculate pagination
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, len(results))
        page_results = results[start_idx:end_idx]

        # Display results
        print(f"\nPage {current_page + 1}/{total_pages}")
        print("-" * 80)

        for i, article in enumerate(page_results, start=start_idx + 1):
            check = "[X]" if i in selected_articles else "[ ]"
            title = article.get('title', 'No title')[:55]
            year = str(article.get('year', 'N/A'))
            source = article.get('source', 'Unknown')[:10]

            print(f"{i:3d} {check} {title:55s} {year:6s} {source:10s}")

        if selected_articles:
            print(f"\n{len(selected_articles)} article(s) selected")

        # Command prompt
        print("\nCommands: (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp")
        command = input("\n> ").lower().strip()

        if command in ['q', 'quit', 'exit']:
            print("\nExiting interactive mode...")
            break

        elif command in ['n', 'next']:
            if current_page < total_pages - 1:
                current_page += 1
            else:
                print("Already on last page")

        elif command in ['p', 'prev', 'previous']:
            if current_page > 0:
                current_page -= 1
            else:
                print("Already on first page")

        elif command in ['h', 'help']:
            print("\n" + "=" * 80)
            print("HELP")
            print("=" * 80)
            print("  n, next      - Go to next page")
            print("  p, prev      - Go to previous page")
            print("  v, view      - View article details")
            print("  s, select    - Toggle article selection")
            print("  e, export    - Export selected articles")
            print("  q, quit      - Exit")
            print("=" * 80)
            input("\nPress Enter to continue...")

        elif command in ['v', 'view']:
            try:
                num = int(input("Enter article number: "))
                if 1 <= num <= len(results):
                    article = results[num - 1]
                    print("\n" + "=" * 80)
                    print(f"ARTICLE #{num}")
                    print("=" * 80)
                    print(f"Title: {article.get('title', 'No title')}")
                    print(f"Authors: {article.get('authors', 'N/A')}")
                    print(f"Journal: {article.get('journal', 'N/A')}")
                    print(f"Year: {article.get('year', 'N/A')}")
                    print(f"DOI: {article.get('doi', 'N/A')}")
                    print(f"Source: {article.get('source', 'N/A')}")
                    if article.get('abstract'):
                        print(f"\nAbstract:\n{article['abstract'][:500]}...")
                    print("=" * 80)
                    input("\nPress Enter to return...")
                else:
                    print(f"Invalid article number. Must be 1-{len(results)}")
            except ValueError:
                print("Invalid number")

        elif command in ['s', 'select']:
            try:
                num = int(input("Enter article number: "))
                if 1 <= num <= len(results):
                    if num in selected_articles:
                        selected_articles.remove(num)
                        print(f"Article #{num} deselected")
                    else:
                        selected_articles.add(num)
                        print(f"Article #{num} selected")
                else:
                    print(f"Invalid article number. Must be 1-{len(results)}")
            except ValueError:
                print("Invalid number")

        elif command in ['e', 'export']:
            if selected_articles:
                print("\nExport formats:")
                print("  1. CSV")
                print("  2. JSON")
                print("  3. BibTeX")
                print("  4. RIS")
                try:
                    choice = int(input("Select format (1-4): "))
                    formats = ["csv", "json", "bibtex", "ris"]
                    if 1 <= choice <= 4:
                        selected_results = [results[num - 1] for num in selected_articles]

                        from lixplore.utils.export import export_results
                        output_file = export_results(selected_results, formats[choice - 1])

                        if output_file:
                            print(f"Exported to: {output_file}")
                        else:
                            print("Export failed")
                    else:
                        print("Invalid choice")
                except ValueError:
                    print("Invalid input")
            else:
                print("No articles selected")

        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    # Test interactive mode
    test_results = [
        {'title': f'Article {i}', 'authors': ['Author A'], 'year': 2020 + i, 'source': 'PubMed', 'doi': f'10.1234/test{i}'}
        for i in range(25)
    ]

    launch_interactive_mode(test_results)
