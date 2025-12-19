# 🔌 TODO: Plugin System for v1.1.0

**Status:** Planned for next release  
**Priority:** High  
**Estimated Time:** 6-8 hours  
**Version:** 1.1.0  

---

## 🎯 Feature Overview

**Goal:** Allow users to add custom data sources (Springer, IEEE, etc.) without modifying code.

**Implementation:** Add `-p` / `--plugin` flag for custom sources via configuration files.

---

## ✅ Why This Feature?

- ✅ Users can integrate ANY academic API they have access to
- ✅ No code modification needed - just config files
- ✅ Doesn't affect existing flags (-P, -C, -J, -E, -x, -A, -s)
- ✅ Makes Lixplore truly extensible
- ✅ Community can share plugin configs
- ✅ Future-proof design

---

## 🎨 Design Decisions (Already Agreed)

### **Flag Choice:** `-p` / `--plugin`
```bash
# Usage:
lixplore -p springer -q "cancer" -m 10
lixplore --plugin ieee -q "machine learning" -m 20

# Combined with existing features:
lixplore -p springer -q "cancer" --sort newest -X xlsx -S first:10
```

### **Why `-p`?**
- ✅ Doesn't conflict with existing flags
- ✅ Clear meaning (plugin)
- ✅ Short and easy to type
- ✅ All current functionality unchanged

---

## 📋 Implementation Checklist

### **Code Changes:**

- [ ] Create `lixplore/plugin_system.py` - Plugin loader and manager
- [ ] Create `lixplore/plugins/` directory - User plugins location
- [ ] Add `-p` / `--plugin` flag to `commands.py`
- [ ] Add plugin loader to `dispatcher.py`
- [ ] Add plugin config parser (YAML)
- [ ] Add plugin directory scanner
- [ ] Add API key management
- [ ] Add error handling for plugins

### **Configuration:**

- [ ] Create `~/.lixplore/plugins/` directory (user config location)
- [ ] Create plugin config schema (YAML format)
- [ ] Add validation for plugin configs
- [ ] Add plugin enable/disable toggle

### **Documentation:**

- [ ] Create `PLUGIN_SYSTEM.md` - Complete user guide
- [ ] Create `PLUGIN_TEMPLATE.yaml` - Template for users
- [ ] Create `PLUGIN_EXAMPLES/` with real examples:
  - [ ] Springer example
  - [ ] IEEE example
  - [ ] Semantic Scholar example
  - [ ] Generic REST API example
- [ ] Update `--help` with `-p` flag
- [ ] Update `--examples` with plugin usage
- [ ] Update man page (`docs/lixplore.1`)
- [ ] Update `README.md` with plugin section
- [ ] Update `CHANGELOG.md` for v1.1.0

### **Testing:**

- [ ] Test plugin loading
- [ ] Test plugin execution
- [ ] Test error handling
- [ ] Test with multiple plugins
- [ ] Test API key management
- [ ] Test on Linux, macOS, Windows

---

## 🔧 Technical Implementation Notes

### **File Structure:**
```
lixplore/
├── plugin_system.py          # NEW: Plugin loader
├── plugins/                   # NEW: Built-in plugin examples
│   └── __init__.py
├── commands.py                # MODIFY: Add -p flag
└── dispatcher.py              # MODIFY: Add plugin support

~/.lixplore/
└── plugins/                   # USER: Custom plugins here
    ├── springer.yaml
    ├── ieee.yaml
    └── my_custom_api.yaml
```

### **Plugin Config Format (YAML):**
```yaml
plugin:
  name: springer
  description: "Springer Academic Journals"
  enabled: true

authentication:
  type: api_key
  key: YOUR_API_KEY
  header: "X-API-Key"

endpoint:
  url: "https://api.springer.com/meta/v2/json"
  method: GET
  params:
    q: "{query}"
    p: "{max_results}"
    api_key: "{api_key}"

field_mapping:
  title: "records[*].title"
  authors: "records[*].creators[*].creator"
  year: "records[*].publicationDate[:4]"
  abstract: "records[*].abstract"
  doi: "records[*].doi"
  journal: "records[*].publicationName"
  url: "records[*].url[0].value"
  source: "Springer"
```

### **Usage Examples:**
```bash
# Search using Springer plugin
lixplore -p springer -q "quantum computing" -m 20

# Combine with sorting and export
lixplore -p springer -q "cancer" --sort newest -S first:10 -X xlsx

# Combined with other features
lixplore -p ieee -q "machine learning" -m 50 -D -X enw
```

---

## 📚 Documentation to Create

### **1. PLUGIN_SYSTEM.md** (Main Guide)
- Introduction to plugins
- How plugins work
- Creating your first plugin
- Configuration file reference
- API authentication methods
- Field mapping guide
- Troubleshooting
- FAQ

### **2. PLUGIN_TEMPLATE.yaml** (Copy-Paste Template)
- Complete template with all options
- Inline comments explaining each field
- Multiple authentication examples
- Field mapping examples

### **3. PLUGIN_EXAMPLES/** (Real Examples)
- `springer.yaml` - Springer API
- `ieee.yaml` - IEEE Xplore
- `semantic_scholar.yaml` - Semantic Scholar
- `generic_rest_api.yaml` - Generic template

