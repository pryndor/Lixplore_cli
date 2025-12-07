#!/usr/bin/env python3

import argparse
from . import commands
from lixplore.utils.cache import cleanup_cache  # import correctly

def main():
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

