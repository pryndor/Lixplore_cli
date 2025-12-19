# Lixplore Development Roadmap

**Current Version:** 1.0.0  
**Status:** Ready for PyPI deployment  

---

## 🚀 v1.0.0 - Initial Release (CURRENT)

**Status:** ✅ COMPLETE - Ready to Deploy  
**Target Date:** December 2024  

### Features:
- ✅ Multi-source search (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- ✅ Boolean operators (AND, OR, NOT, parentheses)
- ✅ 8 export formats (CSV, Excel, JSON, BibTeX, RIS, EndNote, XML)
- ✅ Smart selection (odd, even, ranges, first:N, last:N)
- ✅ Sorting (relevant, newest, oldest, journal, author)
- ✅ Review mode (separate terminal windows)
- ✅ Deduplication
- ✅ Date filtering
- ✅ Author and DOI search
- ✅ Complete documentation (man page, help, examples, TLDR)
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ 26 command-line flags

### Documentation:
- ✅ README.md
- ✅ CHANGELOG.md
- ✅ Man page (lixplore.1)
- ✅ DEPLOYMENT_GUIDE.md
- ✅ Complete help system

---

## 🔌 v1.1.0 - Plugin System (NEXT - HIGH PRIORITY)

**Status:** 📋 PLANNED  
**Target Date:** Q1 2025  
**Priority:** 🔥 HIGH  

### Main Feature: Plugin System
- [ ] Add `-p` / `--plugin` flag for custom data sources
- [ ] Config-file driven (YAML)
- [ ] User plugins in `~/.lixplore/plugins/`
- [ ] API key management
- [ ] Plugin validation
- [ ] Example plugins (Springer, IEEE, Semantic Scholar)

### Documentation:
- [ ] PLUGIN_SYSTEM.md - Complete guide
- [ ] PLUGIN_TEMPLATE.yaml - Copy-paste template
- [ ] PLUGIN_EXAMPLES/ - Real-world examples
- [ ] Update all existing docs

### Benefits:
- Users can add ANY academic API
- No code modification needed
- Community-driven plugin sharing
- Enterprise-ready for custom sources

**👉 See: TODO_v1.1.0_PLUGIN_SYSTEM.md for complete implementation plan**

---

## 📊 v1.2.0 - Statistics & Visualization (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** Q2 2025  

### Features:
- [ ] Statistics dashboard
- [ ] Analyze results by year, journal, author
- [ ] Publication trends visualization
- [ ] Journal impact metrics
- [ ] Author collaboration networks
- [ ] Export statistics to charts/graphs

### Potential Commands:
```bash
lixplore -P -q "cancer" -m 100 --stats
lixplore -P -q "AI" -m 200 --visualize year
lixplore -A -q "research" -m 500 --network authors
```

---

## 📥 v1.3.0 - PDF Download & Management (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** Q2 2025  

### Features:
- [ ] Auto-download open access PDFs
- [ ] PDF library management
- [ ] Local PDF search
- [ ] PDF metadata extraction
- [ ] Integration with Unpaywall API
- [ ] Integration with Sci-Hub (where legal)

### Potential Commands:
```bash
lixplore -P -q "cancer" -m 20 --download-pdf
lixplore --library list
lixplore --library search "machine learning"
```

---

## 🔖 v1.4.0 - Bookmarking & Collections (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** Q3 2025  

### Features:
- [ ] Bookmark articles
- [ ] Create collections
- [ ] Tag articles
- [ ] Add notes/annotations
- [ ] Share collections
- [ ] Export collections

### Potential Commands:
```bash
lixplore bookmark add 1 2 3
lixplore collection create "Cancer Research"
lixplore collection add cancer-research 1 2 3
lixplore notes add 1 "Important study"
```

---

## 💾 v1.5.0 - Search Profiles & History (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** Q3 2025  

### Features:
- [ ] Save search queries as profiles
- [ ] Search history with filtering
- [ ] Recurring searches
- [ ] Search alerts (new papers)
- [ ] Compare search results over time

### Potential Commands:
```bash
lixplore profile save "cancer-research" -P -q "cancer treatment"
lixplore profile run cancer-research
lixplore history --last-week
lixplore alert create "COVID-19" --weekly
```

---

## 🔄 v1.6.0 - Batch Processing (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** Q4 2025  

### Features:
- [ ] Search multiple queries from file
- [ ] Batch export
- [ ] Parallel processing
- [ ] Progress tracking
- [ ] Result aggregation

### Potential Commands:
```bash
lixplore batch queries.txt
lixplore batch --parallel 4 queries.txt
lixplore batch --output results/ queries.txt
```

---

## 🌐 v2.0.0 - Web Interface (FUTURE)

**Status:** 💡 IDEA STAGE  
**Target Date:** 2026  

### Features:
- [ ] Local web UI
- [ ] Search interface
- [ ] Results visualization
- [ ] Export management
- [ ] Settings panel
- [ ] Plugin management UI

### Technology:
- FastAPI backend
- React/Vue frontend
- Local server (localhost:8000)

### Launch:
```bash
lixplore serve
# Opens browser to http://localhost:8000
```

---

## 🎯 Feature Backlog (Prioritized)

### High Priority:
1. 🔥 **Plugin System** (v1.1.0) - Most requested
2. 📊 **Statistics** (v1.2.0) - High value
3. 📥 **PDF Download** (v1.3.0) - User request

### Medium Priority:
4. 🔖 **Bookmarking** (v1.4.0) - Nice to have
5. 💾 **Search Profiles** (v1.5.0) - Convenience
6. 🔄 **Batch Processing** (v1.6.0) - Power users

### Low Priority:
7. 🌐 **Web Interface** (v2.0.0) - Optional
8. 📱 **Mobile companion** - Far future
9. 🤖 **AI recommendations** - Research needed

---

## 📋 Community Requests

*This section will be updated based on user feedback after v1.0.0 release*

- [ ] Feature request 1
- [ ] Feature request 2
- [ ] Feature request 3

---

## 🐛 Known Issues

*To be tracked after v1.0.0 release*

---

## 📅 Release Schedule

| Version | Feature | Target Date | Status |
|---------|---------|-------------|--------|
| v1.0.0 | Initial Release | Dec 2024 | ✅ Ready |
| v1.1.0 | Plugin System | Q1 2025 | 📋 Planned |
| v1.2.0 | Statistics | Q2 2025 | 💡 Idea |
| v1.3.0 | PDF Download | Q2 2025 | 💡 Idea |
| v1.4.0 | Bookmarking | Q3 2025 | 💡 Idea |
| v1.5.0 | Search Profiles | Q3 2025 | 💡 Idea |
| v1.6.0 | Batch Processing | Q4 2025 | 💡 Idea |
| v2.0.0 | Web Interface | 2026 | 💡 Idea |

---

## 🎯 Goals

### Short Term (6 months):
- ✅ Deploy v1.0.0 to PyPI
- 🔲 Implement plugin system (v1.1.0)
- 🔲 Gather user feedback
- 🔲 Build community

### Medium Term (1 year):
- 🔲 Release 3-4 feature updates
- 🔲 Grow user base
- 🔲 Community plugin library
- 🔲 Documentation site

### Long Term (2+ years):
- 🔲 Become standard tool for academic search
- 🔲 1000+ users
- 🔲 Web interface
- 🔲 Plugin marketplace

---

## 📊 Success Metrics

### v1.0.0:
- [ ] 100+ PyPI downloads in first month
- [ ] 10+ GitHub stars
- [ ] 0 critical bugs

### v1.1.0:
- [ ] 5+ community plugins
- [ ] 500+ PyPI downloads
- [ ] 25+ GitHub stars

---

## 🤝 Contributing

See future releases and pick what interests you!

---

## 📞 Contact

- GitHub Issues: Feature requests and bugs
- Discussions: General questions and ideas

---

**Last Updated:** 2024-12-19  
**Next Review:** After v1.0.0 deployment

**🔔 REMEMBER: Check TODO_v1.1.0_PLUGIN_SYSTEM.md before v1.1.0!**
