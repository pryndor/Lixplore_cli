# lixplore → lixplore-cli

This package only exists so that `pip install lixplore` installs
[**lixplore-cli**](https://pypi.org/project/lixplore-cli/), the Lixplore
academic literature search tool. It contains no code of its own.

Please install the real package directly:

```bash
pip install lixplore-cli
```

## Maintainers: building and uploading

```bash
cd packaging/pypi-lixplore
python -m build
twine check --strict dist/*
twine upload dist/*   # needs an account-wide PyPI token the first time
```
