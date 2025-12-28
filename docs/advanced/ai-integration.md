# AI Integration Guide for Lixplore
**How to Use OpenAI, Gemini, and Other AI APIs with Lixplore**

---

## Important Note

✅ **Lixplore does NOT include any ML/AI models**  
✅ **No machine learning dependencies**  
✅ **Lixplore is purely a search and export tool**

This is GOOD because:
- Lightweight and fast
- No expensive compute requirements
- Users can choose their own AI tools
- Modular and flexible

---

## AI Integration Strategies

Users can integrate AI with Lixplore through **piping and scripting**.

---

## 1. OpenAI Integration Examples

### Use Case 1: Summarize Search Results
```python
#!/usr/bin/env python3
"""
Script: summarize_papers.py
Searches Lixplore, sends to OpenAI for summarization
"""

import subprocess
import json
from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")

# 1. Search with Lixplore
result = subprocess.run(
    ["lixplore", "-P", "-q", "CRISPR therapy", "-m", "20", "-X", "json"],
    capture_output=True,
    text=True
)

# 2. Parse results
papers = json.loads(result.stdout)

# 3. Send to OpenAI for analysis
titles = [p['title'] for p in papers[:10]]
prompt = f"""Analyze these recent CRISPR research papers and provide:
1. Main trends
2. Key findings
3. Research gaps

Papers:
{chr(10).join(f"{i+1}. {title}" for i, title in enumerate(titles))}
"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
```

### Use Case 2: Filter Relevant Papers with AI
```python
#!/usr/bin/env python3
"""
Script: ai_filter.py
Filter papers by relevance using OpenAI
"""

import subprocess
import json
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Search
papers_json = subprocess.check_output([
    "lixplore", "-P", "-q", "cancer treatment", 
    "-m", "50", "-X", "json"
])
papers = json.loads(papers_json)

# Filter with AI
relevant_papers = []
for paper in papers:
    prompt = f"""Is this paper relevant to immunotherapy research?
    Title: {paper['title']}
    Abstract: {paper.get('abstract', 'N/A')}
    
    Answer: YES or NO"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    
    if "YES" in response.choices[0].message.content:
        relevant_papers.append(paper)

print(f"Found {len(relevant_papers)} relevant papers out of {len(papers)}")

# Save filtered results
with open("filtered_papers.json", "w") as f:
    json.dump(relevant_papers, f, indent=2)
```

---

## 2. Google Gemini Integration

### Use Case: Generate Literature Review with Gemini
```python
#!/usr/bin/env python3
"""
Script: gemini_review.py
Generate literature review using Gemini
"""

import subprocess
import json
import google.generativeai as genai

genai.configure(api_key='your-gemini-api-key')
model = genai.GenerativeModel('gemini-pro')

# Search with Lixplore
papers_json = subprocess.check_output([
    "lixplore", "-A", "-q", "machine learning healthcare",
    "-m", "100", "-D", "-X", "json"
])
papers = json.loads(papers_json)

# Prepare context
context = "\n\n".join([
    f"Title: {p['title']}\nYear: {p.get('year', 'N/A')}\n"
    f"Authors: {p.get('authors', 'N/A')}\n"
    f"Abstract: {p.get('abstract', 'N/A')[:500]}"
    for p in papers[:20]
])

# Generate review
prompt = f"""Based on these recent papers, write a comprehensive 
literature review on machine learning in healthcare:

{context}

Include:
1. Introduction
2. Main themes
3. Methodologies
4. Conclusions
5. Future directions
"""

response = model.generate_content(prompt)
print(response.text)

# Save to file
with open("literature_review.md", "w") as f:
    f.write(response.text)
```

---

## 3. Custom AI Workflows

### Workflow 1: Automated Research Assistant
```bash
#!/bin/bash
# Script: research_assistant.sh
# Daily AI-powered research monitoring

TOPIC="$1"
DATE=$(date +%Y%m%d)

# 1. Search with Lixplore
lixplore -A -q "$TOPIC" -m 50 -D --sort newest -X json -o "raw_$DATE.json"

# 2. Process with Python + AI
python3 << EOF
import json
from openai import OpenAI

client = OpenAI(api_key="your-key")

with open("raw_$DATE.json") as f:
    papers = json.load(f)

# Get AI summary
titles = [p['title'] for p in papers[:15]]
prompt = f"Summarize key findings from these papers: {titles}"

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

with open("summary_$DATE.txt", "w") as f:
    f.write(response.choices[0].message.content)