### **4. Update Existing Docs:**
- `README.md` - Add plugin section
- `--help` - Add `-p` flag documentation
- `--examples` - Add plugin usage examples
- `docs/lixplore.1` - Add to man page
- `CHANGELOG.md` - v1.1.0 release notes

---

## 🎯 User Experience

### **Step 1: User has Springer API access**
```bash
# User visits Springer dev portal, gets API key
```

### **Step 2: Create plugin config**
```bash
# Copy template
cp PLUGIN_TEMPLATE.yaml ~/.lixplore/plugins/springer.yaml

# Edit and add API key
nano ~/.lixplore/plugins/springer.yaml
```

### **Step 3: Use it!**
```bash
# Search Springer
lixplore -p springer -q "cancer treatment" -m 20

# Works with all existing features
lixplore -p springer -q "cancer" --sort newest -X xlsx
```

---

## ⚠️ Important Considerations

### **Backward Compatibility:**
- ✅ All existing commands must work unchanged
- ✅ No breaking changes to current flags
- ✅ `-p` is NEW flag, doesn't conflict

### **Security:**
- ⚠️ API keys in config files - document security best practices
- ✅ Support environment variables: `SPRINGER_API_KEY`
- ✅ File permissions: Only user can read config

### **Error Handling:**
- ✅ Clear error if plugin not found
- ✅ Clear error if API key missing
- ✅ Clear error if config invalid
- ✅ Validate config on load

---

## 🚀 Release Plan

### **v1.0.0** (Current - Ready to Deploy)
- All current features
- 26 flags
- 8 export formats
- Boolean operators
- Smart selection
- Sorting
- Review mode

### **v1.1.0** (Next - Plugin System)
- Add plugin system
- `-p` / `--plugin` flag
- Plugin config support
- Complete documentation
- Example plugins

### **Future (v1.2.0+)**
- Plugin marketplace
- `lixplore plugin install <name>`
- Plugin validation tool
- Community plugin repository

---

## 📅 Timeline Suggestion

1. **Deploy v1.0.0 first** (ready now)
2. **Get user feedback** (1-2 weeks)
3. **Implement plugin system** (1-2 days)
4. **Test thoroughly** (1 day)
5. **Release v1.1.0** (after testing)

---

## 💡 Implementation Tips

### **Start Simple:**
1. Basic plugin loader (read YAML)
2. Execute plugin (make API call)
3. Map fields to standard format
4. Return results

### **Then Enhance:**
1. Add API key management
2. Add validation
3. Add error handling
4. Add examples

### **Testing Strategy:**
```bash
# Test with example config
lixplore -p example -q "test"

# Test error handling
lixplore -p nonexistent -q "test"

# Test with real API (if available)
lixplore -p springer -q "test" -m 2
```

---

## 📖 References for Implementation

### **Python Libraries Needed:**
- `PyYAML` - For config parsing (add to requirements.txt)
- `jsonpath-ng` - For field mapping (optional)
- Built-in `requests` - Already have it

### **Design Patterns:**
- Plugin architecture
- Strategy pattern
- Configuration-driven development

### **Similar Projects for Inspiration:**
- Poetry plugins
- Pytest plugins
- VS Code extensions

---

## ✅ Success Criteria

After implementation, users should be able to:

1. ✅ Create a plugin config file
2. ✅ Add their API key
3. ✅ Search using: `lixplore -p <name> -q "query"`
4. ✅ Combine with all existing features
5. ✅ Get results in standard format
6. ✅ Export, sort, select as usual

---

## 🆘 Potential Challenges & Solutions

### **Challenge 1: Different API Response Formats**
**Solution:** Flexible field mapping with JSONPath

### **Challenge 2: Various Authentication Methods**
**Solution:** Support multiple auth types (API key, Bearer, OAuth)

### **Challenge 3: API Rate Limits**
**Solution:** Document in plugin config, add optional rate limiting

### **Challenge 4: Error Handling**
**Solution:** Comprehensive validation and clear error messages

---

## 📝 Notes from Discussion

- User wants `-p` flag approach ✓
- Must not affect existing flags ✓
- Need comprehensive documentation ✓
- Examples for Springer, IEEE, etc. ✓
- Config file driven (no code changes) ✓

---

## 🎉 This Feature Will Make Lixplore:

- ✨ **Unique** - First CLI tool with plugin system for academic search
- 🚀 **Extensible** - Users add any API
- 🌍 **Universal** - Works with any data source
- 👥 **Community-Driven** - Users share configs
- 💼 **Enterprise-Ready** - Custom internal sources

---

## 🔔 REMINDER TRIGGERS

**Set reminders for:**
- [ ] After v1.0.0 is deployed to PyPI
- [ ] After getting user feedback
- [ ] Before starting v1.1.0 development
- [ ] Review this file before implementing

**This file is your complete guide - everything is documented here!**

---

## 📞 Quick Start When Ready

When you're ready to implement:

1. Read this file completely
2. Review checklist
3. Start with "Implementation Checklist"
4. Follow "Release Plan"
5. Test using "Testing Strategy"

**Everything you need is documented here!**

---

**Version:** 1.0 (Planning Document)  
**Last Updated:** 2024-12-19  
**Next Review:** After v1.0.0 deployment  

**DON'T FORGET: This is a HIGH PRIORITY feature for v1.1.0!** 🔥
