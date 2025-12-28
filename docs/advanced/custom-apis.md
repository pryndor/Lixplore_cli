# Custom APIs

Lixplore supports adding custom academic data sources beyond the built-in databases (PubMed, arXiv, Crossref, DOAJ, EuropePMC).

---

## Overview

Custom APIs allow you to:

- Add institutional repositories
- Integrate proprietary databases
- Connect to private data sources
- Combine multiple specialized sources

---

## Built-in Custom API Support

### List Custom APIs

View all configured custom APIs:

```bash
lixplore --list-custom-apis
```

### Create API Examples

Generate example API configuration files:

```bash
lixplore --create-api-examples
```

This creates template files in `~/.lixplore/apis/` showing the API configuration format.

---

## Custom API Configuration

### Configuration File Format

Custom APIs are defined in JSON files in `~/.lixplore/apis/`:

```json
{
  "name": "MyUniversity Repository",
  "api_url": "https://repository.myuni.edu/api/search",
  "parameters": {
    "query": "{query}",
    "max_results": "{max_results}",
    "format": "json"
  },
  "mapping": {
    "title": "metadata.title",
    "authors": "metadata.authors",
    "abstract": "metadata.abstract",
    "doi": "identifiers.doi",
    "year": "metadata.publication_year",
    "url": "links.full_text"
  }
}
```

### Using Custom APIs

```bash
# Search using a custom API
lixplore --custom-api MyUniversity -q "research topic" -m 50

# Combine with other sources
lixplore -A --custom-api MyUniversity -q "topic" -m 100
```

---

## Creating a Custom API Integration

### Step 1: Understand the API

Research your target API:

1. API endpoint URL
2. Required parameters
3. Authentication method
4. Response format (JSON, XML, etc.)
5. Field mappings

### Step 2: Create Configuration File

Create a JSON file in `~/.lixplore/apis/my_source.json`:

```json
{
  "name": "MySource",
  "description": "Custom academic database",
  "api_url": "https://api.mysource.com/search",
  "method": "GET",
  "auth": {
    "type": "api_key",
    "key_name": "apikey",
    "key_value": "YOUR_API_KEY_HERE"
  },
  "parameters": {
    "q": "{query}",
    "limit": "{max_results}",
    "sort": "relevance"
  },
  "mapping": {
    "title": "results[].title",
    "authors": "results[].author_list",
    "abstract": "results[].summary",
    "doi": "results[].doi",
    "year": "results[].year",
    "url": "results[].link",
    "journal": "results[].journal_name",
    "pmid": "results[].pubmed_id"
  },
  "response_format": "json",
  "results_path": "data.results"
}
```

### Step 3: Test the Integration

```bash
# Test with a simple query
lixplore --custom-api MySource -q "test" -m 5

# If it works, try a real search
lixplore --custom-api MySource -q "your research topic" -m 50
```

---

## Example: Institutional Repository

### Example Configuration

For a university DSpace repository:

```json
{
  "name": "UniversityRepo",
  "description": "University institutional repository",
  "api_url": "https://repository.university.edu/rest/items",
  "method": "GET",
  "parameters": {
    "query": "{query}",
    "limit": "{max_results}",
    "expand": "metadata"
  },
  "mapping": {
    "title": "metadata.dc.title",
    "authors": "metadata.dc.contributor.author",
    "abstract": "metadata.dc.description.abstract",
    "year": "metadata.dc.date.issued",
    "url": "handle"
  },
  "response_format": "json"
}
```

### Usage

```bash
# Search institutional repository
lixplore --custom-api UniversityRepo -q "faculty research" -m 100 -X xlsx -o repo_search.xlsx
```

---

## Example: Specialized Database

### SSRN (Social Science Research Network)

If SSRN had a public API (hypothetical example):

```json
{
  "name": "SSRN",
  "description": "Social Science Research Network",
  "api_url": "https://api.ssrn.com/v1/search",
  "parameters": {
    "terms": "{query}",
    "perPage": "{max_results}"
  },
  "mapping": {
    "title": "papers[].title",
    "authors": "papers[].authors",
    "abstract": "papers[].abstract",
    "year": "papers[].publication_date",
    "url": "papers[].url"
  }
}
```

---

