# Contributing to Lixplore

Thank you for your interest in contributing to Lixplore! This guide will help you get started.

---

## Ways to Contribute

### 1. Report Bugs

Found a bug? Open an issue:
https://github.com/pryndor/Lixplore_cli/issues

Include:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your environment (OS, Python version, Lixplore version)

### 2. Suggest Features

Have an idea? Open a feature request:
https://github.com/pryndor/Lixplore_cli/issues

Describe:
- The problem you're trying to solve
- Your proposed solution
- Why it would be useful
- Example use cases

### 3. Improve Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify explanations
- Add examples
- Improve organization

### 4. Submit Code

Want to code? Great! See below for development setup.

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Lixplore_cli.git
cd Lixplore_cli
```

### 2. Create Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8
```

### 3. Create a Branch

```bash
git checkout -b feature/my-new-feature
# or
git checkout -b fix/bug-description
```

### 4. Make Your Changes

Edit the code, add features, fix bugs.

### 5. Test Your Changes

```bash
# Run tests
pytest

# Test manually
python3 -m lixplore -P -q "test" -m 5
```

### 6. Format Code

```bash
# Format with black
black lixplore/

# Check with flake8
flake8 lixplore/
```

### 7. Commit and Push

```bash
git add .
git commit -m "Add feature: description"
git push origin feature/my-new-feature
```

### 8. Create Pull Request

Go to GitHub and create a pull request from your branch to `main`.

---

## Code Style

### Python Style

- Follow PEP 8
- Use `black` for formatting
- Maximum line length: 100 characters
- Use type hints where helpful

### Docstrings

```python
def search_pubmed(query: str, max_results: int = 10) -> list:
    """
    Search PubMed for articles.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of article dictionaries
        
    Example:
        >>> results = search_pubmed("cancer", 10)
    """
    pass
```

### Comments

- Write clear, helpful comments
- Explain "why", not "what"
- Keep comments up to date

---

## Testing

### Writing Tests

Add tests for new features in `tests/`:

```python
def test_search_pubmed():
    """Test PubMed search functionality"""
    results = search_pubmed("test", 5)
    assert len(results) <= 5
    assert all('title' in r for r in results)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_search.py

# Run with coverage
pytest --cov=lixplore
```

---

## Project Structure

```
Lixplore_cli/
├── lixplore/
│   ├── __init__.py
│   ├── commands.py          # CLI command handling
│   ├── dispatcher.py        # Main dispatch logic
│   ├── sources/             # API wrappers for each source
│   │   ├── pubmed.py
│   │   ├── arxiv.py
│   │   └── ...
│   └── utils/               # Utility modules
│       ├── annotations.py
│       ├── export.py
│       └── ...
├── tests/                   # Test suite
├── docs/                    # Documentation
├── README.md
├── setup.py
└── pyproject.toml
```

---

## Adding a New Feature

### Example: Adding a New Export Format

1. **Create the exporter**:

```python
# lixplore/utils/export.py

def export_yaml(results, output_file):
    """Export results as YAML"""
    import yaml
    with open(output_file, 'w') as f:
        yaml.dump(results, f)
```

2. **Register it**:

```python
# lixplore/dispatcher.py

EXPORT_FORMATS = {
    'csv': export_csv,
    'json': export_json,
    # Add your format:
    'yaml': export_yaml,
}
```

3. **Add CLI flag** (if needed):

```python
# lixplore/commands.py

parser.add_argument('--export-yaml', ...)
```

4. **Add tests**:

```python
# tests/test_export.py

def test_export_yaml():
    results = [{'title': 'Test'}]
    export_yaml(results, 'test.yaml')
    # Assert file contents
```

5. **Document it**:

Add to `docs/guide/export.md`

---

## Adding a New Data Source

### Example: Adding Google Scholar

1. **Create source module**:

```python
# lixplore/sources/scholar.py

def search_scholar(query, max_results=10):
    """Search Google Scholar"""
    # Implementation
    pass
```

2. **Register source**:

```python
# lixplore/dispatcher.py

SOURCES = {
    'pubmed': search_pubmed,
    'arxiv': search_arxiv,
    'scholar': search_scholar,  # Add
}
```

3. **Add CLI flag**:

```python
# lixplore/commands.py

parser.add_argument('-G', '--scholar',
                    action='store_true',
                    help='Search Google Scholar')
```

4. **Add tests and docs**

---

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style
- [ ] Tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear

### PR Description

Include:
- What the PR does
- Why it's needed
- How to test it
- Screenshots (if UI changes)
- Related issues

### Example PR Description

```markdown
## Add Google Scholar Support

Adds Google Scholar as a new data source.

### Changes
- New `scholar.py` source module
- Added `-G/--scholar` CLI flag
- Updated documentation

### Testing
python3 -m lixplore -G -q "test" -m 5

Closes #42
```

---

## Code Review Process

1. Maintainer reviews your PR
2. May request changes
3. Make requested changes
4. Once approved, PR is merged
5. Your changes are in the next release!

---

## Community Guidelines

### Be Respectful

- Be kind and professional
- Respect different viewpoints
- Help others learn
- Give constructive feedback

### Communication

- Use clear, descriptive titles
- Provide context and examples
- Be patient with responses
- Say thank you!

---

## Getting Help

### Questions About Contributing?

- Open a discussion: https://github.com/pryndor/Lixplore_cli/discussions
- Ask in your PR
- Check existing issues and PRs

### Development Questions?

- Read the code and comments
- Check existing implementations
- Ask for clarification

---

## Recognition

Contributors are recognized in:

- GitHub contributors list
- Release notes
- Future CONTRIBUTORS.md file

---

## Quick Contribution Checklist

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/Lixplore_cli.git

# 2. Create branch
git checkout -b feature/my-feature

# 3. Make changes
# ... edit code ...

# 4. Test
pytest

# 5. Format
black lixplore/

# 6. Commit
git commit -m "Add feature: description"

# 7. Push
git push origin feature/my-feature

# 8. Create PR on GitHub
```

---

## Thank You!

Every contribution, no matter how small, makes Lixplore better for everyone.

**Happy coding!**
