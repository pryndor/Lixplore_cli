#!/usr/bin/env python3
"""
Enhanced TUI (Text User Interface) for Lixplore

A comprehensive visual interface combining:
- Main menu with wizard-like guidance
- Search interface
- Results browsing & selection
- Annotation management (rate, tag, comment)
- Statistics dashboard
- Export functionality

This is the PRIMARY interface for 90% of users.
"""

from __future__ import annotations
import sys
from typing import List, Dict, Optional, Set

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class EnhancedTUI:
    """Enhanced TUI with full functionality."""

    def __init__(self):
        if not RICH_AVAILABLE:
            print("WARNING: Rich library not available. Install with: pip install rich")
            print("Falling back to basic mode...")
            self.console = None
        else:
            self.console = Console()

        self.current_results = []
        self.selected_articles = set()
        self.annotation_manager = None

    def _get_annotation_manager(self):
        """Lazy load annotation manager."""
        if self.annotation_manager is None:
            try:
                from lixplore.utils.annotations import AnnotationManager
                self.annotation_manager = AnnotationManager()
            except Exception as e:
                if self.console:
                    self.console.print(f"[red]Could not load annotation manager: {e}[/red]")
                return None
        return self.annotation_manager

    def launch(self):
        """Launch the enhanced TUI main menu."""
        if not RICH_AVAILABLE:
            self._launch_simple()
            return

        self._show_welcome()

        while True:
            try:
                choice = self._show_main_menu()

                if choice == 1:
                    self._search_workflow()
                elif choice == 2:
                    self._browse_annotations()
                elif choice == 3:
                    self._show_statistics()
                elif choice == 4:
                    self._export_annotations()
                elif choice == 5:
                    self._show_help_guide()
                elif choice == 6:
                    self.console.print("\n[yellow]Thanks for using Lixplore! Goodbye![/yellow]\n")
                    break
                else:
                    self.console.print("[red]Invalid choice[/red]")

            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting Lixplore...[/yellow]\n")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")

    def _show_welcome(self):
        """Show welcome banner."""
        welcome_text = """
[bold cyan]╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                   LIXPLORE - ENHANCED MODE                    ║
║                                                               ║
║          Academic Literature Search & Management             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝[/bold cyan]

[dim]Welcome! This interactive mode guides you through searching, annotating,
and managing your research literature.[/dim]
"""
        self.console.print(welcome_text)

    def _show_main_menu(self) -> int:
        """Show main menu and get user choice."""
        menu_panel = Panel("""
[bold cyan]Main Menu:[/bold cyan]

  1. Search for Articles
  2. Browse My Annotations
  3. View Statistics
  4. Export Annotations
  5. Help & Guide
  6. Exit

[dim]Choose an option to get started...[/dim]
""", title="What would you like to do?", border_style="cyan", box=box.ROUNDED)

        self.console.print(menu_panel)

        try:
            choice = IntPrompt.ask("\nYour choice", default=1, show_default=True)
            return choice
        except:
            return 0

    # ============ SEARCH WORKFLOW ============

    def _search_workflow(self):
        """Guided search workflow."""
        self.console.clear()
        self.console.print("\n[bold cyan]SEARCH FOR ARTICLES[/bold cyan]\n")

        # Get search query
        query = Prompt.ask("What do you want to search for?")
        if not query:
            self.console.print("[yellow]Search cancelled[/yellow]")
            return

        # Choose database
        self.console.print("\n[bold]Which database?[/bold]")
        databases = [
            ("1", "PubMed", "Biomedical & life sciences"),
            ("2", "arXiv", "Physics, math, CS, etc."),
            ("3", "Crossref", "Scholarly works with DOIs"),
            ("4", "EuropePMC", "European biomedical literature"),
            ("5", "All databases", "Comprehensive search (slower)")
        ]

        for num, name, desc in databases:
            marker = "→" if num == "1" else " "
            self.console.print(f"  {marker} {num}. [bold]{name}[/bold] - [dim]{desc}[/dim]")

        db_choice = Prompt.ask("\nYour choice", default="1")

        # Map choice to flags
        db_map = {"1": "P", "2": "x", "3": "C", "4": "E", "5": "A"}
        source_flag = db_map.get(db_choice, "P")

        # Max results
        max_results = IntPrompt.ask("\nHow many results?", default=20)

        # Show abstracts?
        show_abstracts = Confirm.ask("Show abstracts?", default=False)

        # Remove duplicates (if all databases)
        dedup = False
        if db_choice == "5":
            dedup = Confirm.ask("Remove duplicates?", default=True)

        # Execute search
        self.console.print(f"\n[cyan]Searching for: '{query}'...[/cyan]\n")

        try:
            from lixplore import dispatcher

            # Determine which sources to search
            if source_flag == "A":
                sources = ["pubmed", "crossref", "doaj", "europepmc", "arxiv"]
            else:
                source_map = {
                    "P": "pubmed",
                    "x": "arxiv",
                    "C": "crossref",
                    "E": "europepmc"
                }
                sources = [source_map[source_flag]]

            # Search each source
            all_results = []
            for source in sources:
                source_names = {
                    "pubmed": "PubMed",
                    "crossref": "Crossref",
                    "doaj": "DOAJ",
                    "europepmc": "EuropePMC",
                    "arxiv": "arXiv"
                }
                self.console.print(f"  Searching {source_names[source]}...")

                try:
                    results = dispatcher.search(
                        source=source,
                        query=query,
                        limit=max_results
                    )
                    if results:
                        all_results.extend(results)
                        self.console.print(f"    Found {len(results)} articles")
                except Exception as e:
                    self.console.print(f"    [yellow]Error: {e}[/yellow]")

            # Deduplicate if searching multiple sources
            if dedup and len(sources) > 1 and all_results:
                self.console.print("\n  Removing duplicates...")
                all_results = dispatcher.deduplicate_advanced(
                    all_results,
                    strategy="auto",
                    threshold=0.85,
                    keep="first",
                    merge_data=False
                )

            if all_results:
                self.current_results = all_results
                self.console.print(f"\n[green]Found {len(all_results)} articles total![/green]\n")

                # Browse results
                if Confirm.ask("Browse results now?", default=True):
                    self._browse_results()
            else:
                self.console.print("\n[yellow]No results found[/yellow]")
                Prompt.ask("\nPress Enter to continue")

        except Exception as e:
            self.console.print(f"\n[red]Search failed: {e}[/red]")
            import traceback
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            Prompt.ask("\nPress Enter to continue")

    # ============ RESULTS BROWSING ============

    def _browse_results(self):
        """Browse search results with pagination."""
        if not self.current_results:
            self.console.print("[yellow]No results to browse[/yellow]")
            Prompt.ask("\nPress Enter to continue")
            return

        current_page = 0
        page_size = 10
        total_pages = (len(self.current_results) + page_size - 1) // page_size

        while True:
            self.console.clear()

            # Calculate pagination
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(self.current_results))
            page_results = self.current_results[start_idx:end_idx]

            # Show results table
            table = Table(
                title=f"Search Results (Page {current_page + 1}/{total_pages})",
                show_header=True,
                box=box.ROUNDED
            )
            table.add_column("#", style="cyan", width=5)
            table.add_column("Rating", style="yellow", width=8)
            table.add_column("Title", style="white")
            table.add_column("Year", style="yellow", width=6)
            table.add_column("Source", style="magenta", width=10)

            # Get annotations for display
            manager = self._get_annotation_manager()

            for i, article in enumerate(page_results, start=start_idx + 1):
                # Check if annotated
                rating_display = ""
                if manager:
                    annotation = manager.get_annotation_for_article(article)
                    if annotation and annotation.get('rating'):
                        rating_display = f"{annotation['rating']}/5"

                title = article.get('title', 'No title')
                if len(title) > 50:
                    title = title[:47] + "..."

                table.add_row(
                    str(i),
                    rating_display,
                    title,
                    str(article.get('year', 'N/A')),
                    article.get('source', 'Unknown')
                )

            self.console.print(table)

            # Show commands
            if self.selected_articles:
                self.console.print(f"\n[green]{len(self.selected_articles)} article(s) selected[/green]")

            self.console.print("\n[bold]Commands:[/bold]")
            self.console.print("  [cyan]n[/cyan]ext  [cyan]p[/cyan]rev  [cyan]v[/cyan]iew  [cyan]a[/cyan]nnotate  [cyan]s[/cyan]elect  [cyan]e[/cyan]xport  [cyan]b[/cyan]ack  [cyan]q[/cyan]uit")

            command = Prompt.ask("\n>", default="n").lower().strip()

            if command in ['q', 'quit']:
                if Confirm.ask("Exit browse mode?", default=False):
                    break

            elif command in ['b', 'back']:
                break

            elif command in ['n', 'next']:
                if current_page < total_pages - 1:
                    current_page += 1
                else:
                    self.console.print("[yellow]Already on last page[/yellow]")
                    Prompt.ask("Press Enter")

            elif command in ['p', 'prev', 'previous']:
                if current_page > 0:
                    current_page -= 1
                else:
                    self.console.print("[yellow]Already on first page[/yellow]")
                    Prompt.ask("Press Enter")

            elif command in ['v', 'view']:
                try:
                    num = IntPrompt.ask("Article number", default=start_idx + 1)
                    if 1 <= num <= len(self.current_results):
                        self._view_article(self.current_results[num - 1], num)
                    else:
                        self.console.print(f"[red]Invalid number. Must be 1-{len(self.current_results)}[/red]")
                        Prompt.ask("Press Enter")
                except:
                    pass

            elif command in ['a', 'annotate']:
                try:
                    num = IntPrompt.ask("Article number to annotate", default=start_idx + 1)
                    if 1 <= num <= len(self.current_results):
                        self._annotate_article(self.current_results[num - 1], num)
                    else:
                        self.console.print(f"[red]Invalid number[/red]")
                        Prompt.ask("Press Enter")
                except:
                    pass

            elif command in ['s', 'select']:
                try:
                    num = IntPrompt.ask("Article number", default=start_idx + 1)
                    if 1 <= num <= len(self.current_results):
                        if num in self.selected_articles:
                            self.selected_articles.remove(num)
                            self.console.print(f"[yellow]Article #{num} deselected[/yellow]")
                        else:
                            self.selected_articles.add(num)
                            self.console.print(f"[green]Article #{num} selected[/green]")
                        Prompt.ask("Press Enter")
                    else:
                        self.console.print(f"[red]Invalid number[/red]")
                        Prompt.ask("Press Enter")
                except:
                    pass

            elif command in ['e', 'export']:
                if self.selected_articles:
                    self._export_selected_results()
                else:
                    self.console.print("[yellow]No articles selected. Select with 's' first.[/yellow]")
                    Prompt.ask("Press Enter")

            else:
                self.console.print(f"[red]Unknown command: {command}[/red]")
                Prompt.ask("Press Enter")

    def _view_article(self, article: Dict, number: int):
        """View detailed article information."""
        self.console.clear()

        details = []
        details.append(f"[bold cyan]Article #{number}[/bold cyan]\n")
        details.append(f"[bold]Title:[/bold] {article.get('title', 'No title')}\n")

        authors = article.get('authors', [])
        if authors:
            author_str = ", ".join(authors[:5]) if isinstance(authors, list) else str(authors)
            if isinstance(authors, list) and len(authors) > 5:
                author_str += f" [dim](+{len(authors) - 5} more)[/dim]"
            details.append(f"[bold]Authors:[/bold] {author_str}\n")

        if article.get('journal'):
            details.append(f"[bold]Journal:[/bold] {article['journal']}")
        if article.get('year'):
            details.append(f"  [bold]Year:[/bold] {article['year']}\n")
        if article.get('doi'):
            details.append(f"[bold]DOI:[/bold] {article['doi']}\n")
        if article.get('url'):
            details.append(f"[bold]URL:[/bold] {article['url']}\n")
        if article.get('source'):
            details.append(f"[bold]Source:[/bold] {article['source']}\n")

        # Show existing annotation if any
        manager = self._get_annotation_manager()
        if manager:
            annotation = manager.get_annotation_for_article(article)
            if annotation:
                details.append("\n[bold yellow]ANNOTATION:[/bold yellow]\n")
                if annotation.get('rating'):
                    stars = f"{annotation['rating']}/5 stars"
                    details.append(f"[bold]Rating:[/bold] {stars}\n")
                if annotation.get('tags'):
                    details.append(f"[bold]Tags:[/bold] {', '.join(annotation['tags'])}\n")
                if annotation.get('comments'):
                    details.append(f"[bold]Comments:[/bold]\n")
                    for comment in annotation['comments']:
                        details.append(f"  • {comment['text']}\n")

        # Abstract
        abstract = article.get('abstract')
        if abstract:
            details.append(f"\n[bold]Abstract:[/bold]\n{abstract[:500]}{'...' if len(abstract) > 500 else ''}")

        panel = Panel("\n".join(details), title="Article Details", border_style="cyan", box=box.ROUNDED)
        self.console.print(panel)

        Prompt.ask("\nPress Enter to return")

    def _annotate_article(self, article: Dict, number: int):
        """Annotate an article."""
        self.console.clear()
        self.console.print(f"\n[bold cyan]ANNOTATE ARTICLE #{number}[/bold cyan]\n")

        title = article.get('title', 'No title')
        if len(title) > 60:
            title = title[:57] + "..."
        self.console.print(f"[dim]{title}[/dim]\n")

        manager = self._get_annotation_manager()
        if not manager:
            self.console.print("[red]Annotation system not available[/red]")
            Prompt.ask("Press Enter")
            return

        # Check existing annotation
        existing = manager.get_annotation_for_article(article)
        if existing:
            self.console.print("[yellow]This article already has annotations:[/yellow]")
            if existing.get('rating'):
                self.console.print(f"  Rating: {existing['rating']}/5 stars")
            if existing.get('tags'):
                self.console.print(f"  Tags: {', '.join(existing['tags'])}")
            self.console.print()

        # Get rating
        if Confirm.ask("Add/update rating?", default=True):
            try:
                rating = IntPrompt.ask("Rating (1-5 stars)", default=5)
                if not 1 <= rating <= 5:
                    rating = 5
            except:
                rating = None
        else:
            rating = None

        # Get tags
        tags = None
        if Confirm.ask("Add/update tags?", default=True):
            self.console.print("[dim]Examples: important, cite-in-paper, methodology, review-later[/dim]")
            tags_input = Prompt.ask("Tags (comma-separated)")
            if tags_input:
                tags = [t.strip() for t in tags_input.split(',') if t.strip()]

        # Get comment
        comment = None
        if Confirm.ask("Add a comment/note?", default=True):
            comment = Prompt.ask("Your comment")

        # Priority
        priority = None
        if Confirm.ask("Set priority?", default=False):
            self.console.print("  1. Low\n  2. Medium\n  3. High")
            priority_choice = IntPrompt.ask("Priority", default=2)
            priority = {1: "low", 2: "medium", 3: "high"}.get(priority_choice, "medium")

        # Read status
        read_status = None
        if Confirm.ask("Set read status?", default=False):
            self.console.print("  1. Unread\n  2. Reading\n  3. Read")
            status_choice = IntPrompt.ask("Status", default=1)
            read_status = {1: "unread", 2: "reading", 3: "read"}.get(status_choice, "unread")

        # Save annotation
        try:
            manager.annotate(
                article,
                comment=comment,
                rating=rating,
                tags=tags,
                read_status=read_status,
                priority=priority
            )
            self.console.print("\n[green]Annotation saved successfully![/green]")
        except Exception as e:
            self.console.print(f"\n[red]Failed to save annotation: {e}[/red]")

        Prompt.ask("\nPress Enter to continue")

    def _export_selected_results(self):
        """Export selected search results."""
        selected_results = [self.current_results[num - 1] for num in sorted(self.selected_articles)]

        self.console.print("\n[bold]Export Format:[/bold]")
        formats = ["CSV", "JSON", "BibTeX", "RIS", "Excel", "EndNote"]
        for i, fmt in enumerate(formats, 1):
            self.console.print(f"  {i}. {fmt}")

        try:
            choice = IntPrompt.ask("\nSelect format (1-6)", default=1)
            if 1 <= choice <= len(formats):
                from lixplore.utils.export import export_results

                format_name = formats[choice - 1].lower()
                self.console.print(f"\n[cyan]Exporting {len(selected_results)} article(s)...[/cyan]")

                output_file = export_results(selected_results, format_name)
                if output_file:
                    self.console.print(f"[green]Exported to: {output_file}[/green]")
                else:
                    self.console.print("[red]Export failed[/red]")
            else:
                self.console.print("[red]Invalid choice[/red]")
        except Exception as e:
            self.console.print(f"[red]Export error: {e}[/red]")

        Prompt.ask("\nPress Enter to continue")

    # ============ ANNOTATION BROWSING ============

    def _browse_annotations(self):
        """Browse all annotations."""
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print("[red]Annotation system not available[/red]")
            Prompt.ask("Press Enter")
            return

        while True:
            self.console.clear()
            self.console.print("\n[bold cyan]MY ANNOTATIONS[/bold cyan]\n")

            self.console.print("[bold]View:[/bold]")
            self.console.print("  1. All annotations")
            self.console.print("  2. High-rated (4-5 stars)")
            self.console.print("  3. Unread articles")
            self.console.print("  4. High priority")
            self.console.print("  5. Search by keyword")
            self.console.print("  6. Back to main menu")

            try:
                choice = IntPrompt.ask("\nYour choice", default=1)

                if choice == 6:
                    break
                elif choice == 1:
                    annotations = manager.list_all()
                elif choice == 2:
                    annotations = manager.list_all({'min_rating': 4})
                elif choice == 3:
                    annotations = manager.list_all({'read_status': 'unread'})
                elif choice == 4:
                    annotations = manager.list_all({'priority': 'high'})
                elif choice == 5:
                    keyword = Prompt.ask("Search keyword")
                    results = manager.search_annotations(keyword)
                    annotations = [{'article_id': r['article_id'], 'annotation': r['annotation']} for r in results]
                else:
                    continue

                if not annotations:
                    self.console.print("\n[yellow]No annotations found[/yellow]")
                    Prompt.ask("Press Enter")
                    continue

                # Display annotations
                self._display_annotation_list(annotations)
                Prompt.ask("\nPress Enter to continue")

            except:
                pass

    def _display_annotation_list(self, annotations: List[Dict]):
        """Display list of annotations."""
        self.console.print(f"\n[bold]Found {len(annotations)} annotation(s):[/bold]\n")

        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Rating", style="yellow", width=8)
        table.add_column("Title", style="white")
        table.add_column("Tags", style="green", width=20)
        table.add_column("Status", style="magenta", width=10)

        for i, item in enumerate(annotations, 1):
            annotation = item['annotation']
            info = annotation.get('article_info', {})

            rating = ""
            if annotation.get('rating'):
                rating = f"{annotation['rating']}/5"

            title = info.get('title', 'No title')
            if len(title) > 40:
                title = title[:37] + "..."

            tags = ', '.join(annotation.get('tags', [])[:3])
            if len(annotation.get('tags', [])) > 3:
                tags += "..."

            status = annotation.get('read_status', 'unread').title()

            table.add_row(str(i), rating, title, tags, status)

        self.console.print(table)

    # ============ STATISTICS ============

    def _show_statistics(self):
        """Show annotation statistics."""
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print("[red]Annotation system not available[/red]")
            Prompt.ask("Press Enter")
            return

        stats = manager.get_statistics()

        self.console.print("\n[bold cyan]ANNOTATION STATISTICS[/bold cyan]\n")

        # Create statistics panel
        stats_text = []
        stats_text.append(f"[bold]Total Annotated Articles:[/bold] {stats['total']}\n")

        if stats['by_rating']:
            stats_text.append("[bold]Rating Distribution:[/bold]")
            for rating in sorted(stats['by_rating'].keys(), reverse=True):
                count = stats['by_rating'][rating]
                stars = f"({rating})"
                bar = '█' * count
                stats_text.append(f"  {stars} ({rating}): {bar} {count}")
            stats_text.append("")

        if stats['by_status']:
            stats_text.append("[bold]Read Status:[/bold]")
            for status, count in stats['by_status'].items():
                stats_text.append(f"  {status.title()}: {count}")
            stats_text.append("")

        if stats['by_priority']:
            stats_text.append("[bold]Priority:[/bold]")
            for priority, count in stats['by_priority'].items():
                stats_text.append(f"  {priority.title()}: {count}")
            stats_text.append("")

        stats_text.append(f"[bold]Comments:[/bold]")
        stats_text.append(f"  Articles with comments: {stats['with_comments']}")
        stats_text.append(f"  Total comments: {stats['total_comments']}")
        stats_text.append("")

        stats_text.append(f"[bold]Tags:[/bold]")
        stats_text.append(f"  Unique tags: {stats['total_tags']}")
        if stats.get('unique_tags'):
            tags_display = ', '.join(stats['unique_tags'][:10])
            if len(stats['unique_tags']) > 10:
                tags_display += "..."
            stats_text.append(f"  Tags: {tags_display}")

        panel = Panel("\n".join(stats_text), title="Statistics", border_style="cyan", box=box.ROUNDED)
        self.console.print(panel)

        Prompt.ask("\nPress Enter to continue")

    # ============ EXPORT ANNOTATIONS ============

    def _export_annotations(self):
        """Export all annotations."""
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print("[red]Annotation system not available[/red]")
            Prompt.ask("Press Enter")
            return

        self.console.print("\n[bold cyan]EXPORT ANNOTATIONS[/bold cyan]\n")

        self.console.print("[bold]Export Format:[/bold]")
        formats = ["Markdown", "JSON", "CSV"]
        for i, fmt in enumerate(formats, 1):
            self.console.print(f"  {i}. {fmt}")

        try:
            choice = IntPrompt.ask("\nSelect format (1-3)", default=1)
            if 1 <= choice <= 3:
                format_map = {1: "markdown", 2: "json", 3: "csv"}
                export_format = format_map[choice]

                self.console.print(f"\n[cyan]Exporting annotations to {formats[choice-1]}...[/cyan]")
                output_file = manager.export_annotations(format=export_format)
                self.console.print(f"[green]Exported to: {output_file}[/green]")
            else:
                self.console.print("[red]Invalid choice[/red]")
        except Exception as e:
            self.console.print(f"[red]Export error: {e}[/red]")

        Prompt.ask("\nPress Enter to continue")

    # ============ HELP & GUIDE ============

    def _show_help_guide(self):
        """Show help and user guide."""
        self.console.clear()

        help_text = """
[bold cyan]LIXPLORE HELP & GUIDE[/bold cyan]

[bold yellow]Main Menu Options:[/bold yellow]

  [bold]1. Search for Articles[/bold]
     - Choose database (PubMed, arXiv, etc.)
     - Enter search query
     - Browse and annotate results

  [bold]2. Browse My Annotations[/bold]
     - View all your annotated articles
     - Filter by rating, status, priority
     - Search annotations by keyword

  [bold]3. View Statistics[/bold]
     - See rating distribution
     - View read status breakdown
     - Tag usage statistics

  [bold]4. Export Annotations[/bold]
     - Export to Markdown (readable)
     - Export to JSON (backup)
     - Export to CSV (spreadsheet)

[bold yellow]Tips:[/bold yellow]

  • Use ratings (1-5 stars) to mark quality
  • Tag articles for easy organization
  • Add comments for important notes
  • Set priority for must-read papers
  • Export regularly to backup your work

[bold yellow]Keyboard Shortcuts:[/bold yellow]

  • Ctrl+C - Cancel current operation
  • Enter - Accept default/continue
  • Type number - Quick selection

[bold yellow]Annotation Best Practices:[/bold yellow]

  • Rate as you read (1-5 stars)
  • Use consistent tags (e.g., "cite", "important")
  • Add specific comments (e.g., "Fig 3 has data")
  • Mark read status to track progress
  • Export weekly for backup

[bold yellow]For CLI Usage:[/bold yellow]

  Run: lixplore -P -q "topic" -m 20 -X xlsx

  See: lixplore --help

"""
        panel = Panel(help_text, title="Help & Guide", border_style="yellow", box=box.ROUNDED)
        self.console.print(panel)

        Prompt.ask("\nPress Enter to return to main menu")

    # ============ SIMPLE FALLBACK ============

    def _launch_simple(self):
        """Simple mode when Rich is not available."""
        print("\n" + "=" * 70)
        print("LIXPLORE - ENHANCED MODE (Simple)")
        print("=" * 70)
        print("\nNote: Install 'rich' for better interface:")
        print("  pip install rich")
        print("\n" + "=" * 70)

        while True:
            print("\nMain Menu:")
            print("  1. Search for articles")
            print("  2. Browse annotations")
            print("  3. View statistics")
            print("  4. Export annotations")
            print("  5. Exit")

            try:
                choice = input("\nYour choice [1]: ").strip() or "1"
                if choice == "5":
                    print("\nGoodbye!")
                    break
                elif choice in ["1", "2", "3", "4"]:
                    print(f"\n[Feature {choice} - Rich library required for full functionality]")
                    input("Press Enter to continue...")
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break


def launch_enhanced_tui(results=None):
    """
    Launch the enhanced TUI.

    Args:
        results: Optional list of search results to browse immediately
    """
    tui = EnhancedTUI()

    if results:
        # If results provided, go directly to browse mode
        tui.current_results = results
        if RICH_AVAILABLE and tui.console:
            if Confirm.ask("\nBrowse results in TUI mode?", default=True):
                tui._browse_results()
        else:
            print("Results available. Launch TUI with: lixplore --tui")
    else:
        # Launch main menu
        tui.launch()


if __name__ == "__main__":
    # Test the TUI
    launch_enhanced_tui()
