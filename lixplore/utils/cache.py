#!/usr/bin/env python3

import os
from datetime import datetime, timedelta

CACHE_DIR = os.path.expanduser("~/.lixplore_cache")

def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def cleanup_cache(days=7):
    ensure_cache_dir()
    now = datetime.now()
    for f in os.listdir(CACHE_DIR):
        path = os.path.join(CACHE_DIR, f)
        if os.path.isfile(path):
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if now - mtime > timedelta(days=days):
                os.remove(path)

