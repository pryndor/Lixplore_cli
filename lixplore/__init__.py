from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lixplore-cli")
except PackageNotFoundError:
    __version__ = "unknown"
