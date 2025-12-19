#!/usr/bin/env python3

import argparse
import sys
from . import commands
from lixplore.utils.cache import cleanup_cache  # import correctly


def _configure_stdio():
    """Ensure stdout/stderr won't crash on Windows consoles.

    Prefer UTF-8, but at minimum avoid UnicodeEncodeError by replacing
    unencodable characters. This helps when running under cp1252 on
    GitHub Actions Windows runners.
    """
    try:
        if hasattr(sys.stdout, "reconfigure"):
            try:
                # Try UTF-8 first
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                # Fallback to current encoding with replacement
                sys.stdout.reconfigure(errors="replace")
                sys.stderr.reconfigure(errors="replace")
        else:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        # Last resort: ignore failures, but keep running
        pass


def main():
    # Ensure safe I/O early
    _configure_stdio()

    # run cleanup first
    cleanup_cache(days=7)

    parser = argparse.ArgumentParser(
        description="Lixplore Literature CLI Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    commands.add_commands(parser)
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

