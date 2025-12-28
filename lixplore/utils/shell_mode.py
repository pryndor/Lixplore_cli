#!/usr/bin/env python3
"""
Interactive Shell Mode for Lixplore

Provides a persistent shell where users can run commands without typing 'lixplore' repeatedly.
Similar to OpenBB Terminal experience.
"""

import cmd
import shlex
import sys
from typing import List, Dict, Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class LixploreShell(cmd.Cmd):
    """Interactive shell for Lixplore commands."""

    intro = """
╔════════════════════════════════════════════════════════════════╗
║                 LIXPLORE INTERACTIVE SHELL                     ║
║                                                                ║
║  Welcome to Lixplore! Type 'help' for commands.               ║
║  Type 'help <command>' for detailed help on a command.        ║
║  Type 'wizard' for guided workflow assistance.                ║
║  Type 'exit' or 'quit' to leave.                              ║
╚════════════════════════════════════════════════════════════════╝
"""

    prompt = "lixplore> "

    def __init__(self):
        super().__init__()
        self.last_results = []
        self.annotation_manager = None

        if RICH_AVAILABLE:
            self.console = Console()

    def _get_annotation_manager(self):
        """Lazy load annotation manager."""
        if self.annotation_manager is None:
            from lixplore.utils.annotations import AnnotationManager
            self.annotation_manager = AnnotationManager()
        return self.annotation_manager

    # ============ SEARCH COMMANDS ============

    def do_search(self, arg):
        """
        Search for articles across databases.

        Usage:
            search <query> [options]

        Options:
            -P, --pubmed        Search PubMed
            -A, --all           Search all sources
            -C, --crossref      Search Crossref
            -E, --europepmc     Search EuropePMC
            -x, --arxiv         Search arXiv
            -m, --max N         Maximum results (default: 10)
            -a, --abstract      Show abstracts
            -D, --dedup         Remove duplicates

        Examples:
            search cancer treatment -P -m 20
            search "machine learning" -x -m 30 -a
            search diabetes -A -D -m 50
        """
        if not arg:
            print("Error: Please provide a search query")
            print("Usage: search <query> [options]")
            return

        try:
            # Parse arguments
            args = shlex.split(arg)

            # Build command for dispatcher
            from lixplore import dispatcher

            # Create a namespace object to mimic argparse
            import argparse
            ns = argparse.Namespace()

            # Extract query (everything before first -)
            query_parts = []
            options = []
            in_options = False

            for token in args:
                if token.startswith('-'):
                    in_options = True
                if in_options:
                    options.append(token)
                else:
                    query_parts.append(token)

            query = ' '.join(query_parts)

            # Set defaults
            ns.query = query
            ns.pubmed = '-P' in options or '--pubmed' in options
            ns.all = '-A' in options or '--all' in options
            ns.crossref = '-C' in options or '--crossref' in options
            ns.europepmc = '-E' in options or '--europepmc' in options
            ns.arxiv = '-x' in options or '--arxiv' in options
            ns.abstract = '-a' in options or '--abstract' in options
            ns.dedup = '-D' in options or '--dedup' in options
            ns.dedup_threshold = None
            ns.dedup_keep = None
            ns.dedup_merge = False
            ns.interactive = False
            ns.author = None
            ns.doi = None
            ns.date = None
            ns.sort = None
            ns.enrich = None
            ns.stat = False
            ns.stat_top = None
            ns.page = None
            ns.page_size = None
            ns.show_pdf_links = False
            ns.export = None
            ns.output = None
            ns.selection = None
            ns.export_fields = None
            ns.zip = False
            ns.color = None
            ns.custom_api = None
            ns.sources = None

            # Parse max results
            if '-m' in options:
                idx = options.index('-m')
                if idx + 1 < len(options):
                    ns.max_results = int(options[idx + 1])
                else:
                    ns.max_results = 10
            elif '--max' in options:
                idx = options.index('--max')
                if idx + 1 < len(options):
                    ns.max_results = int(options[idx + 1])
                else:
                    ns.max_results = 10
            else:
                ns.max_results = 10

            # Check if any source selected
            if not any([ns.pubmed, ns.all, ns.crossref, ns.europepmc, ns.arxiv]):
                ns.pubmed = True  # Default to PubMed

            print(f"\nSearching for: '{query}'")
            print(f"Max results: {ns.max_results}")
            print()

            # Execute search
            results = dispatcher.execute_search(ns)

            if results:
                self.last_results = results
                print(f"\nFound {len(results)} articles (stored for annotation)")
                print("Use 'annotate <N>' to annotate an article")
                print("Use 'list' to see all results")
                print("Use 'view <N>' to see article details")
            else:
                print("No results found")

        except Exception as e:
            print(f"Error: {e}")
            print("Usage: search <query> [options]")

    def do_list(self, arg):
        """
        List search results or annotations.

        Usage:
            list                    List last search results
            list annotations        List all annotated articles
            list annotations -f <filter>

        Examples:
            list
            list annotations
            list annotations -f "min_rating=4"
        """
        if not arg or arg.strip() == "":
            # List last search results
            if not self.last_results:
                print("No search results available. Run 'search' first.")
                return

            print(f"\n{'='*80}")
            print(f"LAST SEARCH RESULTS ({len(self.last_results)})")
            print(f"{'='*80}\n")

            for i, article in enumerate(self.last_results, 1):
                title = article.get('title', 'No title')
                authors = article.get('authors', [])
                year = article.get('year', 'N/A')

                print(f"[{i}] {title}")
                if authors:
                    author_str = ', '.join(authors[:3]) if isinstance(authors, list) else str(authors)
                    print(f"    Authors: {author_str}")
                print(f"    Year: {year}")
                print()

        elif arg.startswith('annotations'):
            # List annotations
            manager = self._get_annotation_manager()

            filter_params = None
            if '-f' in arg or '--filter' in arg:
                # Parse filter
                parts = arg.split()
                filter_str = parts[-1] if len(parts) > 1 else ""

                filter_params = {}
                for item in filter_str.split(','):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        if key == 'min_rating':
                            filter_params['min_rating'] = int(value)
                        elif key == 'max_rating':
                            filter_params['max_rating'] = int(value)
                        elif key == 'read_status':
                            filter_params['read_status'] = value
                        elif key == 'priority':
                            filter_params['priority'] = value
                        elif key == 'tag':
                            filter_params['tags'] = [value]

            annotations = manager.list_all(filter_params)

            if not annotations:
                print("No annotated articles found.")
                return

            print(f"\n{'='*80}")
            print(f"ANNOTATED ARTICLES ({len(annotations)})")
            print(f"{'='*80}\n")

            for i, item in enumerate(annotations, 1):
                annotation = item['annotation']
                info = annotation.get('article_info', {})

                print(f"[{i}] {info.get('title', 'No title')}")

                if annotation.get('rating'):
                    stars = '' * annotation['rating']
                    print(f"    Rating: {stars} ({annotation['rating']}/5)")

                if annotation.get('tags'):
                    print(f"    Tags: {', '.join(annotation['tags'])}")

                print(f"    Status: {annotation.get('read_status', 'unread').title()} | Priority: {annotation.get('priority', 'medium').title()}")
                print()

    def do_view(self, arg):
        """
        View details of a specific article from last search.

        Usage:
            view <number>

        Example:
            view 3
        """
        if not self.last_results:
            print("No search results available. Run 'search' first.")
            return

        try:
            num = int(arg.strip())
            if 1 <= num <= len(self.last_results):
                article = self.last_results[num - 1]

                print(f"\n{'='*80}")
                print(f"ARTICLE #{num}")
                print(f"{'='*80}")
                print(f"Title: {article.get('title', 'No title')}")

                authors = article.get('authors', [])
                if authors:
                    author_str = ', '.join(authors[:5]) if isinstance(authors, list) else str(authors)
                    print(f"Authors: {author_str}")

                print(f"Year: {article.get('year', 'N/A')}")
                print(f"Journal: {article.get('journal', 'N/A')}")
                print(f"DOI: {article.get('doi', 'N/A')}")
                print(f"Source: {article.get('source', 'N/A')}")

                abstract = article.get('abstract')
                if abstract:
                    print(f"\nAbstract:\n{abstract}")

                print(f"{'='*80}\n")
            else:
                print(f"Invalid article number. Must be 1-{len(self.last_results)}")
        except ValueError:
            print("Usage: view <number>")

    # ============ ANNOTATION COMMANDS ============

    def do_annotate(self, arg):
        """
        Annotate an article from last search results.

        Usage:
            annotate <number> [options]

        Options:
            --rating <1-5>              Rate the article
            --tags <tag1,tag2>          Add tags (comma-separated)
            --comment "<text>"          Add a comment
            --priority <low|medium|high> Set priority
            --status <unread|reading|read> Set read status

        Examples:
            annotate 5 --rating 5 --tags "important,cite"
            annotate 3 --comment "Excellent methodology"
            annotate 7 --rating 4 --priority high --status read
        """
        if not self.last_results:
            print("No search results available. Run 'search' first.")
            return

        try:
            args = shlex.split(arg)
            if not args:
                print("Usage: annotate <number> [options]")
                return

            num = int(args[0])
            if not (1 <= num <= len(self.last_results)):
                print(f"Invalid article number. Must be 1-{len(self.last_results)}")
                return

            article = self.last_results[num - 1]

            # Parse options
            rating = None
            tags = None
            comment = None
            priority = None
            read_status = None

            i = 1
            while i < len(args):
                if args[i] == '--rating' and i + 1 < len(args):
                    rating = int(args[i + 1])
                    i += 2
                elif args[i] == '--tags' and i + 1 < len(args):
                    tags = [tag.strip() for tag in args[i + 1].split(',')]
                    i += 2
                elif args[i] == '--comment' and i + 1 < len(args):
                    comment = args[i + 1]
                    i += 2
                elif args[i] == '--priority' and i + 1 < len(args):
                    priority = args[i + 1]
                    i += 2
                elif args[i] == '--status' and i + 1 < len(args):
                    read_status = args[i + 1]
                    i += 2
                else:
                    i += 1

            # Annotate
            manager = self._get_annotation_manager()
            article_id = manager.annotate(
                article,
                comment=comment,
                rating=rating,
                tags=tags,
                read_status=read_status,
                priority=priority
            )

            print(f"\nArticle #{num} annotated successfully!")
            print(f"  Title: {article.get('title', 'No title')[:60]}...")
            if rating:
                print(f"  Rating: {'' * rating}")
            if tags:
                print(f"  Tags: {', '.join(tags)}")
            if comment:
                print(f"  Comment: {comment[:50]}...")
            print()

        except Exception as e:
            print(f"Error: {e}")
            print("Usage: annotate <number> [options]")

    def do_search_annotations(self, arg):
        """
        Search through your annotations.

        Usage:
            search-annotations <keyword>

        Example:
            search-annotations methodology
        """
        if not arg:
            print("Usage: search-annotations <keyword>")
            return

        manager = self._get_annotation_manager()
        results = manager.search_annotations(arg.strip())

        if not results:
            print(f"No annotations found matching: '{arg}'")
            return

        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS ({len(results)} matches)")
        print(f"{'='*80}\n")

        for i, item in enumerate(results, 1):
            annotation = item['annotation']
            info = annotation.get('article_info', {})

            print(f"[{i}] {info.get('title', 'No title')}")
            print(f"    Match type: {item['match_type']}")
            print(f"    Match: {item['match_text'][:80]}...")
            print()

    def do_export(self, arg):
        """
        Export annotations to file.

        Usage:
            export <format>

        Formats:
            markdown, json, csv

        Example:
            export markdown
            export json
        """
        if not arg or arg.strip() not in ['markdown', 'json', 'csv']:
            print("Usage: export <format>")
            print("Formats: markdown, json, csv")
            return

        manager = self._get_annotation_manager()
        output_file = manager.export_annotations(format=arg.strip())
        print(f"\nAnnotations exported to: {output_file}\n")

    def do_stats(self, arg):
        """
        Show annotation statistics.

        Usage:
            stats
        """
        manager = self._get_annotation_manager()
        stats = manager.get_statistics()

        print(f"\n{'='*80}")
        print("ANNOTATION STATISTICS")
        print(f"{'='*80}\n")

        print(f"Total Annotated Articles: {stats['total']}\n")

        if stats['by_rating']:
            print("Rating Distribution:")
            for rating in sorted(stats['by_rating'].keys(), reverse=True):
                count = stats['by_rating'][rating]
                stars = '' * rating
                bar = '█' * count
                print(f"  {stars} ({rating}): {bar} {count}")
            print()

        if stats['by_status']:
            print("Read Status:")
            for status, count in stats['by_status'].items():
                print(f"  {status.title()}: {count}")
            print()

        if stats['by_priority']:
            print("Priority:")
            for priority, count in stats['by_priority'].items():
                print(f"  {priority.title()}: {count}")
            print()

        print(f"Comments:")
        print(f"  Articles with comments: {stats['with_comments']}")
        print(f"  Total comments: {stats['total_comments']}")
        print()

        print(f"Tags:")
        print(f"  Unique tags: {stats['total_tags']}")
        if stats.get('unique_tags'):
            print(f"  Tags: {', '.join(stats['unique_tags'][:10])}")
        print()

    # ============ UTILITY COMMANDS ============

    def do_wizard(self, arg):
        """
        Launch wizard mode for guided workflows.

        Usage:
            wizard
        """
        from lixplore.utils.wizard_mode import launch_wizard
        launch_wizard(self)

    def do_clear(self, arg):
        """Clear the screen."""
        import os
        os.system('clear' if sys.platform != 'win32' else 'cls')

    def do_exit(self, arg):
        """Exit the interactive shell."""
        print("\nGoodbye!\n")
        return True

    def do_quit(self, arg):
        """Exit the interactive shell."""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """Exit on Ctrl+D."""
        print()
        return self.do_exit(arg)

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for available commands")


def launch_shell():
    """Launch the interactive shell."""
    try:
        shell = LixploreShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\n\nGoodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    launch_shell()
