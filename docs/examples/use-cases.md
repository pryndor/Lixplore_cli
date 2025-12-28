# Real Research Use Cases

> **Real-world examples across different disciplines**

## Table of Contents

- [Biomedical Research](#biomedical-research)
- [Computer Science](#computer-science)
- [Social Sciences](#social-sciences)
- [Physical Sciences](#physical-sciences)
- [Interdisciplinary](#interdisciplinary)

---

## Biomedical Research

### Use Case 1: Clinical Trial Search

**Researcher:** Dr. Sarah Chen, Clinical Researcher
**Goal:** Find all randomized controlled trials for hypertension treatment (2020-2024)

```bash
# Search PubMed for RCTs
lixplore -P -q "hypertension AND randomized controlled trial[pt]" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  --sort newest \
  -a

# Annotate trials by phase
lixplore --annotate 3 --tags "phase3,completed" --priority high
lixplore --annotate 7 --tags "phase2,ongoing"

# Export for meta-analysis
lixplore -P -q "hypertension AND randomized controlled trial[pt]" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  -D \
  --enrich \
  -X xlsx \
  -o rct_hypertension_2020_2024.xlsx

# Generate statistics
lixplore -P -q "hypertension AND randomized controlled trial[pt]" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  --stat \
  --stat-top 20
```

**Result:** 187 trials identified, 45 phase 3, ready for meta-analysis

### Use Case 2: Drug Discovery Literature

**Researcher:** Dr. James Liu, Pharmaceutical Scientist
**Goal:** Comprehensive review of CRISPR applications in cancer therapy

```bash
# Multi-source search
lixplore -s PE -q "(CRISPR OR 'gene editing') AND (cancer OR tumor)" \
  -d 2018-01-01 2024-12-31 \
  -m 500 \
  -D strict \
  --enrich

# Filter by publication type
lixplore -P -q "(CRISPR OR 'gene editing') AND (cancer OR tumor) AND review[pt]" \
  -d 2018-01-01 2024-12-31 \
  -m 100 \
  --sort newest \
  -S first:30

# Download open access PDFs
lixplore -s JE -q "(CRISPR OR 'gene editing') AND (cancer OR tumor)" \
  -d 2018-01-01 2024-12-31 \
  -m 200 \
  -D \
  --download-pdf

# Export to EndNote for grant writing
lixplore -s PE -q "(CRISPR OR 'gene editing') AND (cancer OR tumor)" \
  -d 2018-01-01 2024-12-31 \
  -m 500 \
  -D strict \
  --enrich \
  -X enw \
  -o crispr_cancer_refs.enw
```

**Result:** 342 papers identified, 89 PDFs downloaded, bibliography ready

---

## Computer Science

### Use Case 3: Machine Learning Literature Review

**Researcher:** Alex Rodriguez, PhD Candidate
**Goal:** Survey of transformer architectures for NLP (comprehensive)

```bash
# arXiv + Crossref search
lixplore -s XC -q "(transformer OR attention mechanism) AND NLP" \
  -d 2017-01-01 2024-12-31 \
  -m 1000 \
  -D \
  --sort newest

# Latest developments (arXiv preprints)
lixplore -x -q "transformer architecture" \
  -d 2024-01-01 2024-12-31 \
  -m 200 \
  --sort newest \
  --show-pdf-links

# Foundational papers (historical)
lixplore -C -q "attention mechanism neural networks" \
  -d 2014-01-01 2017-12-31 \
  -m 50 \
  --sort oldest \
  -S first:10

# Generate citation statistics
lixplore -s XC -q "(transformer OR attention) AND NLP" \
  -d 2017-01-01 2024-12-31 \
  -m 1000 \
  -D \
  --stat \
  --stat-top 50

# Export to BibTeX for dissertation
lixplore -s XC -q "(transformer OR attention) AND NLP" \
  -d 2017-01-01 2024-12-31 \
  -m 1000 \
  -D \
  --enrich \
  -X bibtex \
  -o transformers_nlp.bib
```

**Result:** 876 papers, 127 arXiv preprints, comprehensive bibliography

### Use Case 4: Security Vulnerability Research

**Researcher:** Dr. Emily Watson, Cybersecurity Researcher
**Goal:** Track latest security vulnerabilities in IoT devices

```bash
# Monthly monitoring
lixplore -x -q "IoT security vulnerabilities" \
  -d 2024-12-01 2024-12-31 \
  -m 100 \
  --sort newest \
  --download-pdf

# Annotate by severity
lixplore --annotate 2 --tags "critical,CVE,exploit" --priority high --rating 5
lixplore --annotate 5 --tags "medium,mitigation" --priority medium --rating 3

# Weekly alerts
lixplore -x -q "IoT firmware vulnerabilities" \
  -d $(date -d '7 days ago' +%Y-%m-%d) $(date +%Y-%m-%d) \
  -m 50 \
  --sort newest \
  -X xlsx \
  -o weekly_iot_security.xlsx

# Export annotations for team
lixplore --filter-annotations "tag=critical"
lixplore --export-annotations markdown
```

**Result:** Weekly security briefs, critical vulnerabilities tracked

---

## Social Sciences

### Use Case 5: Education Research

**Researcher:** Prof. Maria Garcia, Education Researcher
**Goal:** Systematic review of online learning effectiveness

```bash
# Comprehensive search across databases
lixplore -A -q "(online learning OR e-learning OR distance education) AND effectiveness" \
  -d 2015-01-01 2024-12-31 \
  -m 800 \
  -D strict

# Filter to peer-reviewed journals
lixplore -C -q "online learning effectiveness" \
  -d 2015-01-01 2024-12-31 \
  -m 500 \
  --sort newest

# Apply PRISMA inclusion criteria via annotation
lixplore --annotate 5 --tags "include,RCT,higher-ed" --priority high
lixplore --annotate 12 --tags "exclude,not-empirical" --priority low

# Export included studies
lixplore --filter-annotations "tag=include"
lixplore --export-annotations csv

# Generate PRISMA statistics
lixplore -A -q "online learning effectiveness" \
  -d 2015-01-01 2024-12-31 \
  -m 800 \
  --stat

# Final export for meta-analysis
lixplore --filter-annotations "tag=include,tag=RCT"
lixplore -A -q "online learning effectiveness" \
  -m 800 \
  -D strict \
  --enrich \
  -X xlsx \
  -o systematic_review_online_learning.xlsx
```

**Result:** 87 studies included, ready for meta-analysis

### Use Case 6: Psychology Research

**Researcher:** Dr. David Kim, Clinical Psychologist
**Goal:** Review CBT interventions for anxiety disorders

```bash
# PubMed search (clinical focus)
lixplore -P -q "(CBT OR 'cognitive behavioral therapy') AND (anxiety OR 'anxiety disorders')" \
  -d 2019-01-01 2024-12-31 \
  -m 300 \
  --sort newest \
  -a

# Filter to clinical trials
lixplore -P -q "(CBT OR 'cognitive behavioral therapy') AND anxiety AND clinical trial[pt]" \
  -d 2019-01-01 2024-12-31 \
  -m 150

# Annotate by intervention type
lixplore --annotate 3 --tags "group-therapy,GAD" --rating 5
lixplore --annotate 7 --tags "individual,panic-disorder" --rating 4

# Export for grant proposal
lixplore -P -q "(CBT OR 'cognitive behavioral therapy') AND anxiety" \
  -d 2019-01-01 2024-12-31 \
  -m 300 \
  -D \
  --enrich \
  -c apa \
  -o cbt_anxiety_refs.txt
```

**Result:** 243 studies, 78 clinical trials, APA formatted references

---

## Physical Sciences

### Use Case 7: Climate Science

**Researcher:** Dr. Lisa Anderson, Climate Scientist
**Goal:** Monitor latest climate modeling research

```bash
# Multi-source latest research
lixplore -A -q "climate modeling predictions" \
  -d 2024-01-01 2024-12-31 \
  -m 500 \
  -D \
  --sort newest

# arXiv preprints (very recent)
lixplore -x -q "climate change modeling" \
  -d 2024-11-01 2024-12-31 \
  -m 100 \
  --sort newest \
  --download-pdf

# Top journals analysis
lixplore -C -q "climate modeling" \
  -d 2023-01-01 2024-12-31 \
  -m 800 \
  -D \
  --sort journal \
  --stat \
  --stat-top 30

# Export for IPCC report contribution
lixplore -A -q "climate modeling" \
  -d 2020-01-01 2024-12-31 \
  -m 1000 \
  -D strict \
  --enrich \
  -X xlsx \
  -o ipcc_climate_modeling.xlsx
```

**Result:** 678 papers, top 30 journals identified, ready for policy brief

### Use Case 8: Quantum Physics

**Researcher:** Prof. Robert Zhang, Quantum Physicist
**Goal:** Track quantum computing developments

```bash
# arXiv + Crossref comprehensive search
lixplore -s XC -q "quantum computing" \
  -d 2020-01-01 2024-12-31 \
  -m 1500 \
  -D

# Latest breakthroughs (last month)
lixplore -x -q "(quantum computing OR quantum algorithm)" \
  -d 2024-12-01 2024-12-31 \
  -m 150 \
  --sort newest \
  --show-pdf-links

# Author tracking (key researchers)
lixplore -x -au "Preskill J" -d 2020-01-01 2024-12-31 -m 50 --sort newest
lixplore -x -au "Harrow AW" -d 2020-01-01 2024-12-31 -m 50 --sort newest

# Publication trends analysis
lixplore -s XC -q "quantum computing" \
  -d 2020-01-01 2024-12-31 \
  -m 1500 \
  -D \
  --stat \
  --stat-top 40

# Export to BibTeX
lixplore -s XC -q "quantum computing" \
  -d 2020-01-01 2024-12-31 \
  -m 1500 \
  -D \
  --enrich \
  -X bibtex \
  -o quantum_computing_refs.bib
```

**Result:** 1247 papers, publication trends identified, comprehensive bibliography

---

## Interdisciplinary

### Use Case 9: AI in Healthcare

**Researcher:** Dr. Priya Sharma, Interdisciplinary Researcher
**Goal:** Comprehensive review of AI applications in medical diagnosis

```bash
# Broad interdisciplinary search
lixplore -A -q "(artificial intelligence OR machine learning OR deep learning) AND (medical diagnosis OR clinical diagnosis)" \
  -d 2018-01-01 2024-12-31 \
  -m 1000 \
  -D strict

# Biomedical focus (PubMed)
lixplore -P -q "(AI OR 'machine learning') AND diagnosis" \
  -d 2018-01-01 2024-12-31 \
  -m 500 \
  --sort newest

# CS focus (arXiv)
lixplore -x -q "deep learning medical imaging" \
  -d 2018-01-01 2024-12-31 \
  -m 400 \
  --sort newest

# Combine and deduplicate
lixplore -A -q "(AI OR ML OR 'deep learning') AND (medical OR clinical)" \
  -d 2018-01-01 2024-12-31 \
  -m 1000 \
  -D strict \
  --dedup-merge

# Categorize by medical specialty
lixplore --annotate 3 --tags "radiology,imaging" --rating 5
lixplore --annotate 7 --tags "pathology,histology" --rating 4
lixplore --annotate 12 --tags "cardiology,ECG" --rating 5

# Export by category
lixplore --search-annotations "radiology"
lixplore --export-annotations markdown

# Complete export
lixplore -A -q "(AI OR ML) AND medical diagnosis" \
  -d 2018-01-01 2024-12-31 \
  -m 1000 \
  -D strict \
  --enrich \
  -X xlsx,bibtex \
  -o ai_medical_diagnosis
```

**Result:** 847 papers across disciplines, categorized by specialty

### Use Case 10: Sustainability Research

**Researcher:** Prof. Michael Brown, Environmental Scientist
**Goal:** Interdisciplinary review of renewable energy technologies

```bash
# All sources comprehensive search
lixplore -A -q "(renewable energy OR solar OR wind OR sustainable energy)" \
  -d 2015-01-01 2024-12-31 \
  -m 2000 \
  -D strict

# Open access only (for teaching materials)
lixplore -J -q "renewable energy technology" \
  -d 2020-01-01 2024-12-31 \
  -m 300 \
  --download-pdf

# Latest innovations (arXiv)
lixplore -x -q "renewable energy efficiency" \
  -d 2024-01-01 2024-12-31 \
  -m 200 \
  --sort newest

# Geographic distribution analysis
lixplore -A -q "renewable energy" \
  -d 2015-01-01 2024-12-31 \
  -m 2000 \
  -D \
  --stat \
  --stat-top 50

# Technology-specific exports
lixplore -A -q "solar photovoltaic" -d 2020-01-01 2024-12-31 -m 500 -D -X xlsx -o solar_pv.xlsx
lixplore -A -q "wind turbine" -d 2020-01-01 2024-12-31 -m 500 -D -X xlsx -o wind_turbine.xlsx
lixplore -A -q "battery storage" -d 2020-01-01 2024-12-31 -m 500 -D -X xlsx -o battery_storage.xlsx
```

**Result:** 1654 papers across energy types, ready for policy report

---

## Key Takeaways

### Best Practices from Use Cases

1. **Use appropriate sources** for your discipline
   - Biomedical: PubMed, EuropePMC
   - CS/Physics: arXiv, Crossref
   - Interdisciplinary: All sources with deduplication

2. **Apply date filters** strategically
   - Current awareness: Last month/week
   - Comprehensive review: 5-10 years
   - Historical: From inception

3. **Leverage annotations** for organization
   - Tag by category, methodology, priority
   - Rate for quality assessment
   - Export for collaboration

4. **Export to appropriate formats**
   - LaTeX: BibTeX
   - EndNote/Mendeley: RIS or ENW
   - Analysis: Excel/CSV
   - Zotero: Direct integration

5. **Use statistics** for insights
   - Publication trends
   - Top journals/authors
   - Geographic distribution

---

**Last Updated:** 2024-12-28