## Authentication

### API Key Authentication

```json
{
  "auth": {
    "type": "api_key",
    "key_name": "apikey",
    "key_value": "YOUR_KEY",
    "location": "header"
  }
}
```

### Bearer Token

```json
{
  "auth": {
    "type": "bearer",
    "token": "YOUR_TOKEN"
  }
}
```

### Basic Authentication

```json
{
  "auth": {
    "type": "basic",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
  }
}
```

---

## Field Mapping

### JSON Path Notation

Use dot notation for nested fields:

```json
{
  "mapping": {
    "title": "results[].metadata.title",
    "authors": "results[].metadata.contributors.authors",
    "abstract": "results[].metadata.descriptions.abstract"
  }
}
```

### Array Handling

For arrays, use `[]`:

```json
{
  "authors": "results[].authors[]"
}
```

---

## Advanced Features

### Custom Transformations

Some APIs may require data transformation. Contact the Lixplore team if you need advanced parsing.

### Rate Limiting

Add rate limiting configuration:

```json
{
  "rate_limit": {
    "requests_per_second": 2,
    "burst": 5
  }
}
```

### Pagination

Configure pagination:

```json
{
  "pagination": {
    "type": "page",
    "page_param": "page",
    "per_page_param": "limit"
  }
}
```

---

## Common Use Cases

### University Repository Integration

```bash
# Daily monitoring of university research output
lixplore --custom-api UniversityRepo -q "2025" -m 100 --sort newest -X csv -o daily_output.csv
```

### Specialized Subject Database

```bash
# Search a specialized medical database
lixplore -P --custom-api MedicalDB -q "clinical trial" -m 200 -D -X xlsx
```

### Multiple Custom Sources

```bash
# Combine multiple custom sources
lixplore --custom-api Source1 --custom-api Source2 -q "topic" -m 100 -D
```

---

## Troubleshooting

### API Not Found

```bash
Error: Custom API 'MySource' not found
```

Solution: Check the file exists in `~/.lixplore/apis/` and the name matches.

### Authentication Failure

```bash
Error: 401 Unauthorized
```

Solution: Verify your API key/credentials in the configuration file.

### No Results Returned

Check:
1. API endpoint URL is correct
2. Parameter names match API documentation
3. Field mappings are correct
4. Test the API directly with curl first

### Malformed Response

```bash
Error: Unable to parse API response
```

Solution: Verify the `response_format` and `results_path` settings.

---

## Testing Custom APIs

### Manual Testing with curl

Before configuring in Lixplore, test with curl:

```bash
# Test the API endpoint
curl "https://api.mysource.com/search?q=test&limit=5"

# With authentication
curl -H "Authorization: Bearer YOUR_TOKEN" "https://api.mysource.com/search?q=test"
```

### Validate JSON Configuration

Use a JSON validator:

```bash
# Validate your config file
python3 -m json.tool ~/.lixplore/apis/my_source.json
```

---

## Best Practices

1. **Start Simple**: Test with minimal configuration first
2. **Document APIs**: Keep notes on API quirks and limitations
3. **Version Control**: Track your API configurations
4. **Test Thoroughly**: Test with various queries before production use
5. **Handle Errors**: Check API status codes and error messages
6. **Respect Limits**: Honor API rate limits
7. **Secure Credentials**: Don't commit API keys to version control

---

## Example Configurations

### Generic REST API

```json
{
  "name": "GenericAPI",
  "api_url": "https://api.example.com/search",
  "parameters": {
    "query": "{query}",
    "max": "{max_results}"
  },
  "mapping": {
    "title": "items[].title",
    "authors": "items[].authors",
    "abstract": "items[].description",
    "url": "items[].link"
  }
}
```

---

## Getting Help

If you need help creating a custom API integration:

1. Check API documentation
2. Use `--create-api-examples` for templates
3. Open an issue: https://github.com/pryndor/Lixplore_cli/issues
4. Share your API documentation for assistance

---

## Future Features

Planned improvements for custom APIs:

- GUI configuration tool
- More authentication methods
- Advanced data transformation
- Built-in API testing
- Sharable API configurations

---

**Next**: [Zotero Integration](zotero.md) | [Back to Advanced Features](automation.md)
